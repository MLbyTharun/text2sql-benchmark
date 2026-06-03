# 🧪 LLM Evaluation Harness — Text-to-SQL Benchmark

A structured evaluation framework that benchmarks Large Language Models on Text-to-SQL generation across multiple models and prompt strategies.

---

## 📌 What This Project Does

Most teams pick LLMs based on gut feeling. This project builds a data-driven evaluation system that measures:
- Which model generates the most accurate SQL
- Which prompt strategy works best
- What the cost vs accuracy tradeoff looks like across models

---

## 🔍 Key Findings

| Model | Strategy | Exact Match | Execution Accuracy | Avg Latency |
|---|---|---|---|---|
| llama-3.3-70b-versatile | few_shot | 45% | 100% | 1441ms |
| llama-3.1-8b-instant | few_shot | 40% | 95% | ~1000ms |
| openai/gpt-oss-20b | few_shot | 40% | 95% | ~1500ms |

**Notable insights:**
- Few-shot prompting outperforms zero-shot and chain-of-thought across all models
- Chain-of-thought actually hurts SQL generation — models overthink simple queries
- Llama 3.1 8B is surprisingly competitive with much larger models at lower latency
- Execution accuracy (98.3% avg) is far higher than exact match (26.7%) — models write functionally correct SQL even when wording differs

---

## 🛠 Tech Stack

- **Models:** Llama 3.3 70B, Llama 3.1 8B, GPT-OSS 20B via Groq
- **Dataset:** b-mc2/sql-create-context (HuggingFace)
- **Metrics:** Exact match, execution accuracy (SQLite), token F1
- **Experiment Tracking:** Weights & Biases
- **Dashboard:** Streamlit
- **Language:** Python 3.12

---

## 📊 Metrics Explained

- **Exact Match** — Does the generated SQL exactly match the expected SQL?
- **Execution Accuracy** — Does the SQL actually run and return the correct result?
- **Token F1** — Token level overlap between generated and expected SQL

---

## 🚀 How to Run

**1. Clone the repo**
```bash
git clone https://github.com/MLbyTharun/llm-eval-harness.git
cd llm-eval-harness
```

**2. Install dependencies**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**3. Add your API keys**
```bash
# Create a .env file
GROQ_API_KEY=your_key_here
WANDB_API_KEY=your_key_here
```

**4. Run the evaluation**
```bash
python experiments/run_eval.py
```

**5. Launch the dashboard**
```bash
streamlit run dashboard/app.py
```

---

## 📁 Project Structure
# Project Structure

```text
llm-eval-harness/
├── data/             # Dataset loading
├── evals/            # Metrics and scoring
├── experiments/      # Eval runner and prompt strategies
├── models/           # Model abstractions
├── dashboard/        # Streamlit UI
├── requirements.txt
└── README.md
```

---

## 📈 Experiment Tracking

All runs are tracked on Weights & Biases with per-example logging of metrics, latency, and model outputs.