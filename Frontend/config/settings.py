"""
frontend/config/settings.py
────────────────────────────
All configuration for the PyQt5 desktop frontend.

The frontend knows nothing about backend internals — it only needs API_BASE_URL.
Change that one value (via frontend/.env) to point at any deployed backend.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

_FRONTEND_DIR = Path(__file__).resolve().parent.parent  # …/frontend/
load_dotenv(_FRONTEND_DIR / ".env")

# ── Backend connection ────────────────────────────────────────────────────────
# Override in frontend/.env to point at a remote server.
API_BASE_URL    = os.getenv("API_BASE_URL",   "http://127.0.0.1:5050")
API_TIMEOUT_SEC = int(os.getenv("API_TIMEOUT", "10"))

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_DIR          = _FRONTEND_DIR / "logs"
LOG_LEVEL        = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_MAX_BYTES    = 5 * 1024 * 1024   # 5 MB
LOG_BACKUP_COUNT = 3

LOG_DIR.mkdir(parents=True, exist_ok=True)

# ── Window geometry ───────────────────────────────────────────────────────────
WINDOW_WIDTH           = 1217
WINDOW_HEIGHT          = 718
SIDEBAR_WIDTH          = 75
SIDEBAR_EXPANDED_WIDTH = 275