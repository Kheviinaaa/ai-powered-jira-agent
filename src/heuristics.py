# ---------------------------------------------------------
# heuristics.py
# Computes evaluation metrics for AI-generated Agile outputs.
# ---------------------------------------------------------
def compute_metrics(data):
    # Initialize scores
    total_stories = 0
    valid_stories = 0
    risk_coverage = 0

    # Heuristic: count user stories and check completeness
    if "UserStories" in data:
        total_stories = len(data["UserStories"])
        for story in data["UserStories"]:
            if all(k in story for k in ["title", "description", "acceptance_criteria", "story_points"]):
                valid_stories += 1
                # Heuristic: mark high-risk story if story_points >= 8
                if story["story_points"] >= 8:
                    risk_coverage += 1

    # Avoid divide-by-zero
    story_validity = (valid_stories / total_stories * 100) if total_stories else 0
    risk_score = (risk_coverage / total_stories * 100) if total_stories else 0

    # Consistency score (average heuristic)
    consistency = (story_validity + risk_score) / 2

    return {
        "Story Count Completeness": round(story_validity, 2),
        "Risk Coverage (High-risk stories)": round(risk_score, 2),
        "Overall Consistency Score": round(consistency, 2)
    }
