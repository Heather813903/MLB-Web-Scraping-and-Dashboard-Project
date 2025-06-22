import sqlite3
import pandas as pd

def get_top_10_all_time_rbi_with_years(db_path="mlb_rbi.db"):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # SQL query: total RBI + count of distinct seasons
    query = """
    SELECT 
        player, 
        COUNT(DISTINCT year) AS seasons_played,
        SUM(rbi) AS total_rbi
    FROM rbi_leaders
    GROUP BY player
    ORDER BY total_rbi DESC
    LIMIT 10;
    """

    # Run query and load into DataFrame
    df_top10 = pd.read_sql(query, conn)

    # Close the connection
    conn.close()

    return df_top10

if __name__ == "__main__":
    df = get_top_10_all_time_rbi_with_years()
    print("Top 10 All-Time RBI Leaders (with seasons played):")
    print(df)




