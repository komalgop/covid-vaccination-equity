import pandas as pd
import sqlite3
import os

# Load the CSV we downloaded
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
csv_path = os.path.join(project_dir, "data", "raw", "cdc_vaccination_data.csv")
db_path = os.path.join(project_dir, "data", "vaccinations.db")

print("Loading CSV into SQLite database...")
df = pd.read_csv(csv_path)

# Clean up the date column
df["date"] = pd.to_datetime(df["date"]).dt.date

# Create database and load data
conn = sqlite3.connect(db_path)
df.to_sql("vaccinations", conn, if_exists="replace", index=False)

# Verify it worked
row_count = pd.read_sql("SELECT COUNT(*) as total FROM vaccinations", conn).iloc[0, 0]
print(f"Loaded {row_count} rows into vaccinations table")

# Show the demographic categories available
categories = pd.read_sql("SELECT DISTINCT demographic_category FROM vaccinations", conn)
print(f"\nDemographic categories:\n{categories.to_string(index=False)}")

conn.close()
print(f"\nDatabase saved to {db_path}")
