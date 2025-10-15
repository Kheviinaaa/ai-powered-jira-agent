# /src/validators.py
# This module handles the validation of AI-generated JSON against the defined schemas.
# It is owned by AI Engineer 2 and used by AI Engineer 1 in the generation/repair loop[cite: 101, 161].

import json
from jsonschema import validate, RefResolver, ValidationError
import os

def load_schemas():
    """Loads all schemas and resolves internal $ref references."""
    schema_dir = os.path.join(os.path.dirname(__file__), 'schemas')

    # Load individual schemas
    with open(os.path.join(schema_dir, 'output.schema.json'), 'r') as f:
        output_schema = json.load(f)
    with open(os.path.join(schema_dir, 'story.schema.json'), 'r') as f:
        story_schema = json.load(f)
    with open(os.path.join(schema_dir, 'test.schema.json'), 'r') as f:
        test_schema = json.load(f)

    # Create a resolver to handle local $ref links between schemas
    resolver = RefResolver(
        base_uri=f'file://{os.path.abspath(schema_dir)}/',
        referrer=output_schema,
        store={
            "output.schema.json": output_schema,
            "story.schema.json": story_schema,
            "test.schema.json": test_schema,
        }
    )
    return output_schema, resolver

def validate_output(json_data: dict) -> (bool, list):
    """
    Validates a JSON object against the master output.schema.json.

    Args:
        json_data: The Python dictionary parsed from the AI's JSON output.

    Returns:
        A tuple (is_valid, errors).
        'is_valid' is True if validation passes, False otherwise.
        'errors' is a list of error messages if validation fails.
    """
    try:
        output_schema, resolver = load_schemas()
        validate(instance=json_data, schema=output_schema, resolver=resolver)
        return True, []
    except ValidationError as e:
        # Format a user-friendly error message
        error_message = f"Validation failed at path '{list(e.path)}': {e.message}"
        return False, [error_message]
    except Exception as e:
        return False, [f"An unexpected error occurred during validation: {str(e)}"]

# Example usage for testing
if __name__ == '__main__':
    # This sample should fail because 'generated_at' is missing and story_points is invalid
    sample_invalid_json = {
      "project_name": "Checkout System",
      "epics": [{
          "epic_id": "EPC-001",
          "stories": [{
              "story_id": "US-01",
              "title": "Test Story",
              "description": "A test.",
              "acceptance_criteria": [{"given": "g", "when": "w", "then": "t"}],
              "story_points": 99, # Invalid value
              "sp_justification": "...",
              "risk": "High",
              "test_cases": []
          }]
      }]
    }

    is_valid, errors = validate_output(sample_invalid_json)
    print(f"Validation Result: {'PASS' if is_valid else 'FAIL'}")
    if not is_valid:
        print("Errors:")
        for err in errors:
            print(f"- {err}")

    # This sample should pass
    sample_valid_json = {
      "project_name": "Checkout System",
      "generated_at": "2025-10-12T18:00:00Z",
      "epics": []
    }
    is_valid, errors = validate_output(sample_valid_json)
    print(f"\nValidation Result: {'PASS' if is_valid else 'FAIL'}")