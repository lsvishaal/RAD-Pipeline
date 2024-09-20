import os
from dotenv import load_dotenv
import psycopg2

# Load the .env file
load_dotenv()

# Retrieve database credentials from .env
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=db_host,
    dbname=db_name,
    user=db_user,
    password=db_password,
    port=db_port
)

# Create a cursor to execute queries
cursor = conn.cursor()

# Check PostgreSQL version
cursor.execute("SELECT version();")
db_version = cursor.fetchone()
print(f"Connected to - {db_version}")

# Create 'customers' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')
conn.commit()

# Create 'orders' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(id),
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        amount DECIMAL(10, 2)
    );
''')
conn.commit()

# Insert sample data into 'customers'
cursor.execute('''
    INSERT INTO customers (name, email)
    VALUES (%s, %s)
''', ('John Doe', 'john.doe@example.com'))
conn.commit()

# Insert data into 'orders'
cursor.execute('''
    INSERT INTO orders (customer_id, amount)
    VALUES (%s, %s)
''', (1, 150.50))
conn.commit()

# Retrieve customer orders with JOIN
cursor.execute('''
    SELECT customers.name, orders.amount, orders.order_date
    FROM customers
    JOIN orders ON customers.id = orders.customer_id;
''')
customer_orders = cursor.fetchall()
for order in customer_orders:
    print(order)

# Get total order amount for each customer
cursor.execute('''
    SELECT customers.name, SUM(orders.amount) as total_amount
    FROM customers
    JOIN orders ON customers.id = orders.customer_id
    GROUP BY customers.name;
''')
customer_totals = cursor.fetchall()
for total in customer_totals:
    print(total)

# Rank customers based on total order amount
cursor.execute('''
    SELECT customers.name, SUM(orders.amount) AS total_amount,
           RANK() OVER (ORDER BY SUM(orders.amount) DESC) AS rank
    FROM customers
    JOIN orders ON customers.id = orders.customer_id
    GROUP BY customers.name;
''')
customer_ranks = cursor.fetchall()
for rank in customer_ranks:
    print(rank)

# Filter orders that exceed $100
cursor.execute('''
    SELECT customers.name, orders.amount
    FROM customers
    JOIN orders ON customers.id = orders.customer_id
    WHERE orders.amount > 100;
''')
filtered_orders = cursor.fetchall()
for order in filtered_orders:
    print(order)

# Close cursor and connection
cursor.close()
conn.close()
print("PostgreSQL connection closed.")
