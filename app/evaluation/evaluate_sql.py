from app.evaluation.sql_test_cases import SQL_TEST_CASES
from app.engine.text_to_sql import generate_sql
from app.engine.sql_corrector import generate_valid_sql
from app.database.connection import execute_query


def evaluate_sql():

    total = len(SQL_TEST_CASES)
    valid_count = 0
    execution_count = 0
    table_count = 0

    print("\nSQL GENERATION EVALUATION\n")

    for test in SQL_TEST_CASES:

        question = test["question"]
        expected_table = test["expected_table"]

        print(f"\nQuestion: {question}")

        try:
            # Step 1: Generate SQL
            initial_sql = generate_sql(question)
            print(f"Generated SQL: {initial_sql}")

            # Step 2: Validate and correct SQL
            final_sql, is_valid, message = generate_valid_sql(
                question, initial_sql
            )

            if not is_valid:
                print(f"Validation failed: {message}")
                continue

            valid_count += 1
            print("Validation: PASS")

            # Step 3: Check expected table
            if expected_table.lower() in final_sql.lower():
                table_count += 1
                print("Expected table: PASS")
            else:
                print("Expected table: FAIL")

            # Step 4: Execute SQL
            results = execute_query(final_sql)

            execution_count += 1
            print("Execution: PASS")
            print(f"Rows returned: {len(results)}")

        except Exception as error:
            print(f"Test failed: {error}")

        print("-" * 50)

    print("\nFINAL RESULTS")
    print(f"Total questions: {total}")
    print(f"Valid SQL: {valid_count}/{total}")
    print(f"Successful executions: {execution_count}/{total}")
    print(f"Expected table matched: {table_count}/{total}")


if __name__ == "__main__":
    evaluate_sql()