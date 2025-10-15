from flask import Blueprint, jsonify
import time

bp = Blueprint("health", __name__)
start_time = time.time()

@bp.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "uptime_sec": round(time.time() - start_time, 2),
        "service": "checkout-backend-api"
    })
