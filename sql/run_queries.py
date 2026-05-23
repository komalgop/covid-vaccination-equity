import pandas as pd
import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
db_path = os.path.join(project_dir, "data", "vaccinations.db")

conn = sqlite3.connect(db_path)

# Query 1: Vaccination rates by race/ethnicity
print("=" * 60)
print("QUERY 1: Vaccination rates by race/ethnicity")
print("=" * 60)
q1 = pd.read_sql("""
    SELECT demographic_category, date,
        administered_dose1_pct_known AS dose1_pct,
        series_complete_pop_pct_known AS fully_vaxxed_pct
    FROM vaccinations
    WHERE demographic_category LIKE 'Race_eth_%'
        AND demographic_category NOT IN ('Race_eth_known', 'Race_eth_unknown')
        AND date = (SELECT MAX(date) FROM vaccinations)
    ORDER BY fully_vaxxed_pct DESC
""", conn)
print(q1.to_string(index=False))

# Query 2: Equity gap over time
print("\n" + "=" * 60)
print("QUERY 2: Equity gap between racial groups over time")
print("=" * 60)
q2 = pd.read_sql("""
    SELECT date,
        MAX(series_complete_pop_pct_known) AS highest_rate,
        MIN(series_complete_pop_pct_known) AS lowest_rate,
        MAX(series_complete_pop_pct_known) - MIN(series_complete_pop_pct_known) AS equity_gap
    FROM vaccinations
    WHERE demographic_category LIKE 'Race_eth_NH%'
        AND series_complete_pop_pct_known IS NOT NULL
        AND series_complete_pop_pct_known > 0
    GROUP BY date
    ORDER BY date
""", conn)
print(q2.to_string(index=False))

# Query 5: Booster dropoff by race
print("\n" + "=" * 60)
print("QUERY 5: Booster dropoff by race")
print("=" * 60)
q5 = pd.read_sql("""
    SELECT demographic_category,
        series_complete_pop_pct_known AS fully_vaxxed_pct,
        booster_doses_pop_pct_known AS booster_pct,
        ROUND(series_complete_pop_pct_known - booster_doses_pop_pct_known, 1) AS booster_dropoff
    FROM vaccinations
    WHERE demographic_category LIKE 'Race_eth_NH%'
        AND date = (SELECT MAX(date) FROM vaccinations)
    ORDER BY booster_dropoff DESC
""", conn)
print(q5.to_string(index=False))

conn.close()
print("\nDone!")
