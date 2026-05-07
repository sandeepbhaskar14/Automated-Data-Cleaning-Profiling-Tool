'''/api/report/*

POST /<dataset_id>/generate
GET  /<report_id>/download
GET  /list
'''


from flask import Blueprint, jsonify
from core.logger import get_logger

log = get_logger(__name__)
report_bp = Blueprint("report", __name__)

@report_bp.post("/<dataset_id>/generate")
def generate(dataset_id):
    log.info("POST /api/report/%s/generate — stub", dataset_id)
    return jsonify({"status": "stub", "message": "Coming in Phase 3."}), 501

@report_bp.get("/<report_id>/download")
def download(report_id):
    log.info("GET /api/report/%s/download — stub", report_id)
    return jsonify({"status": "stub", "message": "Coming in Phase 3."}), 501

@report_bp.get("/list")
def list_reports():
    log.info("GET /api/report/list — stub")
    return jsonify({
        "status": "stub",
        "reports": [],
        "message": "Coming in Phase 3."
    }), 501