"""
backend/core/session.py
────────────────────────
Thread-safe, in-process store for staged DataFrames.

Each uploaded file is assigned a UUID (dataset_id).  The DataFrame, its
original filename, and the loader meta dict are held in memory for the
lifetime of the server process.  All public methods are safe to call
from Flask's multi-threaded workers.

Usage
-----
    from core.session import session_store

    session_store.put(dataset_id, df, filename, meta)
    entry = session_store.get(dataset_id)   # → SessionEntry | None
    session_store.delete(dataset_id)
    ids   = session_store.list_ids()
"""

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd

from core.logger import get_logger

log = get_logger(__name__)


@dataclass
class SessionEntry:
    dataset_id:  str
    filename:    str
    df:          pd.DataFrame
    meta:        dict          = field(default_factory=dict)   # loader metadata
    uploaded_at: datetime      = field(default_factory=datetime.utcnow)

    @property
    def shape(self) -> tuple[int, int]:
        return self.df.shape


class _SessionStore:
    """Singleton store — access via module-level ``session_store``."""

    def __init__(self) -> None:
        self._lock: threading.Lock           = threading.Lock()
        self._data: dict[str, SessionEntry]  = {}

    # ── write ─────────────────────────────────────────────────────────────────

    def new_id(self) -> str:
        """Generate a fresh UUID guaranteed not to collide with existing keys."""
        while True:
            candidate = str(uuid.uuid4())
            with self._lock:
                if candidate not in self._data:
                    return candidate

    def put(
        self,
        dataset_id: str,
        df: pd.DataFrame,
        filename: str,
        meta: dict | None = None,
    ) -> None:
        entry = SessionEntry(
            dataset_id  = dataset_id,
            df          = df,
            filename    = filename,
            meta        = meta or {},
        )
        with self._lock:
            self._data[dataset_id] = entry
        log.debug("SessionStore.put  id=%s  shape=%s  file=%s",
                  dataset_id, df.shape, filename)

    # ── read ──────────────────────────────────────────────────────────────────

    def get(self, dataset_id: str) -> SessionEntry | None:
        with self._lock:
            return self._data.get(dataset_id)

    def list_ids(self) -> list[str]:
        with self._lock:
            return list(self._data.keys())

    # ── delete ────────────────────────────────────────────────────────────────

    def delete(self, dataset_id: str) -> bool:
        """Return True if the entry existed and was removed."""
        with self._lock:
            existed = dataset_id in self._data
            if existed:
                del self._data[dataset_id]
        log.debug("SessionStore.delete  id=%s  existed=%s", dataset_id, existed)
        return existed

    def __len__(self) -> int:
        with self._lock:
            return len(self._data)


# Module-level singleton — import this object everywhere
session_store = _SessionStore()