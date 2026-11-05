from app.evaluation.test_cases import TEST_CASES
from app.engine.clarification import detect_ambiguity


def evaluate_clarification():

    correct = 0
    total = len(TEST_CASES)

    print("\nCLARIFICATION ENGINE EVALUATION\n")

    for test in TEST_CASES:

        question = test["question"]
        expected = test["expected_ambiguity"]

        result = detect_ambiguity(question)
        actual = result["is_ambiguous"]

        if expected == actual:
            status = "PASS"
            correct += 1
        else:
            status = "FAIL"

        print(f"Question: {question}")
        print(f"Expected: {expected}")
        print(f"Actual:   {actual}")
        print(f"Result:   {status}")
        print("-" * 40)

    accuracy = (correct / total) * 100

    print("\nFINAL RESULTS")
    print(f"Correct predictions: {correct}/{total}")
    print(f"Accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    evaluate_clarification()