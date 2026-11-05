import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def test_connection():
    try:
        with engine.connect() as connection:

            print("PostgreSQL connected successfully!")

            query = text("""
                SELECT name, city
                FROM customers
                ORDER BY customer_id;
            """)

            result = connection.execute(query)

            rows = result.fetchall()

            print("\nCustomer Records:")

            for row in rows:
                print(row)

    except Exception as e:
        print("Error:", e)

def execute_query(sql_query):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

            rows = result.mappings().all()

            return [dict(row) for row in rows]

    except Exception as e:
        print("Query execution failed:", e)
        return []
if __name__ == "__main__":
    test_connection()