import sqlite3
import re

#   REFER THE DOC!!!!!!!!!!!!!

def exact_match(generated_sql: str, expected_sql: str) -> int:
    """Check if generated SQL exactly matches expected SQL."""
    gen = generated_sql.strip().lower().rstrip(";")
    exp = expected_sql.strip().lower().rstrip(";")
    return 1 if gen == exp else 0


def token_f1(generated_sql: str, expected_sql: str) -> float:
    """Token level F1 score between generated and expected SQL."""
    gen_tokens = set(generated_sql.lower().split())
    exp_tokens = set(expected_sql.lower().split())

    if not gen_tokens or not exp_tokens:
        return 0.0

    common = gen_tokens & exp_tokens
    if not common:
        return 0.0
    #^^^
    precision = len(common) / len(gen_tokens)
    recall = len(common) / len(exp_tokens)
    f1 = 2 * precision * recall / (precision + recall)
    return round(f1, 4)


def clean_sql(sql: str) -> str:
    """Removes markdown code if model returns them."""
    sql = re.sub(r"```sql", "", sql)
    sql = re.sub(r"```", "", sql)
    return sql.strip()


def execution_accuracy(generated_sql: str, expected_sql: str, context: str) -> int:
    """
    Actually run both SQLs against an in-memory SQLite DB
    and check if results match.
    """
    try:
        generated_sql = clean_sql(generated_sql)
        
        conn = sqlite3.connect(":memory:")#bcz we dont need it after eval
        cursor = conn.cursor()

        # Creatimg tables from context
        cursor.executescript(context)

        # Running expected SQL
        cursor.execute(expected_sql)
        expected_result = cursor.fetchall()

        # Running generated SQL
        cursor.execute(generated_sql)
        generated_result = cursor.fetchall()

        conn.close()
        return 1 if expected_result == generated_result else 0 #^^^

    except Exception:
        return 0


def score_result(result: dict) -> dict:
    """Scores a single result with all metrics."""
    generated = result["generated_sql"]
    expected = result["expected_sql"]
    context = result["context"]

    result["exact_match"] = exact_match(generated, expected)
    result["token_f1"] = token_f1(generated, expected)
    result["execution_accuracy"] = execution_accuracy(generated, expected, context)

    return result