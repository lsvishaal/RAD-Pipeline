import pandas as pd
from random import choice, randint, uniform

# Sample data for demonstration
products = ['Product A', 'Product B', 'Product C']
price_range = {'Product A': (10, 20), 'Product B': (20, 30), 'Product C': (30, 40)}
regions = ['North', 'South', 'East', 'West']
num_rows = 100
duplicate_count = 10

data = []

for i in range(1, num_rows + 1):
    # Generate basic data
    product = choice(products)
    quantity = randint(1, 10)
    price = round(uniform(*price_range[product]), 2)
    region = choice(regions)
    sale_date = '2023-10-01'  # Placeholder date

    # Introduce data issues
    if i % 10 == 0:
        product = '' if randint(0, 1) else product  # Empty product name occasionally
    if i % 15 == 0:
        quantity = None  # Missing quantity occasionally
    if i % 20 == 0:
        price = -price if randint(0, 1) else price  # Negative price error occasionally
    if i % 25 == 0:
        region = ' ' if randint(0, 1) else region  # Invalid region occasionally
    if i % 30 == 0:
        sale_date = 'N/A'  # Invalid date format occasionally

    data.append([product, quantity, price, region, sale_date])

# Create DataFrame
dirty_df = pd.DataFrame(data, columns=['Product', 'Quantity', 'Price', 'Region', 'SaleDate'])

# Duplicate some rows
dirty_df = pd.concat([dirty_df, dirty_df.sample(duplicate_count)], ignore_index=True)

# Save DataFrame to CSV
dirty_df.to_csv('dirty_sales_data.csv', index=False)

print("Data generated and saved to dirty_sales_data.csv successfully!")