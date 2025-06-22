import pandas as pd

df = pd.read_csv("data/batting_avg_leaders.csv", skiprows=2)
print("Columns found:", df.columns.tolist())
print(df.head(3))