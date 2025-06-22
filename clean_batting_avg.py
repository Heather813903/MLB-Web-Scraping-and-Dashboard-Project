import pandas as pd

# Skip the first two rows: one is a fake header, one is the real header
df = pd.read_csv("data/batting_avg_leaders.csv", skiprows=2)

# Rename columns to expected names
df.columns = ["Player", "BattingAverage", "Rank"]

# Clean batting averages: remove parentheses and round to 3 decimal places
df["BattingAverage"] = df["BattingAverage"].str.extract(r"(\.\d+)").astype(float).round(3)

# Drop the Rank column (optional)
df = df.drop(columns=["Rank"])

# Save the cleaned version
df.to_csv("data/batting_avg_leaders_clean.csv", index=False)
print(" Cleaned and saved to data/batting_avg_leaders_clean.csv")


