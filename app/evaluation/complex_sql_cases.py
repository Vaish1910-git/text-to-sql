COMPLEX_SQL_CASES = [
    {
        "question": "Show each customer with their total number of orders",
        "expected_tables": ["customers", "orders"]
    },
    {
        "question": "Find customers who have placed more than one order",
        "expected_tables": ["customers", "orders"]
    },
    {
        "question": "Show the total spending of each customer",
        "expected_tables": ["customers", "orders", "order_items"]
    },
    {
        "question": "Find products whose total quantity sold is greater than 5",
        "expected_tables": ["order_items"]
    },
    {
        "question": "Show the average price of products",
        "expected_tables": ["order_items"]
    },
    {
        "question": "Find the customer who placed the latest order",
        "expected_tables": ["customers", "orders"]
    }
]