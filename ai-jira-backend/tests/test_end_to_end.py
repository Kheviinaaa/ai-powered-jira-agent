import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import create_app

def test_generate_and_export():
    app = create_app()
    client = app.test_client()

    payload = {
        "project_name": "Test",
        "epics": [{"epic_id": "E1", "title": "T", "description": "d"}]
    }

    r = client.post("/generate", json=payload)
    assert r.status_code == 200
    data = r.get_json()
    assert "run_id" in data
    run_id = data["run_id"]

    r2 = client.get(f"/runs/{run_id}/json")
    assert r2.status_code == 200
