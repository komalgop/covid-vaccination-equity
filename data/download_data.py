import pandas as pd
import os

# Download CDC COVID-19 vaccination data by demographic group
url = "https://data.cdc.gov/resource/km4m-vcsb.csv?$limit=50000"

print("Downloading CDC vaccination data...")
df = pd.read_csv(url)

print(f"Downloaded {len(df)} rows and {len(df.columns)} columns")
print(f"\nColumns: {list(df.columns)}")
print(df.head(3))

# Save raw data
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
output_path = os.path.join(project_dir, "data", "raw", "cdc_vaccination_data.csv")

df.to_csv(output_path, index=False)
print(f"\nSaved to {output_path}")
