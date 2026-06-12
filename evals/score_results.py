# Testing file 

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
from evals.metrics import score_result

def score_all(input_path="results/raw_results.json",
              output_path="results/scored_results.json"):

    with open(input_path) as f:
        results = json.load(f)

    print(f"Scoring {len(results)} results...")

    scored = [score_result(r) for r in results]

    with open(output_path, "w") as f:
        json.dump(scored, f, indent=2)

    # Print summary table
    df = pd.DataFrame(scored)
    summary = df.groupby(["model", "strategy"])[
        ["exact_match", "token_f1", "execution_accuracy"]
    ].mean().round(3)

    print("\n=== RESULTS SUMMARY ===")
    print(summary.to_string())

    return scored

if __name__ == "__main__":
    score_all()