
import json
from app.engine.gemini_client import ask_gemini


def detect_ambiguity(question):

    prompt = f"""
You are an ambiguity detection engine for a Text-to-SQL system.

Your task is to decide whether the user's database question
has multiple reasonable interpretations.

Database information:
- customers: customer_id, name, city, email
- orders: order_id, customer_id, order_date, status
- order_items: item_id, order_id, product_name, quantity, price

Rules:
1. If the question has a clear meaning, do not ask for clarification.
2. If a term such as "best", "top", or "valuable" has multiple
   reasonable meanings, ask for clarification.
3. Do not treat a question as ambiguous just because it is broad.
4. Only suggest interpretations supported by the database.
5. For "best customers", possible meanings include:
   - Highest total spending
   - Most number of orders
   - Purchases on the greatest number of distinct dates

Return ONLY valid JSON in this exact structure:

{{
    "is_ambiguous": true,
    "question": "What do you mean by best customers?",
    "options": [
        "Highest total spending",
        "Most number of orders",
        "Purchases on the greatest number of distinct dates"
    ]
}}

If the question is clear, return:

{{
    "is_ambiguous": false,
    "question": null,
    "options": []
}}

User question: {question}
"""

    response = ask_gemini(prompt)

    # Remove Markdown code fences if Gemini adds them.
    response = response.strip()
    if response.startswith("```"):
        response = response.replace("```json", "", 1)
        response = response.replace("```", "").strip()

    result = json.loads(response)

    if not isinstance(result.get("is_ambiguous"), bool):
        raise ValueError("Invalid ambiguity response from Gemini.")

    if result["is_ambiguous"]:
        if not result.get("question") or not result.get("options"):
            raise ValueError("Gemini returned incomplete clarification data.")
    else:
        result["question"] = None
        result["options"] = []

    return result


if __name__ == "__main__":

    user_question = input("Enter your question: ")

    result = detect_ambiguity(user_question)

    if result["is_ambiguous"]:
        print("\nClarification needed:")
        print(result["question"])

        for option in result["options"]:
            print("-", option)
    else:
        print("\nNo ambiguity detected.")
