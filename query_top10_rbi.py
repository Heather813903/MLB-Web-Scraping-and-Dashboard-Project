import sqlite3
import pandas as pd

def get_top_10_rbi_leaders(db_path="mlb_rbi.db"):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # SQL query to sum RBI by player and get top 10
    query = """
    SELECT player, SUM(rbi) AS total_rbi
    FROM rbi_leaders
    GROUP BY player
    ORDER BY total_rbi DESC
    LIMIT 10;
    """

    # Execute query and load results into a DataFrame
    df_top10 = pd.read_sql(query, conn)

    # Close the connection
    conn.close()

    return df_top10

if __name__ == "__main__":
    df = get_top_10_rbi_leaders()
    print("Top 10 all-time RBI leaders:")
    print(df)

