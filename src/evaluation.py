# ---------------------------------------------------------
# evaluation.py
# Main evaluation and reporting script.
# ---------------------------------------------------------
import json
import os
from validators import validate_output
from heuristics import compute_metrics

# ---------------------------------------------------------
# Load AI output file
# ---------------------------------------------------------
def load_output(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in: {file_path}")
        return None

# ---------------------------------------------------------
# Main Evaluation
# ---------------------------------------------------------
def run_evaluation():
    print("\n--- Running AI Generation Evaluation ---")

    # Step 1: Load AI output
    file_path = os.path.join("out", "sample_output.json")
    output_data = load_output(file_path)
    if not output_data:
        print("No valid AI output found. Run ai_engine.py first.")
        return

    print("Step 1: Generating AI output...")
    print("Step 2: Validating and computing metrics...")

    # Validate schema
    is_valid, errors = validate_output(output_data)
    structural_validity = 100.0 if is_valid else 0.0

    # Compute heuristic metrics
    metrics = compute_metrics(output_data)
    metrics["Structural Validity (passes schema)"] = structural_validity

    # Print summary
    print("\n--- Evaluation Summary ---")
    for key, value in metrics.items():
        print(f" - {key}: {value}%")

    print("--------------------------")

    # Export results
    print("\nStep 3: Exporting results...")
    os.makedirs("out", exist_ok=True)
    report_path = os.path.join("out", "evaluation_report.json")
    with open(report_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"✅ Evaluation complete. Results saved to {report_path}")

# ---------------------------------------------------------
if __name__ == "__main__":
    run_evaluation()
