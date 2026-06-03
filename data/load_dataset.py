from datasets import load_dataset
import pandas as pd

def load_sql_data(num_samples: int = 100) -> pd.DataFrame:
    print("Loading dataset...")
    dataset = load_dataset("b-mc2/sql-create-context", split="train")
    
    # Take a sample
    df = pd.DataFrame(dataset[:num_samples])
    
    # Keep only what we need
    df = df[["question", "context", "answer"]].dropna()
    df = df.rename(columns={"answer": "expected_sql"})
    
    print(f"Loaded {len(df)} examples")
    return df

if __name__ == "__main__":
    df = load_sql_data(10)
    print(df.head(3))