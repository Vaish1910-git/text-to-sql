ANSWER_TEST_CASES = [
    {
        "question": "Show customers from Pune",
        "check_type": "names",
        "expected": ["Rahul", "Sneha"]
    },
    {
        "question": "List all customers from Mumbai",
        "check_type": "names",
        "expected": ["Priya"]
    },
    {
        "question": "Show all orders",
        "check_type": "row_count",
        "expected": 8
    },
    {
        "question": "How many customers are there?",
        "check_type": "scalar",
        "expected": 5
    },
    {
        "question": "Which customers placed the most orders?",
        "check_type": "order_counts",
        "expected": {
            "Priya": 2,
            "Amit": 2,
            "Rahul": 2,
            "Sneha": 1,
            "Karan": 1
        }
    },
    {
        "question": "Find customers who have spent the most money",
        "check_type": "top_spender",
        "expected": {
            "name": "Amit",
            "total_spent": 72500.00
        }
    }
]