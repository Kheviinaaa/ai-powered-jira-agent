# ---------------------------------------------------------
# evaluation.py
# Main evaluation and reporting script.
# - Finds your output file automatically (out/ OR out/out/)
# - Validates list or single dict
# - Aggregates metrics across all epics
# ---------------------------------------------------------
from __future__ import annotations
import json
import os
from typing import Any, Dict

from validators import validate_output
from heuristics import compute_metrics

def _find_output_path() -> str | None:
    candidates = [
        os.path.join("out", "sample_output.json"),
        os.path.join("out", "out", "sample_output.json"),
        "sample_output.json",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def _load_json(path: str) -> Any | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f" File not found: {path}")
    except json.JSONDecodeError as e:
        print(f" Invalid JSON in: {path} — {e}")
    return None

def run_evaluation() -> Dict[str, float] | None:
    print("\n--- Running AI Generation Evaluation ---")

    # Step 1: Load AI output
    path = _find_output_path()
    if not path:
        print("No valid AI output found. Run ai_engine.py first.")
        return None

    data = _load_json(path)
    if data is None:
        print("No valid AI output found. Run ai_engine.py first.")
        return None

    print("Step 1: Generating AI output...")
    print("Step 2: Validating and computing metrics...")

    # Validate schema (supports list or single)
    is_valid, errors, validity_pct = validate_output(data)

    # Compute heuristic metrics (aggregate if list)
    metrics = compute_metrics(data)
    metrics["Structural Validity (passes schema)"] = round(validity_pct, 2)

    # Print summary
    print("\n--- Evaluation Summary ---")
    for key in [
        "Story Count Completeness",
        "Risk Coverage (High-risk stories)",
        "Overall Consistency Score",
        "Structural Validity (passes schema)",
    ]:
        val = metrics.get(key)
        suffix = "%" if key != "Overall Consistency Score" or isinstance(val, (int, float)) else ""
        print(f" - {key}: {val}%")

    print("--------------------------")

    # Export results
    print("\nStep 3: Exporting results...")
    out_dir = "out"
    os.makedirs(out_dir, exist_ok=True)
    report_path = os.path.join(out_dir, "evaluation_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f" Evaluation complete. Results saved to {report_path}")
    return metrics

if __name__ == "__main__":
    run_evaluation()
