"""
shared/constants.py
────────────────────
Values that both the backend and the frontend need to agree on.

How each side imports this
──────────────────────────
Backend  (run from backend/):
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from shared.constants import APP_NAME           # ← done once in backend/run.py

Frontend (run from frontend/):
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from shared.constants import APP_NAME           # ← done once in frontend/main.py

Every other module inside backend/ or frontend/ can then just write:
    from shared.constants import APP_NAME
because the project root is already on sys.path.
"""

# ── Application identity ──────────────────────────────────────────────────────
APP_NAME    = "Automated Data Cleaning & Profiling Tool"
APP_VERSION = "1.0.0"

# ── Supported dataset file extensions ────────────────────────────────────────
SUPPORTED_EXTENSIONS = (".csv", ".xlsx", ".xls", ".tsv", ".parquet")

# ── Data-quality score bands ──────────────────────────────────────────────────
# Used by backend scorer AND frontend colour/label logic — must match exactly.
QUALITY_EXCELLENT = 90   # ≥ 90  → "Excellent"  (green)
QUALITY_GOOD      = 75   # ≥ 75  → "Good"        (teal)
QUALITY_FAIR      = 50   # ≥ 50  → "Fair"        (orange)
                          # <  50  → "Poor"        (red)

# ── API route prefixes ────────────────────────────────────────────────────────
# Kept here so the frontend ApiClient and the backend blueprint registration
# can never drift out of sync.
ROUTE_HEALTH  = "/api/health"
ROUTE_DATASET = "/api/dataset"
ROUTE_CLEAN   = "/api/clean"
ROUTE_PROFILE = "/api/profile"
ROUTE_REPORT  = "/api/report"