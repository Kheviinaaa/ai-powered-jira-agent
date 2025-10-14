from flask import Blueprint, request, jsonify
from ..services import ai_client, runs
bp = Blueprint("generate", __name__)

@bp.post("")
def from_raw():
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Missing JSON body"}), 400
    try:
        run = ai_client.generate_from_payload(payload)
        runs.store(run)
        return jsonify(run), 200
    except Exception as e:
        return jsonify({"error": "internal", "message": str(e)}), 500
