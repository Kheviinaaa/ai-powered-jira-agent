import pandas as pd

def to_csv(output):
    rows = []
    for epic in output.get("epics", []):
        for story in epic.get("stories", []):
            for tc in story.get("test_cases", []):
                rows.append({
                    "epic_id": epic.get("epic_id"),
                    "story_id": story.get("story_id"),
                    "story_title": story.get("title"),
                    "tc_id": tc.get("id"),
                    "preconditions": tc.get("preconditions"),
                    "steps": tc.get("steps"),
                    "expected_result": tc.get("expected_result")
                })
    df = pd.DataFrame(rows)
    return df.to_csv(index=False)
