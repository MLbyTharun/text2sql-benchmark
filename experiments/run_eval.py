import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import wandb
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from models.llm_arch import GroqModel,NvidiaModel
from experiments.prompts import PROMPT_STRATEGIES
from data.load_dataset import load_sql_data
from evals.metrics import score_result

load_dotenv()

# Define models
MODELS = [
    NvidiaModel("openai/gpt-oss-120b"),
    GroqModel("llama-3.3-70b-versatile"),
    GroqModel("llama-3.1-8b-instant"),
    GroqModel("openai/gpt-oss-20b"),
]

def run_eval(num_samples: int = 100):
    # Initialize W&B
    wandb.init(
        project="llm-eval-harness-v2",
        name="sql-eval-run-02",
        config={
            "num_samples": num_samples,
            "models": [m.model_name for m in MODELS],
            "strategies": list(PROMPT_STRATEGIES.keys()),
            "task": "text-to-sql",
        }
    )

    # Load dataset
    df = load_sql_data(num_samples)

    results = []

    for model in MODELS:
        for strategy_name, prompt_fn in PROMPT_STRATEGIES.items():
            print(f"\nRunning: {model.model_name} | {strategy_name}")

            for _, row in tqdm(df.iterrows(), total=len(df)):
                prompt = prompt_fn(row["question"], row["context"])

                try:
                    response = model.generate(prompt)
                    generated_sql = response["output"].strip()
                    latency = response["latency_ms"]
                except Exception as e:
                    generated_sql = ""
                    latency = 0
                    print(f"Error: {e}")

                result = {
                    "model": model.model_name,
                    "strategy": strategy_name,
                    "question": row["question"],
                    "context": row["context"],
                    "expected_sql": row["expected_sql"],
                    "generated_sql": generated_sql,
                    "latency_ms": latency,
                }

                # Score it immediately
                result = score_result(result)

                # Log to W&B
                wandb.log({
                    "model": model.model_name,
                    "strategy": strategy_name,
                    "exact_match": result["exact_match"],
                    "token_f1": result["token_f1"],
                    "execution_accuracy": result["execution_accuracy"],
                    "latency_ms": latency,
                })

                results.append(result)

    # Save results
    os.makedirs("results", exist_ok=True)
    with open("results/raw_results03.json", "w") as f:
        json.dump(results, f, indent=2)

    # Log summary table to W&B
    summary_df = pd.DataFrame(results).groupby(["model", "strategy"])[
        ["exact_match", "token_f1", "execution_accuracy", "latency_ms"]
    ].mean().round(3).reset_index()

    wandb.log({"summary": wandb.Table(dataframe=summary_df)})

    print(f"\nDone! Saved {len(results)} results")
    print(f"View your run at: https://wandb.ai")

    wandb.finish()
    return results

if __name__ == "__main__":
    run_eval(num_samples=100)