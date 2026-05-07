'''/api/profile/<dataset_id>/*

GET summary | columns | quality
'''


from flask import Blueprint, jsonify
from core.logger import get_logger

log = get_logger(__name__)
profile_bp = Blueprint("profile", __name__)

def _stub(ep, dataset_id):
    log.info("GET /api/profile/%s/%s — stub", dataset_id, ep)
    return jsonify({
        "status": "stub",
        "endpoint": ep,
        "dataset_id": dataset_id,
        "message": "Coming in Phase 2."
    }), 501

@profile_bp.get("/<dataset_id>/summary")
def summary(dataset_id):
    return _stub("summary", dataset_id)

@profile_bp.get("/<dataset_id>/columns")
def columns(dataset_id):
    return _stub("columns", dataset_id)

@profile_bp.get("/<dataset_id>/quality")
def quality(dataset_id):
    return _stub("quality", dataset_id)