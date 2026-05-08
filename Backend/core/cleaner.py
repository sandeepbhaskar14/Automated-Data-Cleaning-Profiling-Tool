"""
backend/core/cleaner.py
────────────────────────
Data-cleaning engine.  Five public functions map directly to the five
/api/clean/* endpoints:

    clean_missing    (df, strategy)   → CleanResult
    clean_duplicates (df, keep)       → CleanResult
    clean_outliers   (df, method, threshold) → CleanResult
    clean_types      (df)             → CleanResult
    clean_all        (df, **kwargs)   → CleanResult   (runs all four in order)

Each CleanResult carries:
    df           the cleaned DataFrame
    rows_before / rows_after
    cols_before / cols_after
    changes      list[dict]  human-readable description of every change made
    summary      dict  top-level counts for the API response

All values in `changes` and `summary` are plain Python primitives — safe for
flask.jsonify() without further conversion.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from core.logger import get_logger
from core.type_inferrer import infer_and_coerce

log = get_logger(__name__)


# ── Result container ──────────────────────────────────────────────────────────

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


# ── helpers ───────────────────────────────────────────────────────────────────

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
    """True only for genuinely numeric columns — excludes boolean dtypes."""
    if pd.api.types.is_bool_dtype(s.dtype):
        return False
    if hasattr(s.dtype, "name") and s.dtype.name == "boolean":
        return False
    return pd.api.types.is_numeric_dtype(s.dtype)


# ══════════════════════════════════════════════════════════════════════════════
#  1.  Missing-value handling
# ══════════════════════════════════════════════════════════════════════════════

_MISSING_STRATEGIES = ("mean", "median", "mode", "drop", "ffill", "bfill", "zero", "unknown")


def clean_missing(
    df: pd.DataFrame,
    strategy: str = "mean",
) -> CleanResult:
    """
    Handle missing values across all columns.

    Strategies
    ----------
    mean    – fill numeric columns with column mean;     non-numeric → mode
    median  – fill numeric columns with column median;   non-numeric → mode
    mode    – fill every column with its mode (first)
    drop    – drop every row that contains at least one null
    ffill   – forward-fill
    bfill   – backward-fill
    zero    – fill numeric with 0, non-numeric with empty string ""
    unknown – fill non-numeric with literal string "Unknown"

    Returns
    -------
    CleanResult
    """
    strategy = strategy.lower()
    if strategy not in _MISSING_STRATEGIES:
        strategy = "mean"

    rows_before, cols_before = df.shape
    out     = df.copy()
    changes: list[dict] = []

    # Count nulls per column before filling
    null_counts = out.isna().sum()
    total_nulls = int(null_counts.sum())

    if strategy == "drop":
        out = out.dropna()
        dropped = rows_before - len(out)
        if dropped:
            changes.append({
                "operation": "drop_rows_with_nulls",
                "rows_dropped": dropped,
                "detail": f"Dropped {dropped} row(s) containing at least one null value.",
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
                    fill_val = (s.mean() if strategy == "mean" else s.median())
                    if fill_val is not None and not (
                        isinstance(fill_val, float) and math.isnan(fill_val)
                    ):
                        out[col] = s.fillna(fill_val)
                        _record_fill(changes, col, f"{strategy}={_safe(fill_val):.4g}",
                                     n_null, n_null)
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
                    fill_val = s.mean()
                    if fill_val is not None and not (
                        isinstance(fill_val, float) and math.isnan(fill_val)
                    ):
                        out[col] = s.fillna(fill_val)
                        _record_fill(changes, col, f"mean={_safe(fill_val):.4g}",
                                     n_null, n_null)
                else:
                    out[col] = s.fillna("Unknown")
                    _record_fill(changes, col, '"Unknown"', n_null, n_null)

    rows_after, cols_after = out.shape
    remaining = int(out.isna().sum().sum())
    log.info(
        "clean_missing  strategy=%s  nulls_before=%d  remaining=%d  rows=%d→%d",
        strategy, total_nulls, remaining, rows_before, rows_after,
    )
    return CleanResult(
        df=out,
        rows_before=rows_before, rows_after=rows_after,
        cols_before=cols_before, cols_after=cols_after,
        changes=changes,
    )


def _fill_mode(df: pd.DataFrame, col: str, changes: list, n_null: int) -> None:
    mode_s = df[col].mode(dropna=True)
    if len(mode_s) == 0:
        return
    fill_val = mode_s.iloc[0]
    df[col]  = df[col].fillna(fill_val)
    _record_fill(changes, col, f"mode={fill_val!r}", n_null, n_null)


def _record_fill(
    changes: list, col: str, method: str, filled: int, total: int
) -> None:
    changes.append({
        "operation": "fill_missing",
        "column":    col,
        "method":    method,
        "filled":    filled,
        "detail":    f"Filled {filled}/{total} null(s) in '{col}' using {method}.",
    })


# ══════════════════════════════════════════════════════════════════════════════
#  2.  Duplicate removal
# ══════════════════════════════════════════════════════════════════════════════

_KEEP_OPTIONS = ("first", "last", False)


def clean_duplicates(
    df: pd.DataFrame,
    keep: str | bool = "first",
) -> CleanResult:
    """
    Remove duplicate rows.

    Parameters
    ----------
    keep : "first" | "last" | False
        Which occurrence to keep.  False removes *all* duplicates.
    """
    rows_before, cols_before = df.shape
    changes: list[dict] = []

    # Normalise keep
    if isinstance(keep, str) and keep.lower() == "false":
        keep = False
    elif isinstance(keep, str) and keep not in ("first", "last"):
        keep = "first"

    n_dupes = int(df.duplicated(keep=keep).sum()) if keep is not False \
              else int(df.duplicated().sum())

    out = df.drop_duplicates(keep=keep)
    rows_after = len(out)
    removed    = rows_before - rows_after

    if removed:
        changes.append({
            "operation":     "remove_duplicates",
            "rows_removed":  removed,
            "keep":          str(keep),
            "detail":        (
                f"Removed {removed} duplicate row(s)  "
                f"(keep='{keep}').  {rows_after} rows remain."
            ),
        })

    log.info("clean_duplicates  removed=%d  keep=%s  rows=%d→%d",
             removed, keep, rows_before, rows_after)
    return CleanResult(
        df=out,
        rows_before=rows_before, rows_after=rows_after,
        cols_before=cols_before, cols_after=cols_before,
        changes=changes,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  3.  Outlier treatment
# ══════════════════════════════════════════════════════════════════════════════

def clean_outliers(
    df: pd.DataFrame,
    method: str     = "iqr",
    threshold: float = 1.5,
    action: str     = "clip",
) -> CleanResult:
    """
    Detect and treat outliers in numeric columns.

    Methods
    -------
    iqr    – Inter-Quartile Range  (Q1 - k·IQR, Q3 + k·IQR)
    zscore – Z-score               (|z| > threshold)

    Actions
    -------
    clip   – clip values to the fence  (default, no rows lost)
    drop   – drop rows containing any outlier

    Parameters
    ----------
    threshold : float
        IQR multiplier (default 1.5)  OR  Z-score threshold (default 3.0
        when method="zscore").
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

    outlier_mask = pd.Series(False, index=out.index)

    for col in out.columns:
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
            lo = q1 - threshold * iqr
            hi = q3 + threshold * iqr
        else:  # zscore
            mu  = float(num.mean())
            std = float(num.std())
            if std == 0:
                continue
            lo = mu - threshold * std
            hi = mu + threshold * std

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
    return CleanResult(
        df=out,
        rows_before=rows_before, rows_after=rows_after,
        cols_before=cols_before, cols_after=cols_before,
        changes=changes,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  4.  Data-type correction
# ══════════════════════════════════════════════════════════════════════════════

def clean_types(df: pd.DataFrame) -> CleanResult:
    """
    Re-run type inference and apply safe coercions to all columns.
    Wraps core.type_inferrer.infer_and_coerce() and formats the result
    into a CleanResult.
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
    return CleanResult(
        df=result.df,
        rows_before=rows_before, rows_after=rows_after,
        cols_before=cols_before, cols_after=cols_after,
        changes=changes,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  5.  Full pipeline
# ══════════════════════════════════════════════════════════════════════════════

def clean_all(
    df: pd.DataFrame,
    missing_strategy: str  = "mean",
    outlier_method:   str  = "iqr",
    outlier_threshold: float = 1.5,
    outlier_action:   str  = "clip",
    duplicate_keep:   str  = "first",
) -> CleanResult:
    """
    Run the full cleaning pipeline in order:
        1. Type correction   (so numeric stats are accurate)
        2. Duplicate removal
        3. Missing-value handling
        4. Outlier treatment

    Returns a single merged CleanResult (df is the final output).
    """
    rows_before, cols_before = df.shape
    all_changes: list[dict]  = []

    r1 = clean_types(df)
    all_changes += r1.changes

    r2 = clean_duplicates(r1.df, keep=duplicate_keep)
    all_changes += r2.changes

    r3 = clean_missing(r2.df, strategy=missing_strategy)
    all_changes += r3.changes

    r4 = clean_outliers(r3.df, method=outlier_method,
                        threshold=outlier_threshold, action=outlier_action)
    all_changes += r4.changes

    rows_after, cols_after = r4.df.shape
    log.info(
        "clean_all  pipeline complete  rows=%d→%d  cols=%d→%d  changes=%d",
        rows_before, rows_after, cols_before, cols_after, len(all_changes),
    )
    return CleanResult(
        df=r4.df,
        rows_before=rows_before, rows_after=rows_after,
        cols_before=cols_before, cols_after=cols_after,
        changes=all_changes,
    )