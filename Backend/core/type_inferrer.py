"""
backend/core/type_inferrer.py
──────────────────────────────
Auto data-type inference and schema detection.

Pandas reads everything as object / float64 when types are ambiguous.
In Pandas 2.x the default string backend is StringDtype (dtype.name == "str")
rather than object — this module handles both.

This module inspects each column and:
  1. Assigns a *logical* type  (numeric | datetime | boolean | categorical | text)
  2. Attempts a *safe coercion* — returns a new DataFrame with corrected dtypes
  3. Reports which columns were changed

Usage
-----
    from core.type_inferrer import infer_and_coerce
    result = infer_and_coerce(df)
    # result.df          – coerced DataFrame
    # result.schema      – list[ColumnSchema]
    # result.corrections – list of {column, from_dtype, to_dtype}
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from core.logger import get_logger

log = get_logger(__name__)


# ── constants ─────────────────────────────────────────────────────────────────

LOGICAL_NUMERIC     = "numeric"
LOGICAL_DATETIME    = "datetime"
LOGICAL_BOOLEAN     = "boolean"
LOGICAL_CATEGORICAL = "categorical"
LOGICAL_TEXT        = "text"
LOGICAL_UNKNOWN     = "unknown"

_BOOL_TRUE  = {"true", "yes", "1", "t", "y"}
_BOOL_FALSE = {"false", "no", "0", "f", "n"}

# ≤ 5 % of rows OR ≤ 50 unique values → treat as categorical
_CARDINALITY_RATIO = 0.05
_CARDINALITY_ABS   = 50


# ── data classes ──────────────────────────────────────────────────────────────

@dataclass
class ColumnSchema:
    name:          str
    raw_dtype:     str
    logical_type:  str
    coerced_dtype: str
    n_unique:      int
    n_null:        int
    coercion_note: str = ""


@dataclass
class InferenceResult:
    df:          pd.DataFrame
    schema:      list[ColumnSchema]
    corrections: list[dict]          # [{column, from_dtype, to_dtype}]


# ── helpers ───────────────────────────────────────────────────────────────────

def _is_string_like(dtype) -> bool:
    """
    Return True for both legacy object dtype AND Pandas 2.x StringDtype.
    Handles:
        object            – classic Pandas string storage
        StringDtype       – Pandas 2.x future_infer_string / ArrowDtype
        pd.api.types.is_string_dtype() catches both
    """
    if dtype == object:
        return True
    if hasattr(dtype, "name") and dtype.name in ("str", "string", "large_string"):
        return True
    return pd.api.types.is_string_dtype(dtype) and not pd.api.types.is_bool_dtype(dtype)


# ── public entry point ────────────────────────────────────────────────────────

def infer_and_coerce(df: pd.DataFrame) -> InferenceResult:
    """
    Inspect *df*, infer logical types, attempt safe coercions.
    Returns an InferenceResult with the corrected DataFrame and full schema.
    """
    df_out      = df.copy()
    schema:      list[ColumnSchema] = []
    corrections: list[dict]         = []

    for col in df_out.columns:
        series     = df_out[col]
        raw_dtype  = str(series.dtype)
        n_unique   = int(series.nunique(dropna=True))
        n_null     = int(series.isna().sum())

        logical, coerced_series, note = _classify_and_coerce(series, n_unique)

        coerced_dtype = str(coerced_series.dtype)
        if coerced_dtype != raw_dtype:
            df_out[col] = coerced_series
            corrections.append({
                "column":     col,
                "from_dtype": raw_dtype,
                "to_dtype":   coerced_dtype,
            })
            log.debug("  coerced  %-30s  %s → %s", col, raw_dtype, coerced_dtype)

        schema.append(ColumnSchema(
            name          = col,
            raw_dtype     = raw_dtype,
            logical_type  = logical,
            coerced_dtype = coerced_dtype,
            n_unique      = n_unique,
            n_null        = n_null,
            coercion_note = note,
        ))

    log.info("Type inference — %d columns, %d corrected",
             len(schema), len(corrections))
    return InferenceResult(df=df_out, schema=schema, corrections=corrections)


# ── classification logic ──────────────────────────────────────────────────────

def _classify_and_coerce(
    s: pd.Series,
    n_unique: int,
) -> tuple[str, pd.Series, str]:
    """Return (logical_type, coerced_series, note)."""
    dtype = s.dtype

    # Already bool (check BEFORE numeric — boolean passes is_numeric_dtype)
    if pd.api.types.is_bool_dtype(dtype):
        return LOGICAL_BOOLEAN, s, ""

    # Pandas nullable boolean extension type
    if hasattr(dtype, "name") and dtype.name == "boolean":
        return LOGICAL_BOOLEAN, s, ""

    # Already datetime
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return LOGICAL_DATETIME, s, ""

    # Category already
    if hasattr(dtype, "name") and dtype.name == "category":
        return LOGICAL_CATEGORICAL, s, ""

    # Already numeric (and not bool, handled above)
    if pd.api.types.is_numeric_dtype(dtype):
        return LOGICAL_NUMERIC, s, ""

    # String-like column (object in Pandas <2, StringDtype in Pandas 2+)
    if _is_string_like(dtype):
        sample = s.dropna()
        if len(sample) == 0:
            return LOGICAL_UNKNOWN, s, ""

        # Cast to plain str for pattern matching (works for both object & StringDtype)
        sample_str = sample.astype(str).str.strip()

        # ── Try boolean ───────────────────────────────────────────────────────
        lower       = sample_str.str.lower()
        unique_lower = set(lower.unique())
        if unique_lower <= (_BOOL_TRUE | _BOOL_FALSE):
            coerced = lower.map(
                lambda v: True if v in _BOOL_TRUE else False
            ).astype("boolean")
            return LOGICAL_BOOLEAN, coerced, "string→boolean"

        # ── Try numeric ───────────────────────────────────────────────────────
        numeric_attempt = pd.to_numeric(sample, errors="coerce")
        if numeric_attempt.notna().mean() >= 0.90:
            coerced = pd.to_numeric(s, errors="coerce")
            return LOGICAL_NUMERIC, coerced, "string→numeric"

        # ── Try datetime ──────────────────────────────────────────────────────
        if _looks_like_datetime(sample_str):
            try:
                coerced = pd.to_datetime(s, errors="coerce")
                if coerced.notna().mean() >= 0.80:
                    return LOGICAL_DATETIME, coerced, "string→datetime"
            except Exception:
                pass

        # ── Categorical vs free text ──────────────────────────────────────────
        n_rows = max(len(s), 1)
        if n_unique <= _CARDINALITY_ABS or (n_unique / n_rows) <= _CARDINALITY_RATIO:
            coerced = s.astype("category")
            return LOGICAL_CATEGORICAL, coerced, "string→category"

        return LOGICAL_TEXT, s, ""

    return LOGICAL_UNKNOWN, s, ""


# ── datetime heuristic ────────────────────────────────────────────────────────

_DATE_PATTERNS = re.compile(
    r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})"         # yyyy-mm-dd  /  yyyy/mm/dd
    r"|(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})"       # dd-mm-yy  /  mm/dd/yyyy
    r"|(\w{3,9} \d{1,2},?\s+\d{4})"           # Jan 01, 2024  /  January 1 2024
)


def _looks_like_datetime(sample: pd.Series, n_check: int = 20) -> bool:
    """Return True if any of the first n_check string values match a date pattern."""
    for val in sample.head(n_check):
        if _DATE_PATTERNS.search(str(val)):
            return True
    return False