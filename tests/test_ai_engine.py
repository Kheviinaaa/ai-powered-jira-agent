# Basic unit test for ai_engine.py
import json, os

def test_output_file():
    path = os.path.join("..", "out", "sample_output.json")
    assert os.path.exists(path), "sample_output.json missing"
    with open(path) as f:
        data = json.load(f)
    assert isinstance(data, list), "Output should be a list"
    assert "UserStories" in data[0], "Missing key: UserStories"
    assert "TestCases" in data[0], "Missing key: TestCases"
