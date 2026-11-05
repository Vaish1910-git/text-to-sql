COMPARISON_RESULTS = {
    "question": "Who are my best customers?",

    "without_clarification": {
        "interpretation": "Highest total spending",
        "top_customer": "Amit",
        "value": 72500.00
    },

    "with_clarification": {
        "selected_interpretation": "Most number of orders",
        "top_customers": ["Priya", "Amit", "Rahul"],
        "order_count": 2
    },

    "observation": (
        "Clarification helps the system understand the user's "
        "intended meaning instead of assuming one interpretation."
    )
}