
import pandas as pd
from database import engine
from sqlalchemy import text

# Read cleaned CSV file
df = pd.read_csv("data/cleaned_ecommerce.csv")

# Display dataset information
print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Upload dataset to PostgreSQL
df.to_sql(
    name="ecommerce_sales",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=1000
)

print("Dataset uploaded successfully!")

# Verify uploaded records
with engine.connect() as connection:
    from sqlalchemy import text

    result = connection.execute(
        text("SELECT COUNT(*) FROM ecommerce_sales")
    )

    print("Records in database:", result.scalar())

print("Starting database upload...")

df.to_sql(
    name="ecommerce_sales",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=1000
)

print("Dataset uploaded successfully!")

import pandas as pd

df = pd.read_csv("data/cleaned_ecommerce.csv")

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())