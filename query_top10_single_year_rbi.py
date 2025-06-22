import sqlite3
import pandas as pd

def get_top_10_rbi_seasons(db_path="mlb_rbi.db"):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)

    # SQL query: top 10 RBI performances by year
    query = """
    SELECT year, player, team, rbi
    FROM rbi_leaders
    ORDER BY rbi DESC
    LIMIT 10;
    """

    # Load results into DataFrame
    df_top10 = pd.read_sql(query, conn)

    # Close DB connection
    conn.close()

    return df_top10

if __name__ == "__main__":
    df = get_top_10_rbi_seasons()
    print("Top 10 single-season RBI performances:")
    print(df)

  











