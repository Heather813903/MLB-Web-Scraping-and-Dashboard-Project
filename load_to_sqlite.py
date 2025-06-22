import sqlite3
import pandas as pd
import os

# Load cleaned data
csv_path = "data/rbi_leaders_clean.csv"
if not os.path.exists(csv_path):
    print(" Cleaned CSV not found. Please run the scraper first.")
    exit()

df = pd.read_csv(csv_path)

# Create/connect to SQLite database
conn = sqlite3.connect("mlb_rbi.db")
cursor = conn.cursor()

# Drop table if it already exists (for reruns)
cursor.execute("DROP TABLE IF EXISTS rbi_leaders")

# Create table
cursor.execute("""
CREATE TABLE rbi_leaders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER,
    player TEXT,
    team TEXT,
    rbi INTEGER
)
""")

# Insert data into the table
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO rbi_leaders (year, player, team, rbi)
        VALUES (?, ?, ?, ?)
    """, (row["Year"], row["Player"], row["Team"], row["RBI"]))

# Commit and close
conn.commit()
print(f" Inserted {len(df)} rows into mlb_rbi.db (table: rbi_leaders)")
conn.close()
