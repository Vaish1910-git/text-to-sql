DATABASE_SCHEMA = """
Database: text_to_sql_db

Table: customers
- customer_id: integer, primary key
- name: customer name
- city: customer city
- email: customer email

Table: orders
- order_id: integer, primary key
- customer_id: foreign key referencing customers.customer_id
- order_date: date
- status: order status

Table: order_items
- item_id: integer, primary key
- order_id: foreign key referencing orders.order_id
- product_name: product name
- quantity: number of items
- price: price per item
"""