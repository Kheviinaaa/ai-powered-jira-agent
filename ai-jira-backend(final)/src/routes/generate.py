from flask import Blueprint, request, jsonify
import uuid
import json
import os

bp = Blueprint('generate', __name__)

@bp.route('/', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        project_name = data.get('project_name', 'Default Project')
        epics = data.get('epics', [])
        
        run_id = str(uuid.uuid4())
        
        # Simple storage without imports
        run_data = {
            "run_id": run_id,
            "project_name": project_name,
            "epics": epics,
            "output": {
                "stories": [
                    {
                        "epic_id": epic["epic_id"],
                        "stories": [f"Story for {epic['title']}"],
                        "test_cases": [f"Test for {epic['title']}"]
                    }
                    for epic in epics
                ]
            }
        }
        
        # Save directly
        os.makedirs("runs_data", exist_ok=True)
        with open(f"runs_data/{run_id}.json", "w") as f:
            json.dump(run_data, f)
        
        return jsonify({
            "status": "success",
            "run_id": run_id,
            "message": f"Generated {len(epics)} epics"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500