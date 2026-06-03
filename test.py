from models.groq_model import GroqModel

models = [
    GroqModel("llama-3.3-70b-versatile"),
    GroqModel("llama-3.1-8b-instant"),
    GroqModel("openai/gpt-oss-20b"),
]

"""for model in models:
    result = model.generate("What is 2 + 2? Answer in one word.")
    print(result)
"""

from experiments.prompts import PROMPT_STRATEGIES

question = "How many students are there?"
context = "CREATE TABLE students (id INT, name VARCHAR, age INT)"

for strategy_name, prompt_fn in PROMPT_STRATEGIES.items():
    print(f"\n--- {strategy_name} ---")
    print(prompt_fn(question, context))