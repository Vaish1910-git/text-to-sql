from app.evaluation.ambiguity_extended_cases import EXTENDED_CASES
from app.engine.clarification import detect_ambiguity


def evaluate_extended():

    print("\nEXTENDED AMBIGUITY TESTING\n")

    for question in EXTENDED_CASES:

        print(f"\nQuestion: {question}")

        try:
            result = detect_ambiguity(question)

            if result["is_ambiguous"]:
                print("Result: AMBIGUOUS")
                print("Clarification:", result["question"])

                for option in result["options"]:
                    print("-", option)

            else:
                print("Result: NOT AMBIGUOUS")

        except Exception as error:
            print("Error:", error)

        print("-" * 45)


if __name__ == "__main__":
    evaluate_extended()