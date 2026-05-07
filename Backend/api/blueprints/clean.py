'''/api/clean/<dataset_id>/*

POST missing | duplicates | outliers | types | run_all
'''


from flask import Blueprint, jsonify
from core.logger import get_logger

log = get_logger(__name__)
clean_bp = Blueprint("clean", __name__)

def _stub(op, dataset_id):
    log.info("POST /api/clean/%s/%s — stub", dataset_id, op)
    return jsonify({
        "status": "stub",
        "operation": op,
        "dataset_id": dataset_id,
        "message": "Coming in Phase 2."
    }), 501

@clean_bp.post("/<dataset_id>/missing")
def missing(dataset_id):
    return _stub("missing", dataset_id)

@clean_bp.post("/<dataset_id>/duplicates")
def duplicates(dataset_id):
    return _stub("duplicates", dataset_id)

@clean_bp.post("/<dataset_id>/outliers")
def outliers(dataset_id):
    return _stub("outliers", dataset_id)

@clean_bp.post("/<dataset_id>/types")
def types(dataset_id):
    return _stub("types", dataset_id)

@clean_bp.post("/<dataset_id>/run_all")
def run_all(dataset_id):
    return _stub("run_all", dataset_id)
