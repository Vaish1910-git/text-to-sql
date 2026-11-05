
from app.engine.gemini_client import ask_gemini
from app.database.schema import DATABASE_SCHEMA
from app.engine.sql_validator import validate_sql


def correct_sql(original_question, incorrect_sql, error_message):

    prompt = f"""
You are an expert PostgreSQL SQL developer.

The following SQL query failed validation.

Database schema:
{DATABASE_SCHEMA}

Original user question:
{original_question}

Incorrect SQL:
{incorrect_sql}

Validation error:
{error_message}

Your task:
1. Fix the SQL query.
2. Generate only a SELECT query.
3. Use only the tables and columns in the schema.
4. Use correct PostgreSQL syntax.
5. Return only SQL without Markdown formatting.
"""

    response = ask_gemini(prompt)

    return response.strip()


def generate_valid_sql(original_question, initial_sql, max_attempts=2):

    sql_query = initial_sql

    for attempt in range(max_attempts + 1):

        is_valid, message = validate_sql(sql_query)

        if is_valid:
            return sql_query, True, "SQL query is valid."

        if attempt == max_attempts:
            return sql_query, False, message

        print(f"\nSQL validation failed: {message}")
        print(f"Correction attempt {attempt + 1}...")

        sql_query = correct_sql(
            original_question,
            sql_query,
            message
        )

    return sql_query, False, "Unable to correct SQL."


if __name__ == "__main__":

    question = "Show customers from Pune"

    incorrect_sql = "SELECT * FROM customers ORDERBY customer_id"

    corrected_sql, is_valid, message = generate_valid_sql(
        question,
        incorrect_sql
    )

    print("\nCorrected SQL:")
    print(corrected_sql)

    print("\nValidation:", message)
