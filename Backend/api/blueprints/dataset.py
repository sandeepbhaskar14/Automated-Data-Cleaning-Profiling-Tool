'''
POST   /api/dataset/upload
GET    /api/dataset/<id>/info
DELETE /api/dataset/<id>
'''

from flask import Blueprint, jsonify
from core.logger import get_logger

log = get_logger(__name__)
dataset_bp = Blueprint("dataset", __name__)

def _stub(method, route, **kw):
    log.info("%s /api/dataset/%s — stub", method, route)
    return jsonify({"status": "stub", "message": "Coming in Phase 2.", **kw}), 501

@dataset_bp.post("/upload")
def upload():
    return _stub("POST", "upload")

@dataset_bp.get("/<dataset_id>/info")
def info(dataset_id):
    return _stub("GET", f"{dataset_id}/info", dataset_id=dataset_id)

@dataset_bp.delete("/<dataset_id>")
def delete(dataset_id):
    return _stub("DELETE", dataset_id, dataset_id=dataset_id)