# ---------------------------------------------------------
# heuristics.py
# Computes evaluation metrics for AI-generated Agile outputs.
# Works for a single epic dict or a list of epic dicts.
# ---------------------------------------------------------
from __future__ import annotations
from typing import Any, Dict, Tuple

REQUIRED_STORY_FIELDS = {"title", "description", "acceptance_criteria", "story_points"}
AC_KEYS = {"Given", "When", "Then"}

def _story_is_complete(story: dict) -> bool:
    if not REQUIRED_STORY_FIELDS.issubset(story.keys()):
        return False
    ac = story.get("acceptance_criteria", {})
    return isinstance(ac, dict) and AC_KEYS.issubset(ac.keys())

def _metrics_for_one(epic_obj: dict) -> Tuple[int, int, int]:
    """
    Returns (total_stories, valid_stories, high_risk_count)
    - high risk defined as story_points >= 8
    """
    total = 0
    valid = 0
    high = 0
    stories = epic_obj.get("UserStories", []) or []
    for s in stories:
        total += 1
        if _story_is_complete(s):
            valid += 1
            try:
                if float(s.get("story_points", 0)) >= 8:
                    high += 1
            except (TypeError, ValueError):
                pass
    return total, valid, high

def compute_metrics(data: Any) -> Dict[str, float]:
    # Aggregate across list or single dict
    if isinstance(data, list):
        totals = [ _metrics_for_one(d) for d in data ]
        total_stories = sum(t for t, _, _ in totals)
        valid_stories = sum(v for _, v, _ in totals)
        high_risk     = sum(h for _, _, h in totals)
    else:
        total_stories, valid_stories, high_risk = _metrics_for_one(data)

    story_validity = (valid_stories / total_stories * 100.0) if total_stories else 0.0
    risk_score     = (high_risk / total_stories * 100.0) if total_stories else 0.0
    consistency    = (story_validity + risk_score) / 2.0

    return {
        "Story Count Completeness": round(story_validity, 2),
        "Risk Coverage (High-risk stories)": round(risk_score, 2),
        "Overall Consistency Score": round(consistency, 2),
    }
