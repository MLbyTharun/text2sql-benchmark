# Text-to-SQL Benchmark Evaluation

A systematic evaluation of large language models on the Text-to-SQL task, comparing multiple model architectures across different prompting strategies, with execution-based result verification and an interactive results dashboard.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Models Evaluated](#models-evaluated)
- [Prompting Strategies](#prompting-strategies)
- [Evaluation Pipeline](#evaluation-pipeline)
- [Tech Stack](#tech-stack)
- [Results & Tracking](#results--tracking)
- [Dashboard](#dashboard)
- [Threats to Validity](#threats-to-validity)
- [Future Work](#future-work)
- [How to run](#How-to-Run)
- [Project Structute](#Project-Structure)
---

## Project Overview

This project benchmarks the capability of large language models (LLMs) to translate natural language questions into executable SQL queries — a task known as **Text-to-SQL**. Rather than relying solely on string-level comparison, the evaluation uses **execution-based assessment** to determine whether a generated query retrieves the correct answer from the database, accounting for the fact that multiple syntactically different queries can be semantically equivalent.

The study covers four modls across three prompting strategies, evaluated under identical conditions for a rigorous and fair comparison.

---

## Dataset

Each sample in the benchmark consists of three components:

- A **database schema** describing table and column structure
- A **natural language question** posed by a user
- A **ground-truth SQL query** as the reference answer

### Key Challenges

Text-to-SQL is a non-trivial task. The core difficulties include:

- Interpeting the user's intent from loosely worded questions
- Mapping natural language terms to the correct schema attributes
- Selecting the right tables and columns among potentially many candidates
- Generating syntactically valid SQL
- Handling aggregations, filters, joins, and nested queries correctly
- Recognizing that multiple SQL formulations can produce identical results

Because of the last point, **execution-based evaluation is used alongside Exact Match** — a generated query us considered correct if it retrieves the same result set as the ground-truth query, even if the SQL text differs.

---

## Models Evaluated

All inference was served through the **Groq API**, which provides optimized low-latency infrastructure for LLM serving. The following models were selected to span a wide range of parameter scales and architectures:

| Model | Parameters |
|---|---|
| `llama-3.1-8b-instant` | 8 Billion |
| `llama-3.3-70b-versatile` | 70 Billion |
| `openai/gpt-oss-20b` | 20 Billion |
| `openai/gpt-oss-120b` | 120 Billion |

All models were evaluated under identical prompt conditions and using the same evaluation pipeline.

---
## Results

All metrics are reported as percentages. Latency is the average inference time per query in milliseconds.

| Model | Strategy | Exact Match (%) | Token F1 (%) | Execution Accuracy (%) | Latency (ms) |
|---|---|:---:|:---:|:---:|:---:|
| llama-3.1-8b-instant | Zero Shot | 15.0 | 76.3 | 97.0 | 1786 |
| llama-3.1-8b-instant | Few Shot | 27.0 | 77.3 | 95.0 | 2463 |
| llama-3.1-8b-instant | Chain of Thought | 13.0 | 78.3 | 95.0 | 2476 |
| llama-3.3-70b-versatile | Zero Shot | 16.0 | 75.5 | 98.0 | 1831 |
| llama-3.3-70b-versatile | Few Shot | 28.0 | 83.0 | 98.0 | 2487 |
| llama-3.3-70b-versatile | Chain of Thought | 16.0 | 72.5 | 98.0 | 2487 |
| openai/gpt-oss-20b | Zero Shot | 8.0 | 65.9 | 98.0 | 2150 |
| openai/gpt-oss-20b | Few Shot | 15.0 | 69.9 | 96.0 | 2903 |
| openai/gpt-oss-20b | Chain of Thought | 4.0 | 65.7 | 96.0 | 2783 |
| openai/gpt-oss-120b | Zero Shot | 2.0 | 65.7 | 98.0 | 2272 |
| openai/gpt-oss-120b | Few Shot | 19.0 | 68.8 | 98.0 | 2915 |
| openai/gpt-oss-120b | Chain of Thought | 1.0 | 66.1 | 98.0 | 2919 |

> **Note:** Execution Accuracy is the primary correctness signal. Exact Match is a strict string comparison and consistently underestimates true model capability across all models and strategies.
---

## Prompting Strategies

Three distinct strategies were tested to understand how prompt design affects SQL generation quality.

### Zero-Shot

The model receives only the database schema and the user question — no examples. Performance here reflects the model's raw, pre-trained capabiity for SQL reasoning.

### Few-Shot

A set of example Question–SQL pairs is prepended to the prompt before the target question. This gives the model in-context demonstrations of SQL syntax patterns, schema interpetation, and query structure without any fine-tuning.

### Chain-of-Thought

The model is instructed to reason through intermediate steps — understanding the question, identifing relevant tables and columns, and planning the query — before producing the final SQL. This strategy targets improvement in logical reasoning and schema understanding.

---

## Evaluation Pipeline

For every combination of model and prompting strategy, the following steps were executed:

1. Provide the input question and schema to the model via the Groq API
2. Receive the generated SQL query
3. Execute both the generated query and the ground-truth query against the database using **SQLite3**
4. Compare execution results to determine correctness
5. Compute Exact Match and Execution Accuracy metrics
6. Log all results and aggregate statistics

The pipeline was kept identical across all experiments to ensure comparability.

---

## Tech Stack

| Component | Tool |
|---|---|
| Inference API | [Groq](https://groq.com) |
| Database Engine | SQLite3 |
| Experiment Tracking | Weights & Biases (wandb) |
| Results Dashboard | Streamlit |
| Language | Python |

### Why Each Tool

- **Groq** — chosen for its high-throughput, low-latency inference, essential when running evaluations across many model-prompt combinations
- **SQLite3** — used to execute both reference and generated SQL queries and compare result sets directly, enabling execution-based evaluation
- **Weights & Biases (wandb)** — tracks all experiment runs, logs per-sample results, metrics, and aggregates, providing full reproducibility and run comparison
- **Streamlit** — powers an interactive dashboard where users can explore model outputs, compare SQL generations, and view results for every question across all models

---

## Results & Tracking

All runs are tracked with **Weights & Biases**. Each logged run includes:

- Model name and prompting strategy
- Per-sample generated SQL and ground-truth SQL
- Execution match result per sample
- Exact Match result per sample
- Aggregate accuracy metrics across the dataset

This makes it straightforward to reproduce any run or audit individual predictions.

---

## Dashboard

The **Streamlit** application provides an interactive interface to explore the benchmark results. Users can:

- Browse every question in the benchmark
- View the generated SQL from all four models side by side
- See the ground-truth SQL and the execution result comparison
- Filter by prompting strategy or model
- Identify where models agree or diverge

This makes the evaluation transoarent and acessible without needing to inspect raw logs or code.

---

## Threats to Validity

The following limitations should be kept in mind when interpreting results.

### Dataset Coverage
The benchmark may not capture the full diversity of real-world database systems. A larger, more varied dataset could surface additional model strengths and weaknesses.

### Prompt Sensitivity
LLMs are sensitive to prompt phrasing, schema formatting, and example selection. Results are specific to the prompts used in this study and may shift with minor modifications.

### Exact Match as a Metric
Exact Match is a strict string-level comparison that can underestimate true model capability. Many generated queries that fail Exact Match still produce correct execution results. Execution Accuracy is the more reliable signal.

### Model Version Dependency
Evaluation reflects the model versions available on Groq at the time of the study. Future updates to these models may change performance characteristics.

### Single-Benchmark Scope
All experiments were conducted on one dataset. Generalization to different domains, schemas, or database scales has not been assessed.

---

## Future Work

Several directions are identified for extending this study:

- **Advanced Prompting** — explore Self-Consistency, ReAct, Program-of-Thought, and Tree-of-Thought prompting
- **Larger Benchmarks** — evaluate on Spider, Spider 2.0, BIRD, and WikiSQL for comparability with published research
- **Error Taxonomy** — categorize failure modes such as wrong column selection, incorrect aggregation, missing filters, and join errors
- **Cross-Model Ensembles** — combine outputs from multiple models to improve robustness
- **Production Database Evaluation** — test on real-world schemas with complex relationships, large table counts, and domain-specific terminology

---

---
## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/MLbyTharun/text2sql-benchmark.git
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

## Project Structure
# Project Structure

```text
text2sql-benchmark/
├── data/             # Dataset loading
├── evals/            # Metrics and scoring
├── experiments/      # Eval runner and prompt strategies
├── models/           # Model abstractions
├── dashboard/        # Streamlit UI
├── requirements.txt
└── README.md
```

---

## Experiment Tracking

All runs are tracked on Weights & Biases with per-example logging of metrics, latency, and model outputs.

