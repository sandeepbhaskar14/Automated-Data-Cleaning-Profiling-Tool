"""
backend/core/loader.py
───────────────────────
File ingestion layer — the single entry-point for turning an uploaded file
into a pandas DataFrame.

Supported formats
─────────────────
  .csv   .tsv   .xlsx   .xls   .json   .parquet

Usage
-----
    from core.loader import load_file, LoadError
    df, meta = load_file(raw_bytes, original_filename="sales.csv")

Returns
-------
    df   : pd.DataFrame  – the raw, unmodified frame
    meta : dict          – {filename, extension, size_bytes, rows, cols, …format-specific}
"""

from __future__ import annotations

import io
import json
from pathlib import Path

import chardet
import pandas as pd

from core.logger import get_logger
from shared.constants import SUPPORTED_EXTENSIONS

log = get_logger(__name__)

# MAX_UPLOAD_MB is backend-specific; read from config so it stays overrideable
try:
    from config.settings import MAX_UPLOAD_MB
except ImportError:
    MAX_UPLOAD_MB = 50

_MAX_BYTES = MAX_UPLOAD_MB * 1024 * 1024


# ── exception ─────────────────────────────────────────────────────────────────

class LoadError(Exception):
    """Raised when a file cannot be ingested (bad format, too large, parse error)."""


# ── public entry point ────────────────────────────────────────────────────────

def load_file(
    source: bytes | str | Path,
    original_filename: str,
) -> tuple[pd.DataFrame, dict]:
    """
    Load *source* into a DataFrame.

    Parameters
    ----------
    source            : raw bytes from a Flask upload, or a filesystem path
    original_filename : original filename including extension (.csv, .xlsx …)

    Returns
    -------
    (df, meta)  where meta is a plain dict safe to JSON-serialise
    """
    ext = Path(original_filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise LoadError(
            f"Unsupported file type '{ext}'.  "
            f"Allowed: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    # Normalise to bytes
    if isinstance(source, (str, Path)):
        raw: bytes = Path(source).read_bytes()
    else:
        raw = source

    size_bytes = len(raw)
    if size_bytes > _MAX_BYTES:
        raise LoadError(
            f"File is {size_bytes / 1_048_576:.1f} MB — "
            f"maximum allowed is {MAX_UPLOAD_MB} MB."
        )

    log.debug("load_file  file=%s  ext=%s  size=%d bytes",
              original_filename, ext, size_bytes)

    dispatch = {
        ".csv":     _load_csv,
        ".tsv":     _load_tsv,
        ".xlsx":    _load_excel,
        ".xls":     _load_excel,
        ".json":    _load_json,
        ".parquet": _load_parquet,
    }
    df, extra = dispatch[ext](raw, original_filename)

    meta = {
        "filename":   original_filename,
        "extension":  ext,
        "size_bytes": size_bytes,
        "rows":       int(df.shape[0]),
        "cols":       int(df.shape[1]),
        **extra,
    }
    log.info("Loaded  %s  →  %d rows × %d cols", original_filename,
             df.shape[0], df.shape[1])
    return df, meta


# ── format loaders ────────────────────────────────────────────────────────────

def _detect_encoding(raw: bytes) -> str:
    """Detect byte encoding with chardet; fall back to utf-8."""
    result   = chardet.detect(raw[:50_000])   # sample first 50 KB
    encoding = result.get("encoding") or "utf-8"
    log.debug("Detected encoding: %s  confidence=%.2f",
              encoding, result.get("confidence", 0))
    return encoding


def _load_csv(raw: bytes, filename: str) -> tuple[pd.DataFrame, dict]:
    encoding = _detect_encoding(raw)
    try:
        df = pd.read_csv(
            io.BytesIO(raw),
            encoding=encoding,
            low_memory=False,
            on_bad_lines="warn",
        )
    except Exception as exc:
        raise LoadError(f"Could not parse CSV '{filename}': {exc}") from exc
    return df, {"encoding": encoding}


def _load_tsv(raw: bytes, filename: str) -> tuple[pd.DataFrame, dict]:
    encoding = _detect_encoding(raw)
    try:
        df = pd.read_csv(
            io.BytesIO(raw),
            sep="\t",
            encoding=encoding,
            low_memory=False,
            on_bad_lines="warn",
        )
    except Exception as exc:
        raise LoadError(f"Could not parse TSV '{filename}': {exc}") from exc
    return df, {"encoding": encoding}


def _load_excel(raw: bytes, filename: str) -> tuple[pd.DataFrame, dict]:
    try:
        xls         = pd.ExcelFile(io.BytesIO(raw))
        sheet_names = xls.sheet_names
        df          = pd.read_excel(io.BytesIO(raw), sheet_name=0)
    except Exception as exc:
        raise LoadError(f"Could not parse Excel file '{filename}': {exc}") from exc
    return df, {"sheet_names": sheet_names, "active_sheet": sheet_names[0]}


def _load_json(raw: bytes, filename: str) -> tuple[pd.DataFrame, dict]:
    encoding = _detect_encoding(raw)
    try:
        text   = raw.decode(encoding)
        parsed = json.loads(text)

        if isinstance(parsed, list):
            df     = pd.DataFrame(parsed)
            orient = "records"
        elif isinstance(parsed, dict):
            # Handles pandas split / columns / index orient dicts
            df     = pd.read_json(io.BytesIO(raw))
            orient = "object"
        else:
            raise LoadError(
                f"JSON root must be an array or object, "
                f"got {type(parsed).__name__}."
            )
    except LoadError:
        raise
    except Exception as exc:
        raise LoadError(f"Could not parse JSON '{filename}': {exc}") from exc
    return df, {"encoding": encoding, "json_orient": orient}


def _load_parquet(raw: bytes, filename: str) -> tuple[pd.DataFrame, dict]:
    try:
        df = pd.read_parquet(io.BytesIO(raw))
    except Exception as exc:
        raise LoadError(f"Could not parse Parquet file '{filename}': {exc}") from exc
    return df, {}