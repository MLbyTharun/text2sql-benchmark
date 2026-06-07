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


| Model                   | Strategy         | Exact Match | Execution Accuracy | Latency |
|-------------------------|------------------|-------------|--------------------|---------|
| llama-3.1-8b-instant    | chain_of_thought | 15%         | 100%               | 2461ms  |
| llama-3.1-8b-instant    | few_shot         | 40%         | 95%                | 1309ms |
| llama-3.1-8b-instant    | zero_shot        | 20%         | 95%                | 277ms   |
| llama-3.3-70b-versatile | chain_of_thought | 25%         | 100%               | 2679ms  |
| llama-3.3-70b-versatile | few_shot         | 45%         | 100%               | 1441ms  |
| llama-3.3-70b-versatile | zero_shot        | 25%         | 100%               | 405ms   |
| openai/gpt-oss-20b      | chain_of_thought | 10%         | 100%               | 2599ms  |
| openai/gpt-oss-20b      | few_shot         | 40%         | 95%                | 1945ms |
| openai/gpt-oss-20b      | zero_shot        | 20%         | 100%               | 408ms   |

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
## Reasoning Does Not Always Improve Text-to-SQL Performance

Interestingly, Chain-of-Thought (CoT) prompting resulted in lower Exact Match scores compared to Few-Shot prompting. This may be because the models tend to overthink the task, generating more verbose or complex SQL queries than necessary. While these queries are often logically correct and maintain high Execution Accuracy, they can differ syntactically from the reference SQL, leading to lower Exact Match scores. This highlights that in Text-to-SQL tasks, additional reasoning does not always translate into better benchmark performance.

---

## Evaluation Summary

The evaluation compared three open-source LLMs across Zero-Shot, Few-Shot, and Chain-of-Thought (CoT) prompting strategies for SQL generation. Results show that Few-Shot prompting consistently achieved the highest Exact Match scores, reaching 45% with Llama 3.3 70B, while maintaining perfect execution accuracy. This suggests that providing examples helps models better align with the expected SQL query structure.

Although Chain-of-Thought prompting achieved 100% Execution Accuracy across all models, it produced lower Exact Match scores (10–25%). This indicates that the models often generated logically correct SQL queries that returned the correct results but differed syntactically from the reference queries. The additional reasoning steps may have encouraged the models to overthink the task and produce more verbose or alternative SQL formulations.

Zero-Shot prompting delivered the fastest response times, with latencies ranging from 277–408 ms, making it suitable for low-latency applications. However, its Exact Match performance was generally lower than Few-Shot prompting.

Overall, Llama 3.3 70B with Few-Shot prompting emerged as the best-performing configuration, achieving the highest Exact Match score (45%) while maintaining 100% Execution Accuracy. The results highlight the trade-off between response speed, query structure alignment, and reasoning complexity when selecting a prompting strategy for text-to-SQL tasks.

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
