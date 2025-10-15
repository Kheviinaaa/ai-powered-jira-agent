from flask import Blueprint, jsonify, Response
import json
import os
import csv
import io

bp = Blueprint("exports", __name__)

def to_csv(data):
    """Simple CSV formatter"""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Epic ID', 'Story', 'Test Case'])
    
    for epic_data in data.get('stories', []):
        epic_id = epic_data.get('epic_id', '')
        stories = epic_data.get('stories', [])
        test_cases = epic_data.get('test_cases', [])
        
        max_len = max(len(stories), len(test_cases))
        for i in range(max_len):
            story = stories[i] if i < len(stories) else ''
            test_case = test_cases[i] if i < len(test_cases) else ''
            writer.writerow([epic_id, story, test_case])
    
    return output.getvalue()

@bp.get("/<run_id>/json")
def get_json(run_id):
    try:
        with open(f"runs_data/{run_id}.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({"error": "Run not found"}), 404

@bp.get("/<run_id>/csv")
def get_csv(run_id):
    try:
        with open(f"runs_data/{run_id}.json", "r") as f:
            data = json.load(f)
        csv_content = to_csv(data["output"])
        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename={run_id}.csv"}
        )
    except:
        return jsonify({"error": "Run not found"}), 404