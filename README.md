Here’s a simple README for your project:

---

# PostgreSQL CSV Import Project

This project demonstrates how to import data from a CSV file into a PostgreSQL database using Python. The project focuses on creating a table in PostgreSQL to store product orders and then importing data from a CSV file into the table. 

## Project Structure

- **`Main.py`**: The Python script that connects to the PostgreSQL database, creates an `orders` table, and imports data from the `MOCK_DATA.csv` file into the table.
- **`MOCK_DATA.csv`**: A sample CSV file containing mock order data with fields such as `product_id`, `customer_id`, `quantity`, `price`, and `date`.
- **`.env`**: This file contains the database credentials (host, port, database name, username, and password) used to connect to the PostgreSQL instance.

## Prerequisites

1. **Python 3** installed on your machine.
2. **PostgreSQL** instance (in this case, hosted on Render.com).
3. The following Python libraries:
   - `psycopg2` for connecting to PostgreSQL.
   - `dotenv` for managing environment variables.

You can install the required libraries using:
```bash
pip install psycopg2 python-dotenv
```

## How It Works

1. **Connection**: The script connects to your PostgreSQL database using credentials stored in the `.env` file.
   
2. **Table Creation**: If the `orders` table doesn't already exist, the script creates it with columns that match the structure of the CSV file (`product_id`, `customer_id`, `quantity`, `price`, and `date`).

3. **CSV Import**: The script reads the `MOCK_DATA.csv` file line by line, skipping the header row, and inserts each row of data into the `orders` table.

4. **Verification**: After inserting the data, the script fetches all rows from the `orders` table and prints them to verify the data insertion.

## Instructions

1. **Clone the project** to your local machine.
   ```bash
   git clone <repository-url>
   ```

2. **Set up the `.env` file** in the root directory with your PostgreSQL credentials:
   ```bash
   DB_HOST=<your-host>
   DB_NAME=<your-database-name>
   DB_USER=<your-username>
   DB_PASSWORD=<your-password>
   DB_PORT=<your-port>
   ```

3. **Run the script**:
   ```bash
   python Main.py
   ```

4. The script will:
   - Connect to the PostgreSQL database.
   - Create the `orders` table (if it doesn't already exist).
   - Import data from `MOCK_DATA.csv` into the `orders` table.
   - Print all the data from the table for verification.

## Example of CSV File (`MOCK_DATA.csv`)

```
product_id,customer_id,quantity,price,date
1,1,22,76,3/17/2024
2,2,22,96,10/7/2023
3,3,52,92,1/16/2024
4,4,46,28,12/24/2023
5,5,27,44,10/29/2023
6,6,69,80,2/3/2024
7,7,75,79,10/21/2023
8,8,9,95,1/2/2024
9,9,48,32,12/9/2023
10,10,30,28,6/30/2024
```

## Future Phases

- **Phase 3** will involve querying data and generating insights (e.g., summarizing customer purchases or analyzing trends).
- **Phase 4** will expand the complexity of the dataset or use additional data sources (e.g., external APIs).

---

## License

This project is open-source and available for modification or expansion.

---

