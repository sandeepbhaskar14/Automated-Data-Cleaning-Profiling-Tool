"""
backend/core/
─────────────
Business-logic layer — import from here for clean, stable public API.

Modules
-------
logger.py        – rotating file + coloured console logging
session.py       – thread-safe in-memory DataFrame store (session_store singleton)
loader.py        – file ingestion: CSV, TSV, Excel, JSON, Parquet  →  (df, meta)
type_inferrer.py – auto dtype inference + safe coercion            →  InferenceResult
profiler.py      – statistical profiling: summary / columns / quality
cleaner.py       – data cleaning: missing values, duplicates, outliers, types
"""

# Expose the most-used symbols at package level so callers can write:
#   from core import session_store, load_file, infer_and_coerce, profiler, cleaner
from core.session       import session_store          # noqa: F401
from core.loader        import load_file, LoadError   # noqa: F401
from core.type_inferrer import infer_and_coerce       # noqa: F401
from core               import profiler               # noqa: F401
from core               import cleaner                # noqa: F401