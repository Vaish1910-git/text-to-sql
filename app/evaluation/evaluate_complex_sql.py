from app.evaluation.complex_sql_cases import COMPLEX_SQL_CASES
from app.engine.text_to_sql import generate_sql
from app.engine.sql_corrector import generate_valid_sql
from app.database.connection import execute_query


def evaluate_complex_sql():

    total = len(COMPLEX_SQL_CASES)
    valid_count = 0
    execution_count = 0
    table_count = 0

    print("\nCOMPLEX SQL EVALUATION\n")

    for test in COMPLEX_SQL_CASES:

        question = test["question"]
        expected_tables = test["expected_tables"]

        print(f"\nQuestion: {question}")

        try:
            # Step 1: Generate SQL
            initial_sql = generate_sql(question)

            print(f"\nGenerated SQL:\n{initial_sql}")

            # Step 2: Validate and correct SQL
            final_sql, is_valid, message = generate_valid_sql(
                question, initial_sql
            )

            print("\nFinal SQL after validation:")
            print(repr(final_sql))
            print("Validation result:", is_valid)
            print("Validation message:", message)

            if not is_valid:
                print(f"Validation: FAIL - {message}")
                continue

            valid_count += 1
            print("Validation: PASS")

            # Step 3: Check expected tables
            missing_tables = [
                table for table in expected_tables
                if table.lower() not in final_sql.lower()
            ]

            if not missing_tables:
                table_count += 1
                print("Expected tables: PASS")
            else:
                print(f"Expected tables: FAIL - Missing {missing_tables}")

            # Step 4: Execute SQL
            results = execute_query(final_sql)

            execution_count += 1

            print("Execution: PASS")
            print(f"Rows returned: {len(results)}")

        except Exception as error:
            print(f"Test failed: {error}")

        print("-" * 50)

    # Final report
    print("\nFINAL RESULTS")
    print(f"Total questions: {total}")
    print(f"Valid SQL: {valid_count}/{total}")
    print(f"Successful executions: {execution_count}/{total}")
    print(f"Expected tables matched: {table_count}/{total}")


if __name__ == "__main__":
    evaluate_complex_sql()