from flask import Blueprint, jsonify, Response
from ..services import runs, formatter
bp = Blueprint("exports", __name__)

@bp.get("/<run_id>/json")
def get_json(run_id):
    data = runs.get(run_id)
    if not data:
        return jsonify({"error": "Run not found"}), 404
    return jsonify(data)

@bp.get("/<run_id>/csv")
def get_csv(run_id):
    data = runs.get(run_id)
    if not data:
        return jsonify({"error": "Run not found"}), 404
    csv_content = formatter.to_csv(data["output"])
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={run_id}.csv"}
    )
