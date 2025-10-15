# ---------------------------------------------------------
# validators.py
# Validates AI-generated output (single dict or list of dicts)
# against a strict JSON Schema that matches your ai_engine.py output.
# ---------------------------------------------------------

from __future__ import annotations
import json
import os
from typing import Tuple, List, Any

from jsonschema import validate
from jsonschema.exceptions import ValidationError

# Inline schemas (no $ref) to avoid resolver issues
STORY_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "acceptance_criteria": {
            "type": "object",
            "properties": {
                "Given": {"type": "string"},
                "When": {"type": "string"},
                "Then": {"type": "string"}
            },
            "required": ["Given", "When", "Then"]
        },
        "story_points": {"type": "number"}
    },
    "required": ["title", "description", "acceptance_criteria", "story_points"]
}

TEST_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "objective": {"type": "string"},
        "expected_result": {"type": "string"}
    },
    "required": ["id", "objective", "expected_result"]
}

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "Epic": {"type": "string"},
        "UserStories": {"type": "array", "items": STORY_SCHEMA},
        "TestCases": {"type": "array", "items": TEST_SCHEMA}
    },
    "required": ["Epic", "UserStories", "TestCases"]
}

def _validate_one(obj: dict) -> Tuple[bool, str | None]:
    try:
        validate(instance=obj, schema=OUTPUT_SCHEMA)
        return True, None
    except ValidationError as e:
        path = " → ".join(str(p) for p in e.path) if e.path else "(root)"
        return False, f"path [{path}]: {e.message}"

def validate_output(data: Any) -> Tuple[bool, List[str], float]:
    """
    Validate either a single epic dict or a list of epic dicts.
    Returns: (is_all_valid, errors, validity_percent)
    - is_all_valid: True only if every item validates
    - errors: list of error strings (empty if all valid)
    - validity_percent: 0..100 proportion of valid items
    """
    errors: List[str] = []

    if isinstance(data, list):
        total = len(data)
        valid_count = 0
        for idx, item in enumerate(data):
            ok, err = _validate_one(item)
            if not ok:
                errors.append(f"[epic #{idx}] {err}")
            else:
                valid_count += 1
        pct = (valid_count / total * 100.0) if total else 0.0
        return valid_count == total, errors, pct
    else:
        ok, err = _validate_one(data)
        return ok, ([] if ok else [err]), (100.0 if ok else 0.0)

if __name__ == "__main__":
    # Handy manual check: tries both possible locations
    candidates = [
        os.path.join("out", "sample_output.json"),
        os.path.join("out", "out", "sample_output.json"),
        "sample_output.json",
    ]
    path = next((p for p in candidates if os.path.exists(p)), None)
    if not path:
        print(" No sample_output.json found.")
        raise SystemExit(0)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    ok, errs, pct = validate_output(data)
    print(f"Validation Result: {'PASS' if ok else 'FAIL'} ({pct:.1f}%)")
    if errs:
        print("Errors:")
        for e in errs:
            print(" -", e)
