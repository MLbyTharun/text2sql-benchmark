def zero_shot_prompt(question: str, context: str) -> str:
    return f"""Given the following SQL table schema:
{context}

Write a SQL query to answer this question: {question}
Return only the SQL query, nothing else."""


def few_shot_prompt(question: str, context: str) -> str:
    return f"""Given the following SQL table schema:
{context}

Here are some examples:
Question: How many employees are there?
SQL: SELECT COUNT(*) FROM employees;

Question: What are the names of all customers?
SQL: SELECT name FROM customers;

Question: Find all products with price greater than 100
SQL: SELECT * FROM products WHERE price > 100;

Now answer this:
Question: {question}
Return only the SQL query, nothing else."""


def chain_of_thought_prompt(question: str, context: str) -> str:
    return f"""Given the following SQL table schema:
{context}

Think step by step, then write a SQL query to answer: {question}

Steps:
1. Identify which tables and columns are needed
2. Determine any filters or conditions
3. Write the final SQL query

Return only the final SQL query, nothing else."""


PROMPT_STRATEGIES = {
    "zero_shot": zero_shot_prompt,
    "few_shot": few_shot_prompt,
    "chain_of_thought": chain_of_thought_prompt,
}