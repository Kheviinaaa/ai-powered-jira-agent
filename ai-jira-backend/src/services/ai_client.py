import uuid, datetime
from ..models.schemas import GenerateRequest

def generate_from_payload(payload):
    # Validate using Pydantic model
    req = GenerateRequest(**payload)
    # Simulated AI output until real AI available
    fake_output = {
        "epics": [{
            "epic_id": e.epic_id,
            "title": e.title,
            "stories": [
                {"story_id": "US-01", "title": f"{e.title} - Story 1",
                 "test_cases": [
                     {"id": "TC-01", "preconditions":"None","steps":"Step 1","expected_result":"Expected"}
                 ]}
            ]
        } for e in req.epics]
    }
    return {
        "run_id": str(uuid.uuid4()),
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "output": fake_output
    }
