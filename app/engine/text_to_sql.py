from app.engine.gemini_client import ask_gemini
from app.database.schema import DATABASE_SCHEMA


def generate_sql(question):

    prompt = f"""
    You are an expert PostgreSQL SQL developer.

    Your task is to convert the user's natural language
    question into a PostgreSQL SELECT query.

    Database Schema:
    {DATABASE_SCHEMA}

    User Question:
    {question}

    Rules:
    1. Generate only SELECT queries.
    2. Use only tables and columns in the schema.
    3. Use correct JOIN conditions.
    4. Do not generate INSERT, UPDATE, DELETE or DROP.
    5. Return only SQL query without Markdown formatting.
    """

    response = ask_gemini(prompt)

    return response.strip()


if __name__ == "__main__":

    question = input("Ask your database: ")

    sql_query = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql_query)