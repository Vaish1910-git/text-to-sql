
import re

from sqlglot import parse, exp
from sqlglot.errors import ParseError, ErrorLevel


ALLOWED_TABLES = {
    "customers",
    "orders",
    "order_items"
}

FORBIDDEN_EXPRESSIONS = {
    "insert",
    "update",
    "delete",
    "drop",
    "create",
    "alter",
    "merge",
    "command",
    "transaction",
    "into",
    "lock"
}


def validate_sql(sql_query):

    try:

        # Step 1: Check empty input
        if not sql_query or not sql_query.strip():
            return False, "SQL query cannot be empty."

        # Step 2: Detect commonly merged SQL keywords
        if re.search(r"\b(ORDERBY|GROUPBY)\b", sql_query, re.IGNORECASE):
            return False, "Invalid SQL keyword spacing. Check ORDER BY or GROUP BY."

        # Step 3: Parse using strict PostgreSQL syntax
        statements = parse(
            sql_query,
            read="postgres",
            error_level=ErrorLevel.RAISE
        )

        # Step 4: Allow exactly one statement
        if len(statements) != 1 or statements[0] is None:
            return False, "Only one SQL statement is allowed."

        expression = statements[0]

        # Step 5: Allow only SELECT queries
        if not isinstance(expression, exp.Select):
            return False, "Only SELECT queries are allowed."

        # Step 6: Check SELECT has columns or expressions
        if not expression.expressions:
            return False, "SELECT must contain at least one column or expression."

        # Step 7: Inspect every SQL expression
        for node in expression.walk():

            # Reject dangerous operations
            if node.key.lower() in FORBIDDEN_EXPRESSIONS:
                return False, "Unsafe SQL operation detected."

            # Check referenced tables
            if isinstance(node, exp.Table):

                table_name = node.name.lower()

                if table_name not in ALLOWED_TABLES:
                    return False, f"Table not allowed: {node.name}"

                # Only allow tables from the public schema
                if node.db and node.db.lower() != "public":
                    return False, "Only the public schema is allowed."

                if node.catalog:
                    return False, "Database-qualified tables are not allowed."

        return True, "SQL query is valid."

    except ParseError:
        return False, "Invalid SQL syntax."

    except Exception as error:
        return False, f"SQL validation error: {error}"


if __name__ == "__main__":

    test_queries = [

        "SELECT * FROM customers",

        "SELECT name FROM customers WHERE city = 'Pune'",

        "SELECT FROM customers",

        "SELECT * FROM customers ORDERBY customer_id",

        "SELECT * FROM unknown_table",

        "DELETE FROM customers",

        "DROP TABLE customers",

        "SELECT * FROM customers; SELECT * FROM orders",

        """
        SELECT c.name, COUNT(o.order_id)
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.name
        ORDER BY COUNT(o.order_id) DESC
        """
        """
SELECT c.customer_id, c.name,
SUM(oi.quantity * oi.price) AS total_spending
FROM customers c
JOIN orders o ON c.customer_id = o.customer_idJOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.name
"""
    ]

    for query in test_queries:

        is_valid, message = validate_sql(query)

        print("\nQuery:", query)
        print("Valid:", is_valid)
        print("Message:", message)
