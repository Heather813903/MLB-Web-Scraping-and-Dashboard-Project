import sqlite3
import pandas as pd
import os

DB_PATH = "mlb_stats.db"

def import_csv_to_db(csv_path, table_name, conn, dtype_map=None):
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return
    df = pd.read_csv(csv_path)

    if dtype_map:
        for col, dtype in dtype_map.items():
            try:
                df[col] = df[col].astype(dtype)
            except Exception as e:
                print(f"Warning: Could not convert column {col} to {dtype}: {e}")

    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f" Imported {len(df)} rows into table '{table_name}'")

def main():
    conn = sqlite3.connect(DB_PATH)

    # Re-import RBI Leaders (optional)
    import_csv_to_db(
        "data/rbi_leaders_clean.csv",
        "rbi_leaders",
        conn,
        dtype_map={"Year": int, "Player": str, "Team": str, "RBI": int}
    )

    #  Re-import Cleaned Batting Avg Leaders
    import_csv_to_db(
        "data/batting_avg_leaders_clean.csv",
        "batting_avg_leaders",
        conn,
        dtype_map={"Player": str, "BattingAverage": float}
    )

    conn.commit()
    conn.close()
    print(" Database import complete.")

if __name__ == "__main__":
    main()