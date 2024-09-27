import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

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

# Read the CSV file into a DataFrame
df = pd.read_csv('sales_data.csv')

# PostgreSQL connection details
db_config = {
    'username': db_user,
    'password': db_password,
    'host': db_host,
    'port': db_port,
    'database': db_name
}

# Create a connection string
connection_string = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# Create an SQLAlchemy engine
engine = create_engine(connection_string)

# Load data into the sales table
df.to_sql('sales', engine, index=False, if_exists='replace')

print("Data loaded successfully!")

# Close cursor and connection
cursor.close()
conn.close()
print("PostgreSQL connection closed.")