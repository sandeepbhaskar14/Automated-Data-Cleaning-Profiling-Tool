"""
backend/core/cleaner.py
────────────────────────
Data-cleaning engine.

Public API
──────────
    clean_missing       (df, strategy)                   → CleanResult
    clean_missing_cols  (df, threshold)                  → CleanResult
    clean_duplicates    (df, keep, subset)               → CleanResult
    clean_outliers      (df, method, threshold, action)  → CleanResult
    clean_types         (df)                             → CleanResult
    clean_normalize     (df, columns, ops)               → CleanResult
    clean_pipeline      (df, steps)                      → CleanResult
    clean_all           (df, **kwargs)                   → CleanResult

Each function returns a CleanResult with:
    df          – cleaned DataFrame
    rows_before / rows_after
    cols_before / cols_after
    changes     – list[dict]  one entry per atomic change (JSON-safe)
    summary     – dict        top-level counts for the API layer
"""

from __future__ import annotations

import math
import re as _re
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from core.logger import get_logger
from core.type_inferrer import infer_and_coerce

log = get_logger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
#  Result container
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class CleanResult:
    df:           pd.DataFrame
    rows_before:  int
    rows_after:   int
    cols_before:  int
    cols_after:   int
    changes:      list[dict] = field(default_factory=list)

    @property
    def summary(self) -> dict:
        return {
            "rows_before":  self.rows_before,
            "rows_after":   self.rows_after,
            "rows_removed": self.rows_before - self.rows_after,
            "cols_before":  self.cols_before,
            "cols_after":   self.cols_after,
            "cols_removed": self.cols_before - self.cols_after,
            "changes":      self.changes,
        }


# ══════════════════════════════════════════════════════════════════════════════
#  Shared helpers
# ══════════════════════════════════════════════════════════════════════════════

def _safe(v: Any) -> Any:
    """Convert numpy scalars / NaN / Inf to JSON-safe Python types."""
    if v is None:
        return None
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    return v


def _is_true_numeric(s: pd.Series) -> bool:
    """True for genuinely numeric columns — excludes boolean dtypes."""
    if pd.api.types.is_bool_dtype(s.dtype):
        return False
    if hasattr(s.dtype, "name") and s.dtype.name == "boolean":
        return False
    return pd.api.types.is_numeric_dtype(s.dtype)


def _is_string_col(s: pd.Series) -> bool:
    """True for object / Pandas 2.x StringDtype columns."""
    if s.dtype == object:
        return True
    if hasattr(s.dtype, "name") and s.dtype.name in ("str", "string", "large_string"):
        return True
    return pd.api.types.is_string_dtype(s.dtype) and not pd.api.types.is_bool_dtype(s.dtype)


# ══════════════════════════════════════════════════════════════════════════════
#  1.  Missing-value handling (row strategy)
# ══════════════════════════════════════════════════════════════════════════════

_MISSING_STRATEGIES = (
    "mean", "median", "mode", "drop", "ffill", "bfill", "zero", "unknown"
)


def clean_missing(
    df: pd.DataFrame,
    strategy: str = "mean",
) -> CleanResult:
    """
    Handle missing values across all columns.

    Strategies
    ----------
    mean    – numeric → column mean;      non-numeric → mode
    median  – numeric → column median;    non-numeric → mode
    mode    – every column → first mode
    drop    – drop any row containing at least one null
    ffill   – forward-fill
    bfill   – backward-fill
    zero    – numeric → 0;  non-numeric → ""
    unknown – non-numeric → "Unknown";  numeric → column mean
    """
    strategy = strategy.lower()
    if strategy not in _MISSING_STRATEGIES:
        strategy = "mean"

    rows_before, cols_before = df.shape
    out     = df.copy()
    changes: list[dict] = []
    total_nulls = int(out.isna().sum().sum())

    if strategy == "drop":
        out = out.dropna()
        dropped = rows_before - len(out)
        if dropped:
            changes.append({
                "operation":   "drop_rows_with_nulls",
                "rows_dropped": dropped,
                "detail":       f"Dropped {dropped} row(s) with at least one null.",
            })
    else:
        for col in out.columns:
            n_null = int(out[col].isna().sum())
            if n_null == 0:
                continue
            s = out[col]
            if strategy == "ffill":
                out[col] = s.ffill()
                filled = n_null - int(out[col].isna().sum())
                _record_fill(changes, col, "forward-fill", filled, n_null)
            elif strategy == "bfill":
                out[col] = s.bfill()
                filled = n_null - int(out[col].isna().sum())
                _record_fill(changes, col, "backward-fill", filled, n_null)
            elif strategy == "mode":
                _fill_mode(out, col, changes, n_null)
            elif strategy in ("mean", "median"):
                if _is_true_numeric(s):
                    fv = s.mean() if strategy == "mean" else s.median()
                    if fv is not None and not (isinstance(fv, float) and math.isnan(fv)):
                        out[col] = s.fillna(fv)
                        _record_fill(changes, col, f"{strategy}={_safe(fv):.4g}", n_null, n_null)
                    else:
                        _fill_mode(out, col, changes, n_null)
                else:
                    _fill_mode(out, col, changes, n_null)
            elif strategy == "zero":
                if _is_true_numeric(s):
                    out[col] = s.fillna(0)
                    _record_fill(changes, col, "0", n_null, n_null)
                else:
                    out[col] = s.fillna("")
                    _record_fill(changes, col, '""', n_null, n_null)
            elif strategy == "unknown":
                if _is_true_numeric(s):
                    fv = s.mean()
                    if fv is not None and not (isinstance(fv, float) and math.isnan(fv)):
                        out[col] = s.fillna(fv)
                        _record_fill(changes, col, f"mean={_safe(fv):.4g}", n_null, n_null)
                else:
                    out[col] = s.fillna("Unknown")
                    _record_fill(changes, col, '"Unknown"', n_null, n_null)

    rows_after, cols_after = out.shape
    remaining = int(out.isna().sum().sum())
    log.info("clean_missing  strategy=%s  nulls_before=%d  remaining=%d  rows=%d→%d",
             strategy, total_nulls, remaining, rows_before, rows_after)
    return CleanResult(df=out, rows_before=rows_before, rows_after=rows_after,
                       cols_before=cols_before, cols_after=cols_after, changes=changes)


def _fill_mode(df: pd.DataFrame, col: str, changes: list, n_null: int) -> None:
    mode_s = df[col].mode(dropna=True)
    if not len(mode_s):
        return
    fv = mode_s.iloc[0]
    df[col] = df[col].fillna(fv)
    _record_fill(changes, col, f"mode={fv!r}", n_null, n_null)


def _record_fill(changes: list, col: str, method: str, filled: int, total: int) -> None:
    changes.append({
        "operation": "fill_missing",
        "column":    col,
        "method":    method,
        "filled":    filled,
        "detail":    f"Filled {filled}/{total} null(s) in '{col}' using {method}.",
    })


# ══════════════════════════════════════════════════════════════════════════════
#  2.  Drop columns with too many missing values
# ══════════════════════════════════════════════════════════════════════════════

def clean_missing_cols(
    df: pd.DataFrame,
    threshold: float = 0.50,
) -> CleanResult:
    """
    Drop columns where the fraction of null values exceeds *threshold*.

    Parameters
    ----------
    threshold : float  (0–1, default 0.50)
        Columns with  null_count / row_count > threshold  are dropped.
    """
    rows_before, cols_before = df.shape
    changes: list[dict] = []

    null_frac = df.isna().mean()
    drop_cols = [col for col in df.columns if null_frac[col] > threshold]

    out = df.drop(columns=drop_cols)

    for col in drop_cols:
        pct = null_frac[col] * 100
        changes.append({
            "operation": "drop_high_null_column",
            "column":    col,
            "null_pct":  round(pct, 2),
            "threshold": threshold * 100,
            "detail":    (
                f"Dropped column '{col}' — {pct:.1f}% null "
                f"(threshold {threshold * 100:.0f}%)."
            ),
        })

    rows_after, cols_after = out.shape
    log.info("clean_missing_cols  threshold=%.0f%%  dropped=%d  cols=%d→%d",
             threshold * 100, len(drop_cols), cols_before, cols_after)
    return CleanResult(df=out, rows_before=rows_before, rows_after=rows_after,
                       cols_before=cols_before, cols_after=cols_after, changes=changes)


# ══════════════════════════════════════════════════════════════════════════════
#  3.  Duplicate removal (with optional key-column subset)
# ══════════════════════════════════════════════════════════════════════════════

def clean_duplicates(
    df: pd.DataFrame,
    keep:   str | bool      = "first",
    subset: list[str] | None = None,
) -> CleanResult:
    """
    Remove duplicate rows, optionally using only a subset of columns as the key.

    Parameters
    ----------
    keep   : "first" | "last" | False
    subset : list of column names to consider when identifying duplicates.
             None (default) means all columns.
    """
    rows_before, cols_before = df.shape
    changes: list[dict] = []

    # Normalise keep
    if isinstance(keep, str) and keep.lower() == "false":
        keep = False
    elif isinstance(keep, str) and keep not in ("first", "last"):
        keep = "first"

    # Validate subset
    valid_subset: list[str] | None = None
    if subset:
        valid_subset = [c for c in subset if c in df.columns]
        if not valid_subset:
            valid_subset = None

    out = df.drop_duplicates(keep=keep, subset=valid_subset)
    rows_after = len(out)
    removed    = rows_before - rows_after

    if removed:
        key_desc = f"columns {valid_subset}" if valid_subset else "all columns"
        changes.append({
            "operation":     "remove_duplicates",
            "rows_removed":  removed,
            "keep":          str(keep),
            "subset":        valid_subset,
            "detail":        (
                f"Removed {removed} duplicate row(s) "
                f"(key: {key_desc}, keep='{keep}'). "
                f"{rows_after} rows remain."
            ),
        })

    log.info("clean_duplicates  removed=%d  keep=%s  subset=%s  rows=%d→%d",
             removed, keep, valid_subset, rows_before, rows_after)
    return CleanResult(df=out, rows_before=rows_before, rows_after=rows_after,
                       cols_before=cols_before, cols_after=cols_before, changes=changes)


# ══════════════════════════════════════════════════════════════════════════════
#  4.  Outlier treatment (IQR + Z-score, clip or drop)
# ══════════════════════════════════════════════════════════════════════════════

def clean_outliers(
    df: pd.DataFrame,
    method:    str   = "iqr",
    threshold: float = 1.5,
    action:    str   = "clip",
    columns:   list[str] | None = None,
) -> CleanResult:
    """
    Detect and treat outliers in numeric columns.

    Methods
    -------
    iqr    – Inter-Quartile Range  (Q1 - k·IQR, Q3 + k·IQR)
    zscore – Z-score               (|z| > threshold)

    Actions
    -------
    clip   – clip values to the computed fence (no rows removed)
    drop   – drop rows that contain at least one outlier value

    Parameters
    ----------
    columns : optional list of columns to check.  None → all numeric columns.
    """
    method = method.lower()
    if method not in ("iqr", "zscore"):
        method = "iqr"
    action = action.lower()
    if action not in ("clip", "drop"):
        action = "clip"

    rows_before, cols_before = df.shape
    out     = df.copy()
    changes: list[dict] = []

    # Determine which columns to inspect
    target_cols = columns if columns else list(df.columns)
    outlier_mask = pd.Series(False, index=out.index)

    for col in target_cols:
        if col not in out.columns:
            continue
        s = out[col]
        if not _is_true_numeric(s):
            continue

        num = s.dropna().astype(float)
        if len(num) < 4:
            continue

        if method == "iqr":
            q1, q3 = float(num.quantile(0.25)), float(num.quantile(0.75))
            iqr    = q3 - q1
            if iqr == 0:
                continue
            lo, hi = q1 - threshold * iqr, q3 + threshold * iqr
        else:  # zscore
            mu, std = float(num.mean()), float(num.std())
            if std == 0:
                continue
            lo, hi = mu - threshold * std, mu + threshold * std

        col_mask = s.notna() & ((s < lo) | (s > hi))
        n_out    = int(col_mask.sum())
        if n_out == 0:
            continue

        outlier_mask = outlier_mask | col_mask

        if action == "clip":
            out[col] = s.clip(lower=lo, upper=hi)
            changes.append({
                "operation": "clip_outliers",
                "column":    col,
                "method":    method,
                "threshold": threshold,
                "lower":     _safe(lo),
                "upper":     _safe(hi),
                "outliers":  n_out,
                "detail":    (
                    f"Clipped {n_out} outlier(s) in '{col}' "
                    f"to [{_safe(lo):.4g}, {_safe(hi):.4g}] "
                    f"({method}, k={threshold})."
                ),
            })
        else:
            changes.append({
                "operation": "mark_outliers_for_drop",
                "column":    col,
                "outliers":  n_out,
                "detail":    f"Marked {n_out} outlier(s) in '{col}' for removal.",
            })

    if action == "drop" and outlier_mask.any():
        n_drop = int(outlier_mask.sum())
        out    = out[~outlier_mask]
        changes.append({
            "operation":    "drop_outlier_rows",
            "rows_dropped": n_drop,
            "detail":       f"Dropped {n_drop} row(s) containing outliers.",
        })

    rows_after = len(out)
    log.info("clean_outliers  method=%s  threshold=%s  action=%s  rows=%d→%d",
             method, threshold, action, rows_before, rows_after)
    return CleanResult(df=out, rows_before=rows_before, rows_after=rows_after,
                       cols_before=cols_before, cols_after=cols_before, changes=changes)


# ══════════════════════════════════════════════════════════════════════════════
#  5.  Data-type correction
# ══════════════════════════════════════════════════════════════════════════════

def clean_types(df: pd.DataFrame) -> CleanResult:
    """
    Re-run type inference on all columns and apply safe coercions.
    Strings that look like numbers are coerced to float64.
    Strings that look like dates are coerced to datetime64.
    Low-cardinality strings become Categorical.
    Boolean-looking strings become nullable boolean.
    """
    rows_before, cols_before = df.shape
    result  = infer_and_coerce(df)
    changes = [
        {
            "operation":  "coerce_dtype",
            "column":     c["column"],
            "from_dtype": c["from_dtype"],
            "to_dtype":   c["to_dtype"],
            "detail":     (
                f"Column '{c['column']}' coerced "
                f"from {c['from_dtype']} → {c['to_dtype']}."
            ),
        }
        for c in result.corrections
    ]
    rows_after, cols_after = result.df.shape
    log.info("clean_types  corrections=%d", len(changes))
    return CleanResult(df=result.df, rows_before=rows_before, rows_after=rows_after,
                       cols_before=cols_before, cols_after=cols_after, changes=changes)


# ══════════════════════════════════════════════════════════════════════════════
#  6.  Normalisation (whitespace, case, regex)
# ══════════════════════════════════════════════════════════════════════════════

# Supported normalisation operations (order matters when chaining)
NORMALIZE_OPS = (
    "trim",          # strip leading/trailing whitespace
    "lower",         # lowercase
    "upper",         # uppercase
    "title",         # title-case
    "strip_punct",   # remove punctuation characters
    "collapse_ws",   # collapse multiple spaces/tabs to single space
    "strip_digits",  # remove digit characters
)


def clean_normalize(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    ops: list[str] | None     = None,
) -> CleanResult:
    """
    Apply string-normalisation operations to text/categorical columns.

    Parameters
    ----------
    columns : list of column names to normalise.
              None → every string-like column in the DataFrame.
    ops     : ordered list of operation names from NORMALIZE_OPS.
              None → ["trim", "collapse_ws"] (safe, non-destructive defaults).

    Supported ops
    -------------
    trim         – strip leading and trailing whitespace
    lower        – convert to lowercase
    upper        – convert to uppercase
    title        – convert to title case
    strip_punct  – remove all punctuation (keeps alphanumeric + space)
    collapse_ws  – replace runs of whitespace with a single space
    strip_digits – remove numeric digits

    Returns
    -------
    CleanResult with one change entry per (column, op) combination that
    actually modified at least one cell.
    """
    if ops is None:
        ops = ["trim", "collapse_ws"]

    # Validate ops
    valid_ops = [o for o in ops if o in NORMALIZE_OPS]
    if not valid_ops:
        valid_ops = ["trim"]

    rows_before, cols_before = df.shape
    out     = df.copy()
    changes: list[dict] = []

    # Determine target columns
    target_cols: list[str] = []
    if columns:
        target_cols = [c for c in columns if c in out.columns]
    else:
        target_cols = [c for c in out.columns if _is_string_col(out[c])]

    for col in target_cols:
        s = out[col]
        if not _is_string_col(s):
            continue

        # Work on a plain object Series for all string ops
        working = s.astype(object)

        for op in valid_ops:
            before = working.copy()

            if op == "trim":
                working = working.str.strip()
            elif op == "lower":
                working = working.str.lower()
            elif op == "upper":
                working = working.str.upper()
            elif op == "title":
                working = working.str.title()
            elif op == "strip_punct":
                working = working.str.replace(r"[^\w\s]", "", regex=True)
            elif op == "collapse_ws":
                working = working.str.replace(r"\s+", " ", regex=True).str.strip()
            elif op == "strip_digits":
                working = working.str.replace(r"\d", "", regex=True)

            # Count cells that actually changed (ignoring NaN)
            changed_mask = (
                working.notna() & before.notna() & (working != before)
            )
            n_changed = int(changed_mask.sum())
            if n_changed > 0:
                changes.append({
                    "operation": "normalize",
                    "column":    col,
                    "op":        op,
                    "cells":     n_changed,
                    "detail":    (
                        f"Applied '{op}' to '{col}' — "
                        f"{n_changed} cell(s) modified."
                    ),
                })

        # Write back — try to preserve original dtype when safe
        try:
            if hasattr(s.dtype, "name") and s.dtype.name in ("str", "string"):
                out[col] = working.astype("string")
            else:
                out[col] = working
        except Exception:
            out[col] = working

    rows_after, cols_after = out.shape
    log.info("clean_normalize  ops=%s  cols=%d  changes=%d",
             valid_ops, len(target_cols), len(changes))
    return CleanResult(df=out, rows_before=rows_before, rows_after=rows_after,
                       cols_before=cols_before, cols_after=cols_after, changes=changes)


# ══════════════════════════════════════════════════════════════════════════════
#  7.  Pipeline chaining — apply multiple operations in sequence
# ══════════════════════════════════════════════════════════════════════════════

# Registry mapping step names → (function, allowed_kwargs)
_STEP_REGISTRY: dict[str, tuple] = {
    "normalize":    (clean_normalize,    ("columns", "ops")),
    "missing":      (clean_missing,      ("strategy",)),
    "missing_cols": (clean_missing_cols, ("threshold",)),
    "duplicates":   (clean_duplicates,   ("keep", "subset")),
    "outliers":     (clean_outliers,     ("method", "threshold", "action", "columns")),
    "types":        (clean_types,        ()),
}


def clean_pipeline(
    df: pd.DataFrame,
    steps: list[dict],
) -> CleanResult:
    """
    Apply a sequence of cleaning operations defined by *steps*.

    Each step is a dict:
        { "op": "<step_name>", <kwargs> ... }

    Supported step names (and their kwargs) come from _STEP_REGISTRY above.

    Example
    -------
    steps = [
        {"op": "normalize", "ops": ["trim", "lower"]},
        {"op": "missing",   "strategy": "mean"},
        {"op": "duplicates","keep": "first"},
        {"op": "outliers",  "method": "iqr", "threshold": 1.5, "action": "clip"},
        {"op": "types"},
    ]

    Returns
    -------
    A single merged CleanResult whose `df` is the output of the final step.
    The `changes` list concatenates changes from every step in order.
    Each change dict has an extra `step_index` key for traceability.
    """
    if not steps:
        rows, cols = df.shape
        return CleanResult(df=df.copy(), rows_before=rows, rows_after=rows,
                           cols_before=cols, cols_after=cols)

    rows_before, cols_before = df.shape
    all_changes: list[dict]  = []
    current = df.copy()

    for idx, step in enumerate(steps):
        op_name = step.get("op", "")
        if op_name not in _STEP_REGISTRY:
            log.warning("pipeline step %d: unknown op '%s' — skipped", idx, op_name)
            continue

        fn, allowed_kw = _STEP_REGISTRY[op_name]

        # Extract only allowed kwargs for this function
        kwargs = {k: v for k, v in step.items() if k in allowed_kw}

        try:
            result = fn(current, **kwargs)
        except Exception as exc:
            log.error("pipeline step %d (%s) failed: %s", idx, op_name, exc)
            continue

        # Tag each change with its pipeline position
        for ch in result.changes:
            ch["step_index"] = idx
            ch["step_op"]    = op_name

        all_changes.extend(result.changes)
        current = result.df

        log.debug("pipeline step %d (%s) — rows=%d→%d  changes=%d",
                  idx, op_name, result.rows_before, result.rows_after,
                  len(result.changes))

    rows_after, cols_after = current.shape
    log.info("clean_pipeline  steps=%d  rows=%d→%d  total_changes=%d",
             len(steps), rows_before, rows_after, len(all_changes))
    return CleanResult(df=current, rows_before=rows_before, rows_after=rows_after,
                       cols_before=cols_before, cols_after=cols_after,
                       changes=all_changes)


# ══════════════════════════════════════════════════════════════════════════════
#  8.  Full convenience pipeline (clean_all)
# ══════════════════════════════════════════════════════════════════════════════

def clean_all(
    df: pd.DataFrame,
    missing_strategy:  str   = "mean",
    outlier_method:    str   = "iqr",
    outlier_threshold: float = 1.5,
    outlier_action:    str   = "clip",
    duplicate_keep:    str   = "first",
    normalize:         bool  = True,
    drop_null_cols:    bool  = False,
    null_col_threshold: float = 0.80,
) -> CleanResult:
    """
    Run the standard cleaning pipeline in the recommended order:
        1. Normalisation          (trim + collapse_ws on string cols, if normalize=True)
        2. Drop high-null columns (if drop_null_cols=True)
        3. Type correction
        4. Duplicate removal
        5. Missing-value handling
        6. Outlier treatment
    """
    steps: list[dict] = []

    if normalize:
        steps.append({"op": "normalize", "ops": ["trim", "collapse_ws"]})
    if drop_null_cols:
        steps.append({"op": "missing_cols", "threshold": null_col_threshold})

    steps += [
        {"op": "types"},
        {"op": "duplicates", "keep": duplicate_keep},
        {"op": "missing",    "strategy": missing_strategy},
        {"op": "outliers",   "method": outlier_method,
         "threshold": outlier_threshold, "action": outlier_action},
    ]

    return clean_pipeline(df, steps)