import os
from dotenv import load_dotenv
import psycopg2
import csv

# Load the .env file
load_dotenv()

# Retrieve database credentials from .env
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=db_user,
        password=db_password,
        port=db_port
    )
    print("Successfully connected to the database")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()

# Create a cursor to execute queries
cursor = conn.cursor()

# Check PostgreSQL version
cursor.execute("SELECT version();")
db_version = cursor.fetchone()
print(f"Connected to - {db_version}")

# Drop existing 'orders' table (if exists)
print("Dropping 'orders' table if it exists...")
cursor.execute('''
    DROP TABLE IF EXISTS orders;
''')
conn.commit()

# Create 'orders' table based on CSV structure
print("Creating 'orders' table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        product_id INT,
        customer_id INT,
        quantity INT,
        price DECIMAL(10, 2),
        order_date DATE
    );
''')
conn.commit()

# Import data from CSV into the 'orders' table
csv_file_path = 'MOCK_DATA.csv'
print(f"Reading data from {csv_file_path}...")
try:
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            print(f"Inserting row: {row}")
            cursor.execute('''
                INSERT INTO orders (product_id, customer_id, quantity, price, order_date)
                VALUES (%s, %s, %s, %s, %s)
            ''', (int(row[0]), int(row[1]), int(row[2]), float(row[3]), row[4]))
    conn.commit()
    print("Data successfully inserted from CSV.")
except Exception as e:
    print(f"Error reading or inserting data from CSV: {e}")

# Example 1: Aggregation - Calculate total revenue from all orders
try:
    print("Calculating total revenue...")
    cursor.execute('''
        SELECT SUM(price * quantity) AS total_revenue
        FROM orders;
    ''')
    total_revenue = cursor.fetchone()[0]
    print(f"Total Revenue: {total_revenue}")
except Exception as e:
    print(f"Error calculating total revenue: {e}")

# Example 2: Window Function - Rank orders by total price
try:
    print("Ranking orders by total price...")
    cursor.execute('''
        SELECT product_id, customer_id, quantity, price, 
               RANK() OVER (ORDER BY (price * quantity) DESC) AS rank
        FROM orders;
    ''')
    ranked_orders = cursor.fetchall()
    print("\nRanked Orders by Total Price:")
    for order in ranked_orders:
        print(order)
except Exception as e:
    print(f"Error ranking orders: {e}")

# Example 3: Join - Assuming we have a customers table, join orders with customers
# Create 'customers' table
print("Creating 'customers' table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY, -- Use 'id' to match the customer_id in the 'orders' table
        name VARCHAR(100),
        email VARCHAR(100)
    );
''')
conn.commit()

# Insert some dummy customer data
print("Inserting dummy customer data...")
cursor.execute('''
    INSERT INTO customers (name, email)
    VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Charlie', 'charlie@example.com'),
    ('David', 'david@example.com'),
    ('Eve', 'eve@example.com')
    ON CONFLICT DO NOTHING;
''')
conn.commit()

# Join customers and orders tables to show customer orders
try:
    print("Joining customers and orders tables...")
    cursor.execute('''
        SELECT customers.name, orders.product_id, orders.quantity, orders.price, orders.order_date
        FROM orders
        JOIN customers ON customers.id = orders.customer_id;
    ''')
    customer_orders = cursor.fetchall()
    print("\nCustomer Orders:")
    for order in customer_orders:
        print(order)
except Exception as e:
    print(f"Error joining customers and orders: {e}")

# Close cursor and connection
cursor.close()
conn.close()
print("PostgreSQL connection closed.")
