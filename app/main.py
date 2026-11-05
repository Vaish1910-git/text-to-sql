
from app.engine.text_to_sql import generate_sql
from app.engine.clarification import detect_ambiguity
from app.engine.sql_corrector import generate_valid_sql
from app.database.connection import execute_query


def main():

    # Step 1: Get user question
    original_question = input("Ask your database: ")

    # Step 2: Detect ambiguity
    clarification = detect_ambiguity(original_question)

    question = original_question

    if clarification["is_ambiguous"]:

        print("\n" + clarification["question"])

        for index, option in enumerate(
            clarification["options"], start=1
        ):
            print(f"{index}. {option}")

        choice = input("\nSelect an option: ")

        if not choice.isdigit():
            print("Invalid choice.")
            return

        choice = int(choice)

        if choice < 1 or choice > len(clarification["options"]):
            print("Invalid choice.")
            return

        selected_option = clarification["options"][choice - 1]

        question = (
            f"Original question: {original_question}\n"
            f"Clarified meaning: {selected_option}"
        )

    # Step 3: Generate SQL
    initial_sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(initial_sql)

    # Step 4: Validate and correct SQL
    sql_query, is_valid, message = generate_valid_sql(
        question,
        initial_sql
    )

    print("\nFinal SQL:")
    print(sql_query)

    print("\nValidation:", message)

    if not is_valid:
        print("Query rejected. Not executing.")
        return

    # Step 5: Execute SQL
    results = execute_query(sql_query)

    print("\nQuery Results:")

    for row in results:
        print(row)


if __name__ == "__main__":
    main()
