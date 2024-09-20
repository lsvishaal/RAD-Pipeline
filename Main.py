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

# # Test query
# cursor.execute("SELECT version();")
# db_version = cursor.fetchone()
# print(f"Connected to - {db_version}")

#Create Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')
conn.commit()
print("Table 'Customers' created successfully.")

#Insert Data
cursor.execute(''' INSERT INTO customers (name, email)
               VALUES (%s, %s) ''', ('John Doe', 'john.doe@example.com'))
conn.commit()
print("Sample Data inserted successfully.")

#Query Table for Sample Data

cursor.execute("SELECT * FROM customers;")
customers = cursor.fetchall()

for customer in customers:
    print(customer)


# Close cursor and connection
cursor.close()
conn.close()
print("PostgreSQL connection closed.")
