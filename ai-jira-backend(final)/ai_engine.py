import sys, os
import uuid
import datetime

# ---------------------------------------------------------
# Ensure project root is on Python path (so imports work)
# ---------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from models.schemas import GenerateRequest
import ai_engine  # Uses your uploaded ai_engine.py file


def generate_from_payload(payload):
    """
    Validates the incoming payload, sends each epic to the AI engine,
    and formats the combined output for the backend.
    """
    # Validate payload using Pydantic schema
    req = GenerateRequest(**payload)
    all_outputs = []

    # Process each epic in the request
    for epic in req.epics:
        # Combine title and description into a single text for the AI
        epic_text = f"{epic.title}: {epic.description or ''}"

        # Generate user stories + test cases using AI engine
        ai_output = ai_engine.generate_user_stories(epic_text)

        # Validate AI output
        if not ai_engine.validate_output(ai_output):
            print(f"⚠️ Validation failed for epic: {epic.title}")

        all_outputs.append(ai_output)

    # Clean duplicates or invalid entries
    final_output = ai_engine.post_process(all_outputs)

    # Return the full structured run result
    return {
        "run_id": str(uuid.uuid4()),
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "output": {
            "epics": final_output
        }
    }
