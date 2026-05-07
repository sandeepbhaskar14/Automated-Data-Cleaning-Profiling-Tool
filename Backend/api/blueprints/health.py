"""
backend/api/blueprints/health.py
──────────────────────────────────
GET /api/health/  →  {"status": "ok", "version": "1.0.0"}

shared.constants is importable because backend/run.py already added the
project root to sys.path before Flask starts.
"""

from flask import Blueprint, jsonify
from shared.constants import APP_VERSION
from core.logger import get_logger

log       = get_logger(__name__)
health_bp = Blueprint("health", __name__)


@health_bp.get("/")
def ping():
    log.debug("Health check")
    return jsonify({"status": "ok", "version": APP_VERSION}), 200