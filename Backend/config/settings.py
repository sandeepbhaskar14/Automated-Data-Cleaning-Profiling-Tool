"""
backend/config/settings.py
───────────────────────────
All configuration for the Flask backend.
Values can be overridden via backend/.env
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent   # → backend/
LOG_DIR    = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports" / "output"
UPLOAD_DIR = BASE_DIR / "uploads"

for _d in (LOG_DIR, REPORT_DIR, UPLOAD_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ── Environment ────────────────────────────────────────────────────────────────
load_dotenv(BASE_DIR / ".env")

# ── Flask ──────────────────────────────────────────────────────────────────────
FLASK_HOST  = os.getenv("FLASK_HOST",  "0.0.0.0")   # 0.0.0.0 for deployed servers
FLASK_PORT  = int(os.getenv("FLASK_PORT", "5050"))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
SECRET_KEY  = os.getenv("SECRET_KEY",  "dev-secret-change-in-prod")

# CORS — which origins are allowed to call the API
#   development : http://localhost:*
#   production  : set CORS_ORIGINS=https://your-domain.com in .env
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

# ── Logging ────────────────────────────────────────────────────────────────────
LOG_LEVEL        = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_MAX_BYTES    = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 3

# ── Data Cleaning Defaults ────────────────────────────────────────────────────
MISSING_VALUE_STRATEGY = "mean"    # mean | median | mode | drop | ffill
OUTLIER_METHOD         = "iqr"     # iqr | zscore
OUTLIER_THRESHOLD      = 1.5
DUPLICATE_KEEP         = "first"   # first | last | False
MAX_UPLOAD_MB          = 50

# ── Quality Score Thresholds ──────────────────────────────────────────────────
QUALITY_EXCELLENT = 90
QUALITY_GOOD      = 75
QUALITY_FAIR      = 50

# ── App Meta ──────────────────────────────────────────────────────────────────
APP_NAME    = "Automated Data Cleaning & Profiling Tool"
APP_VERSION = "1.0.0"

# ── Supported File Types ──────────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = (".csv", ".xlsx", ".xls", ".tsv", ".parquet")