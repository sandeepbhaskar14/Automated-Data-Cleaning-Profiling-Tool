"""
backend/api/blueprints/clean.py
────────────────────────────────

Endpoints
─────────
POST /api/clean/<dataset_id>/missing       – fill / drop missing values (row strategy)
POST /api/clean/<dataset_id>/missing_cols  – drop columns above null threshold
POST /api/clean/<dataset_id>/duplicates    – remove duplicate rows (+ key-column subset)
POST /api/clean/<dataset_id>/outliers      – IQR / Z-score outlier treatment
POST /api/clean/<dataset_id>/types         – auto dtype coercion
POST /api/clean/<dataset_id>/normalize     – whitespace, case, regex normalisation
POST /api/clean/<dataset_id>/pipeline      – chain any sequence of cleaning steps
POST /api/clean/<dataset_id>/run_all       – full convenience pipeline

All endpoints
  • read the staged DataFrame from session_store
  • call the appropriate cleaner.* function
  • write the cleaned DataFrame back into session_store (in-place update)
  • return a structured JSON summary of every change made

Request bodies (all fields optional — defaults come from config/settings.py):

  /missing      { "strategy": "mean"|"median"|"mode"|"drop"|"ffill"|"bfill"|"zero"|"unknown" }
  /missing_cols { "threshold": 0.50 }                        (0–1, fraction of nulls)
  /duplicates   { "keep": "first"|"last"|"false",
                  "subset": ["col1","col2"] }                (null = all columns)
  /outliers     { "method": "iqr"|"zscore", "threshold": 1.5,
                  "action": "clip"|"drop",
                  "columns": ["col1"] }                      (null = all numeric)
  /normalize    { "columns": ["col1"],                       (null = all string cols)
                  "ops": ["trim","lower","collapse_ws",…] }
  /pipeline     { "steps": [{"op":"normalize","ops":["trim"]},
                             {"op":"missing","strategy":"mean"},
                             ...] }
  /run_all      { "missing_strategy", "outlier_method", "outlier_threshold",
                  "outlier_action", "duplicate_keep",
                  "normalize": true, "drop_null_cols": false,
                  "null_col_threshold": 0.80 }
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

log      = get_logger(__name__)
clean_bp = Blueprint("clean", __name__)


# ── helpers ───────────────────────────────────────────────────────────────────

def _get_or_404(dataset_id: str):
    entry = session_store.get(dataset_id)
    if entry is None:
        return None, (jsonify({"error": f"Dataset '{dataset_id}' not found."}), 404)
    return entry, None


def _body() -> dict:
    try:
        d = request.get_json(silent=True)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _save(entry, df) -> None:
    session_store.put(entry.dataset_id, df, entry.filename, entry.meta)


def _resp(dataset_id: str, operation: str, result, **extra) -> tuple:
    payload = {"dataset_id": dataset_id, "operation": operation,
               "summary": result.summary, **extra}
    return jsonify(payload), 200


# ── POST /api/clean/<dataset_id>/missing ─────────────────────────────────────

@clean_bp.post("/<dataset_id>/missing")
def handle_missing(dataset_id: str):
    """Fill or drop missing values (row-level strategy)."""
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    strategy = _body().get("strategy", MISSING_VALUE_STRATEGY)
    result   = cleaner.clean_missing(entry.df, strategy=strategy)
    _save(entry, result.df)

    log.info("clean/missing  id=%s  strategy=%s  rows=%d→%d  changes=%d",
             dataset_id, strategy, result.rows_before, result.rows_after,
             len(result.changes))
    return _resp(dataset_id, "missing", result, strategy=strategy)


# ── POST /api/clean/<dataset_id>/missing_cols ─────────────────────────────────

@clean_bp.post("/<dataset_id>/missing_cols")
def handle_missing_cols(dataset_id: str):
    """Drop columns whose null fraction exceeds threshold."""
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    body      = _body()
    threshold = float(body.get("threshold", 0.50))
    result    = cleaner.clean_missing_cols(entry.df, threshold=threshold)
    _save(entry, result.df)

    log.info("clean/missing_cols  id=%s  threshold=%.0f%%  dropped=%d  cols=%d→%d",
             dataset_id, threshold * 100,
             result.cols_before - result.cols_after,
             result.cols_before, result.cols_after)
    return _resp(dataset_id, "missing_cols", result, threshold=threshold)


# ── POST /api/clean/<dataset_id>/duplicates ───────────────────────────────────

@clean_bp.post("/<dataset_id>/duplicates")
def remove_duplicates(dataset_id: str):
    """Remove duplicate rows, optionally keyed on a column subset."""
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    body   = _body()
    keep   = body.get("keep",   DUPLICATE_KEEP)
    subset = body.get("subset", None)          # list[str] | None

    result = cleaner.clean_duplicates(entry.df, keep=keep, subset=subset)
    _save(entry, result.df)

    log.info("clean/duplicates  id=%s  keep=%s  subset=%s  removed=%d",
             dataset_id, keep, subset,
             result.rows_before - result.rows_after)
    return _resp(dataset_id, "duplicates", result, keep=str(keep), subset=subset)


# ── POST /api/clean/<dataset_id>/outliers ─────────────────────────────────────

@clean_bp.post("/<dataset_id>/outliers")
def treat_outliers(dataset_id: str):
    """Detect and treat outliers in numeric columns."""
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    body      = _body()
    method    = body.get("method",    OUTLIER_METHOD)
    threshold = float(body.get("threshold", OUTLIER_THRESHOLD))
    action    = body.get("action",    "clip")
    columns   = body.get("columns",   None)    # list[str] | None

    result = cleaner.clean_outliers(entry.df, method=method, threshold=threshold,
                                    action=action, columns=columns)
    _save(entry, result.df)

    log.info("clean/outliers  id=%s  method=%s  threshold=%s  action=%s  changes=%d",
             dataset_id, method, threshold, action, len(result.changes))
    return _resp(dataset_id, "outliers", result,
                 method=method, threshold=threshold, action=action)


# ── POST /api/clean/<dataset_id>/types ───────────────────────────────────────

@clean_bp.post("/<dataset_id>/types")
def correct_types(dataset_id: str):
    """Auto-infer and coerce column data types."""
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    result = cleaner.clean_types(entry.df)
    _save(entry, result.df)

    log.info("clean/types  id=%s  corrections=%d", dataset_id, len(result.changes))
    return _resp(dataset_id, "types", result)


# ── POST /api/clean/<dataset_id>/normalize ────────────────────────────────────

@clean_bp.post("/<dataset_id>/normalize")
def normalize(dataset_id: str):
    """
    Normalise string columns: trim whitespace, standardise case, remove
    punctuation/digits, collapse multiple spaces.

    Body
    ----
    {
        "columns": ["col1", "col2"],    // omit → all string cols
        "ops":     ["trim", "lower"]    // omit → ["trim", "collapse_ws"]
    }

    Available ops: trim | lower | upper | title | strip_punct |
                   collapse_ws | strip_digits
    """
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    body    = _body()
    columns = body.get("columns", None)
    ops     = body.get("ops",     None)

    result = cleaner.clean_normalize(entry.df, columns=columns, ops=ops)
    _save(entry, result.df)

    log.info("clean/normalize  id=%s  cols=%s  ops=%s  changes=%d",
             dataset_id, columns, ops, len(result.changes))
    return _resp(dataset_id, "normalize", result, ops=ops)


# ── POST /api/clean/<dataset_id>/pipeline ─────────────────────────────────────

@clean_bp.post("/<dataset_id>/pipeline")
def pipeline(dataset_id: str):
    """
    Execute a user-defined sequence of cleaning operations in one request.

    Body
    ----
    {
        "steps": [
            {"op": "normalize",  "ops": ["trim", "lower"]},
            {"op": "missing",    "strategy": "mean"},
            {"op": "missing_cols","threshold": 0.8},
            {"op": "duplicates", "keep": "first", "subset": ["id"]},
            {"op": "outliers",   "method": "iqr", "threshold": 1.5, "action": "clip"},
            {"op": "types"}
        ]
    }

    Each step's DataFrame output is fed as input to the next step.
    The session store is updated once with the final result.
    """
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    body  = _body()
    steps = body.get("steps", [])

    if not isinstance(steps, list) or not steps:
        return jsonify({"error": "Body must contain a non-empty 'steps' list."}), 400

    result = cleaner.clean_pipeline(entry.df, steps=steps)
    _save(entry, result.df)

    log.info("clean/pipeline  id=%s  steps=%d  rows=%d→%d  changes=%d",
             dataset_id, len(steps), result.rows_before, result.rows_after,
             len(result.changes))
    return _resp(dataset_id, "pipeline", result, n_steps=len(steps))


# ── POST /api/clean/<dataset_id>/run_all ─────────────────────────────────────

@clean_bp.post("/<dataset_id>/run_all")
def run_all(dataset_id: str):
    """
    Convenience endpoint that runs the full recommended cleaning pipeline.

    Body (all optional — falls back to config defaults)
    ----
    {
        "missing_strategy":   "mean",
        "duplicate_keep":     "first",
        "outlier_method":     "iqr",
        "outlier_threshold":  1.5,
        "outlier_action":     "clip",
        "normalize":          true,
        "drop_null_cols":     false,
        "null_col_threshold": 0.80
    }
    """
    entry, err = _get_or_404(dataset_id)
    if err:
        return err

    body   = _body()
    params = {
        "missing_strategy":   body.get("missing_strategy",   MISSING_VALUE_STRATEGY),
        "outlier_method":     body.get("outlier_method",     OUTLIER_METHOD),
        "outlier_threshold":  float(body.get("outlier_threshold", OUTLIER_THRESHOLD)),
        "outlier_action":     body.get("outlier_action",     "clip"),
        "duplicate_keep":     body.get("duplicate_keep",     DUPLICATE_KEEP),
        "normalize":          bool(body.get("normalize",          True)),
        "drop_null_cols":     bool(body.get("drop_null_cols",     False)),
        "null_col_threshold": float(body.get("null_col_threshold", 0.80)),
    }

    result = cleaner.clean_all(entry.df, **params)
    _save(entry, result.df)

    log.info("clean/run_all  id=%s  rows=%d→%d  changes=%d",
             dataset_id, result.rows_before, result.rows_after, len(result.changes))
    return _resp(dataset_id, "run_all", result, params=params)