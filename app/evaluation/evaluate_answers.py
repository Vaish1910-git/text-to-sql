from app.evaluation.answer_test_cases import ANSWER_TEST_CASES
from app.engine.text_to_sql import generate_sql
from app.engine.sql_corrector import generate_valid_sql
from app.database.connection import execute_query


def evaluate_answers():

    correct = 0
    total = len(ANSWER_TEST_CASES)

    print("\nANSWER CORRECTNESS EVALUATION\n")

    for test in ANSWER_TEST_CASES:

        question = test["question"]
        check_type = test["check_type"]
        expected = test["expected"]

        print(f"\nQuestion: {question}")

        try:
            # Generate SQL
            initial_sql = generate_sql(question)

            # Validate and correct SQL
            final_sql, is_valid, message = generate_valid_sql(
                question, initial_sql
            )

            if not is_valid:
                print("SQL validation failed:", message)
                continue

            # Execute SQL
            results = execute_query(final_sql)

            # Compare actual result with expected answer
            actual = None

            if check_type == "names":
                actual = sorted(row["name"] for row in results)
                expected = sorted(expected)

            elif check_type == "row_count":
                actual = len(results)

            elif check_type == "scalar":
                actual = list(results[0].values())[0] if results else None

            elif check_type == "order_counts":
                actual = {
                    row["name"]: row["order_count"]
                    for row in results
                }

            elif check_type == "top_spender":
                if results:
                    actual = {
                        "name": results[0]["name"],
                        "total_spent": float(results[0]["total_spent"])
                    }

            # Compare results
            if check_type == "top_spender" and actual is not None:
                is_correct = (
                    actual["name"] == expected["name"]
                    and abs(
                        actual["total_spent"] - expected["total_spent"]
                    ) < 0.01
                )
            else:
                is_correct = actual == expected

            if is_correct:
                print("Result: PASS")
                correct += 1
            else:
                print("Result: FAIL")

            print("Expected:", expected)
            print("Actual:  ", actual)

        except Exception as error:
            print("Test error:", error)

        print("-" * 50)

    accuracy = (correct / total) * 100

    print("\nFINAL RESULTS")
    print(f"Correct answers: {correct}/{total}")
    print(f"Answer accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    evaluate_answers()