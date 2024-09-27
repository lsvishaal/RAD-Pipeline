import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

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

# Initial data preview before cleaning
print("\nInitial Data Preview (Before Cleaning):")
print(df.head())  # Show the first 5 rows before cleaning

# Data Cleaning
df['product'] = df['product'].replace('', np.nan)  # Replace empty product names with NaN
df['quantity'] = df['quantity'].fillna(df['quantity'].median())  # Fill missing quantities with median value
df['price'] = df['price'].fillna(df['price'].mean())  # Fill missing prices with mean value
df['region'] = df['region'].replace('', np.nan)  # Replace empty regions with NaN
df = df.dropna(subset=['region'])  # Drop rows with NaN in 'region'
df['sale_date'] = df['sale_date'].fillna('1970-01-01')  # Fill missing dates with a default date

# Remove duplicates
df = df.drop_duplicates()

# Convert data types
df['quantity'] = df['quantity'].astype(int)  # Convert quantity to integer
df['price'] = df['price'].astype(float)  # Convert price to float
df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')  # Convert sale_date to datetime

# Data preview after cleaning
print("\nData Preview (After Cleaning):")
print(df.head())  # Show the first 5 rows after cleaning

# Save cleaned data to CSV
df.to_csv('cleaned_sales_data.csv', index=False)

# PostgreSQL details
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
