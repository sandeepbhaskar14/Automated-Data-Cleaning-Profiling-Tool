"""
backend/run.py
───────────────
Standalone entry point for the Flask backend server.

Development
-----------
    cd backend/
    python run.py

Production (gunicorn)
---------------------
    cd backend/
    gunicorn "api.app:create_app()" --bind 0.0.0.0:5050 --workers 4

Docker
------
    WORKDIR /app/backend
    CMD ["gunicorn", "api.app:create_app()", "--bind", "0.0.0.0:5050"]

sys.path contract
-----------------
Adds TWO directories before any application import:
  1. <project_root>/backend/  → "from config…", "from core…", "from api…"
  2. <project_root>/          → "from shared.constants import …"
No other file in backend/ touches sys.path.
"""

import sys
from pathlib import Path

_BACKEND_DIR = Path(__file__).resolve().parent          # …/backend/
_PROJECT_DIR = _BACKEND_DIR.parent                      # …/ (project root)

sys.path.insert(0, str(_BACKEND_DIR))
sys.path.insert(0, str(_PROJECT_DIR))

# ── All application imports below this line ───────────────────────────────────
from config.settings import FLASK_HOST, FLASK_PORT, FLASK_DEBUG
from core.logger import get_logger
from api.app import create_app

log = get_logger(__name__)

if __name__ == "__main__":
    app = create_app()
    log.info(
        "Backend starting  http://%s:%d  (debug=%s)",
        FLASK_HOST, FLASK_PORT, FLASK_DEBUG,
    )
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=True,
        use_reloader=True,
    )