"""
backend/core/profiler.py
─────────────────────────
Core profiling engine.  Three public functions map to the three API endpoints:

    profile_summary(df, meta)    → dict   (dataset-level overview)
    profile_columns(df, schema)  → list   (per-column stats + distribution)
    profile_quality(df, schema)  → dict   (quality score + issue list)

All returned values are plain Python primitives (str/int/float/list/dict/None)
— safe to pass directly to flask.jsonify().
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

from core.logger import get_logger
from core.type_inferrer import ColumnSchema

log = get_logger(__name__)


# ── helpers ───────────────────────────────────────────────────────────────────

def _safe(value: Any) -> Any:
    """Convert numpy scalars and NaN/Inf to JSON-safe Python types."""
    if value is None:
        return None
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def _pct(n: int, total: int) -> float:
    return round(100.0 * n / total, 4) if total else 0.0


def _is_true_numeric(series: pd.Series) -> bool:
    """
    True only for genuinely numeric series — explicitly excludes boolean dtypes,
    which pass pd.api.types.is_numeric_dtype() but cannot be used with quantile().
    """
    if pd.api.types.is_bool_dtype(series.dtype):
        return False
    if hasattr(series.dtype, "name") and series.dtype.name == "boolean":
        return False
    return pd.api.types.is_numeric_dtype(series.dtype)


# ── Summary ───────────────────────────────────────────────────────────────────

def profile_summary(df: pd.DataFrame, meta: dict) -> dict:
    """
    High-level dataset overview.

    Returns
    -------
    {
        filename, extension, size_bytes,
        rows, cols, total_cells,
        missing_cells, missing_pct,
        duplicate_rows, duplicate_pct,
        numeric_cols, datetime_cols, categorical_cols, text_cols, boolean_cols,
        memory_usage_bytes
    }
    """
    rows, cols  = df.shape
    total_cells = rows * cols
    missing     = int(df.isna().sum().sum())
    duplicates  = int(df.duplicated().sum())
    memory      = int(df.memory_usage(deep=True).sum())

    dtype_counts: dict[str, int] = {}
    for col in df.columns:
        kind = _dtype_kind(df[col])
        dtype_counts[kind] = dtype_counts.get(kind, 0) + 1

    return {
        **meta,
        "rows":               rows,
        "cols":               cols,
        "total_cells":        total_cells,
        "missing_cells":      missing,
        "missing_pct":        _pct(missing, total_cells),
        "duplicate_rows":     duplicates,
        "duplicate_pct":      _pct(duplicates, rows),
        "numeric_cols":       dtype_counts.get("numeric",     0),
        "datetime_cols":      dtype_counts.get("datetime",    0),
        "categorical_cols":   dtype_counts.get("categorical", 0),
        "text_cols":          dtype_counts.get("text",        0),
        "boolean_cols":       dtype_counts.get("boolean",     0),
        "memory_usage_bytes": memory,
    }


# ── Column-level detail ───────────────────────────────────────────────────────

def profile_columns(df: pd.DataFrame, schema: list[ColumnSchema]) -> list[dict]:
    """
    Per-column profile.  Each entry contains:

    All columns
        name, logical_type, coerced_dtype,
        n_null, null_pct, n_unique, cardinality_pct

    Numeric columns (non-boolean)
        mean, std, min, p25, p50, p75, max, skewness, kurtosis, sum
        histogram: [{bin_start, bin_end, count}]   (20 equal-width bins)

    Datetime columns
        min_date, max_date, date_range_days

    Boolean columns
        true_count, false_count, true_pct

    Categorical / text columns
        top_values: [{value, count, pct}]   (top 10)
    """
    rows       = len(df)
    schema_map = {s.name: s for s in schema}
    result     = []

    for col in df.columns:
        s    = df[col]
        info = schema_map.get(col)

        entry: dict[str, Any] = {
            "name":            col,
            "logical_type":    info.logical_type  if info else _dtype_kind(s),
            "coerced_dtype":   info.coerced_dtype if info else str(s.dtype),
            "n_null":          _safe(s.isna().sum()),
            "null_pct":        _pct(int(s.isna().sum()), rows),
            "n_unique":        _safe(s.nunique(dropna=True)),
            "cardinality_pct": _pct(int(s.nunique(dropna=True)), rows),
        }

        # ── Numeric stats (explicitly exclude boolean) ─────────────────────
        if _is_true_numeric(s):
            num = s.dropna().astype(float)   # cast to float for numpy safety
            if len(num):
                q = num.quantile([0.25, 0.50, 0.75])
                entry.update({
                    "mean":     _safe(num.mean()),
                    "std":      _safe(num.std()),
                    "min":      _safe(num.min()),
                    "p25":      _safe(float(q.iloc[0])),
                    "p50":      _safe(float(q.iloc[1])),
                    "p75":      _safe(float(q.iloc[2])),
                    "max":      _safe(num.max()),
                    "skewness": _safe(num.skew()),
                    "kurtosis": _safe(num.kurt()),
                    "sum":      _safe(num.sum()),
                })
                entry["histogram"] = _histogram(num)
            else:
                entry["histogram"] = []

        # ── Datetime stats ─────────────────────────────────────────────────
        elif pd.api.types.is_datetime64_any_dtype(s):
            dt = s.dropna()
            if len(dt):
                entry.update({
                    "min_date":        str(dt.min()),
                    "max_date":        str(dt.max()),
                    "date_range_days": _safe((dt.max() - dt.min()).days),
                })

        # ── Boolean stats ──────────────────────────────────────────────────
        elif pd.api.types.is_bool_dtype(s) or (
            hasattr(s.dtype, "name") and s.dtype.name == "boolean"
        ):
            non_null = s.dropna()
            true_count  = int((non_null == True).sum())   # noqa: E712
            false_count = int((non_null == False).sum())  # noqa: E712
            entry.update({
                "true_count":  true_count,
                "false_count": false_count,
                "true_pct":    _pct(true_count, len(non_null)) if len(non_null) else 0.0,
            })

        # ── Categorical / text top values ──────────────────────────────────
        else:
            vc = s.value_counts(dropna=True).head(10)
            entry["top_values"] = [
                {"value": _safe(v), "count": int(c), "pct": _pct(int(c), rows)}
                for v, c in vc.items()
            ]

        result.append(entry)

    log.debug("profile_columns — %d columns profiled", len(result))
    return result


# ── Quality score ─────────────────────────────────────────────────────────────

def profile_quality(df: pd.DataFrame, schema: list[ColumnSchema]) -> dict:
    """
    Compute a 0–100 data-quality score from four equally-weighted components.

    Components (25 pts each)
    ────────────────────────
    completeness  – penalises missing values
    uniqueness    – penalises duplicate rows
    consistency   – penalises columns that remain as unresolved object dtype
    validity      – rewards positive logical-type identification

    Returns
    -------
    {
        score, label,
        components: {completeness, uniqueness, consistency, validity},
        issues:     [{type, severity, detail}]
    }
    """
    rows, cols  = df.shape
    total_cells = rows * cols

    # completeness (0–25)
    missing      = int(df.isna().sum().sum())
    completeness = 25.0 * (1 - missing / total_cells) if total_cells else 25.0

    # uniqueness (0–25)
    dupes      = int(df.duplicated().sum())
    uniqueness = 25.0 * (1 - dupes / rows) if rows else 25.0

    # consistency (0–25) — object columns that were not coerced
    raw_object = sum(1 for c in df.columns if df[c].dtype == object)
    consistency = 25.0 * (1 - raw_object / cols) if cols else 25.0

    # validity (0–25) — columns with a positively identified logical type
    typed    = sum(1 for s in schema if s.logical_type not in ("unknown", "text"))
    validity = 25.0 * (typed / len(schema)) if schema else 25.0

    score = max(0.0, min(100.0, round(completeness + uniqueness + consistency + validity, 1)))
    label = _quality_label(score)

    # issue list
    issues: list[dict] = []

    missing_pct = _pct(missing, total_cells)
    if missing_pct > 0:
        issues.append({
            "type":     "missing_values",
            "severity": "high" if missing_pct > 10 else "medium" if missing_pct > 2 else "low",
            "detail":   f"{missing} missing cells ({missing_pct:.2f}%)",
        })

    if dupes > 0:
        dup_pct = _pct(dupes, rows)
        issues.append({
            "type":     "duplicate_rows",
            "severity": "high" if dup_pct > 5 else "medium" if dup_pct > 1 else "low",
            "detail":   f"{dupes} duplicate rows ({dup_pct:.2f}%)",
        })

    if raw_object > 0:
        issues.append({
            "type":     "unresolved_types",
            "severity": "medium",
            "detail":   f"{raw_object} column(s) remain as unresolved 'object' type",
        })

    for s in schema:
        if s.n_null == len(df) and len(df) > 0:
            issues.append({
                "type":     "empty_column",
                "severity": "high",
                "detail":   f"Column '{s.name}' is entirely null",
            })

    log.info("Quality score: %.1f  (%s)  issues=%d", score, label, len(issues))
    return {
        "score":  score,
        "label":  label,
        "components": {
            "completeness": round(completeness, 2),
            "uniqueness":   round(uniqueness,   2),
            "consistency":  round(consistency,  2),
            "validity":     round(validity,     2),
        },
        "issues": issues,
    }


# ── private helpers ───────────────────────────────────────────────────────────

def _histogram(series: pd.Series, bins: int = 20) -> list[dict]:
    """
    Compute a histogram with up to *bins* equal-width buckets using NumPy.
    Returns [{bin_start, bin_end, count}].
    """
    try:
        arr = np.array(series.dropna(), dtype=float)
        if len(arr) < 2:
            return []
        counts, edges = np.histogram(arr, bins=bins)
        return [
            {
                "bin_start": _safe(float(edges[i])),
                "bin_end":   _safe(float(edges[i + 1])),
                "count":     int(counts[i]),
            }
            for i in range(len(counts))
        ]
    except Exception:
        return []


def _dtype_kind(s: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(s.dtype):
        return "boolean"
    if hasattr(s.dtype, "name") and s.dtype.name == "boolean":
        return "boolean"
    if _is_true_numeric(s):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(s):
        return "datetime"
    if hasattr(s.dtype, "name") and s.dtype.name == "category":
        return "categorical"
    return "text"


def _quality_label(score: float) -> str:
    from shared.constants import QUALITY_EXCELLENT, QUALITY_GOOD, QUALITY_FAIR
    if score >= QUALITY_EXCELLENT:
        return "Excellent"
    if score >= QUALITY_GOOD:
        return "Good"
    if score >= QUALITY_FAIR:
        return "Fair"
    return "Poor"