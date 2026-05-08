"""
backend/api/blueprints/clean.py
────────────────────────────────
POST /api/clean/<dataset_id>/missing      – handle missing values
POST /api/clean/<dataset_id>/duplicates   – remove duplicate rows
POST /api/clean/<dataset_id>/outliers     – treat outliers
POST /api/clean/<dataset_id>/types        – correct data types
POST /api/clean/<dataset_id>/run_all      – full pipeline

All endpoints
  • read the staged DataFrame from session_store
  • run the requested cleaning operation
  • write the cleaned DataFrame back to session_store (in-place update)
  • return a JSON summary of changes made

Request body (JSON, optional per endpoint):

  /missing    { "strategy": "mean"|"median"|"mode"|"drop"|"ffill"|"bfill"|"zero"|"unknown" }
  /duplicates { "keep": "first"|"last"|"false" }
  /outliers   { "method": "iqr"|"zscore", "threshold": 1.5, "action": "clip"|"drop" }
  /run_all    { all of the above, optional }
"""

from flask import Blueprint, jsonify, request

from core.logger  import get_logger
from core.session import session_store
from core import cleaner
from config.settings import (
    MISSING_VALUE_STRATEGY,
    OUTLIER_METHOD,
    OUTLIER_THRESHOLD,
    DUPLICATE_KEEP,
)

log = get_logger(__name__)
clean_bp = Blueprint("clean", __name__)


# ── shared helpers ────────────────────────────────────────────────────────────

def _get_or_404(dataset_id: str):
    entry = session_store.get(dataset_id)
    if entry is None:
        return None, (jsonify({"error": f"Dataset '{dataset_id}' not found."}), 404)
    return entry, None


def _body() -> dict:
    """Return parsed JSON body or empty dict (never raises)."""
    try:
        data = request.get_json(silent=True)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _write_back(entry, df, result) -> None:
    """Persist the cleaned DataFrame back into the session store."""
    session_store.put(entry.dataset_id, df, entry.filename, entry.meta)


# ── POST /api/clean/<dataset_id>/missing ─────────────────────────────────────

@clean_bp.post("/<dataset_id>/missing")
def handle_missing(dataset_id: str):
    """
    Fill or drop missing values.

    Body  { "strategy": "mean" }   (default from settings)

    Returns 200
    -----------
    { dataset_id, operation, summary: {rows_before, rows_after, …, changes} }
    """
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    strategy = _body().get("strategy", MISSING_VALUE_STRATEGY)
    result   = cleaner.clean_missing(entry.df, strategy=strategy)
    _write_back(entry, result.df, result)

    log.info("clean/missing  id=%s  strategy=%s  rows=%d→%d  changes=%d",
             dataset_id, strategy,
             result.rows_before, result.rows_after, len(result.changes))

    return jsonify({
        "dataset_id": dataset_id,
        "operation":  "missing",
        "strategy":   strategy,
        "summary":    result.summary,
    }), 200


# ── POST /api/clean/<dataset_id>/duplicates ───────────────────────────────────

@clean_bp.post("/<dataset_id>/duplicates")
def remove_duplicates(dataset_id: str):
    """
    Remove duplicate rows.

    Body  { "keep": "first" }   (default from settings)

    Returns 200
    -----------
    { dataset_id, operation, summary }
    """
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    keep   = _body().get("keep", DUPLICATE_KEEP)
    result = cleaner.clean_duplicates(entry.df, keep=keep)
    _write_back(entry, result.df, result)

    log.info("clean/duplicates  id=%s  keep=%s  removed=%d",
             dataset_id, keep,
             result.rows_before - result.rows_after)

    return jsonify({
        "dataset_id": dataset_id,
        "operation":  "duplicates",
        "keep":       str(keep),
        "summary":    result.summary,
    }), 200


# ── POST /api/clean/<dataset_id>/outliers ─────────────────────────────────────

@clean_bp.post("/<dataset_id>/outliers")
def treat_outliers(dataset_id: str):
    """
    Detect and treat outliers in numeric columns.

    Body  { "method": "iqr", "threshold": 1.5, "action": "clip" }

    Returns 200
    -----------
    { dataset_id, operation, method, threshold, action, summary }
    """
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    body      = _body()
    method    = body.get("method",    OUTLIER_METHOD)
    threshold = float(body.get("threshold", OUTLIER_THRESHOLD))
    action    = body.get("action",    "clip")

    result = cleaner.clean_outliers(entry.df,
                                    method=method,
                                    threshold=threshold,
                                    action=action)
    _write_back(entry, result.df, result)

    log.info("clean/outliers  id=%s  method=%s  threshold=%s  action=%s  changes=%d",
             dataset_id, method, threshold, action, len(result.changes))

    return jsonify({
        "dataset_id": dataset_id,
        "operation":  "outliers",
        "method":     method,
        "threshold":  threshold,
        "action":     action,
        "summary":    result.summary,
    }), 200


# ── POST /api/clean/<dataset_id>/types ───────────────────────────────────────

@clean_bp.post("/<dataset_id>/types")
def correct_types(dataset_id: str):
    """
    Run auto-type inference and coerce columns to their detected types.

    Body  {}  (no parameters needed)

    Returns 200
    -----------
    { dataset_id, operation, summary }
    """
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    result = cleaner.clean_types(entry.df)
    _write_back(entry, result.df, result)

    log.info("clean/types  id=%s  corrections=%d",
             dataset_id, len(result.changes))

    return jsonify({
        "dataset_id": dataset_id,
        "operation":  "types",
        "summary":    result.summary,
    }), 200


# ── POST /api/clean/<dataset_id>/run_all ─────────────────────────────────────

@clean_bp.post("/<dataset_id>/run_all")
def run_all(dataset_id: str):
    """
    Run the full cleaning pipeline:
        1. type correction → 2. duplicates → 3. missing → 4. outliers

    Body (all optional, fall back to settings defaults)
    ----
    {
        "missing_strategy":  "mean",
        "duplicate_keep":    "first",
        "outlier_method":    "iqr",
        "outlier_threshold": 1.5,
        "outlier_action":    "clip"
    }

    Returns 200
    -----------
    { dataset_id, operation, params, summary }
    """
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    body = _body()
    params = {
        "missing_strategy":  body.get("missing_strategy",  MISSING_VALUE_STRATEGY),
        "outlier_method":    body.get("outlier_method",    OUTLIER_METHOD),
        "outlier_threshold": float(body.get("outlier_threshold", OUTLIER_THRESHOLD)),
        "outlier_action":    body.get("outlier_action",    "clip"),
        "duplicate_keep":    body.get("duplicate_keep",    DUPLICATE_KEEP),
    }

    result = cleaner.clean_all(entry.df, **params)
    _write_back(entry, result.df, result)

    log.info("clean/run_all  id=%s  rows=%d→%d  total_changes=%d",
             dataset_id, result.rows_before, result.rows_after, len(result.changes))

    return jsonify({
        "dataset_id": dataset_id,
        "operation":  "run_all",
        "params":     params,
        "summary":    result.summary,
    }), 200