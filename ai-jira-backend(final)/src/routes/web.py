from flask import Blueprint, render_template
import json
import os

bp = Blueprint('web', __name__)

# Simple placeholder functions
def generate_from_payload(data):
    return {"stories": ["Mock story 1", "Mock story 2"], "test_cases": ["Mock test 1", "Mock test 2"]}

def store(run_data):
    os.makedirs("runs_data", exist_ok=True)
    with open(f"runs_data/{run_data['run_id']}.json", "w") as f:
        json.dump(run_data, f)

def get(run_id):
    try:
        with open(f"runs_data/{run_id}.json", "r") as f:
            return json.load(f)
    except:
        return None

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/runs')
def runs_list():
    return render_template('runs_list.html')