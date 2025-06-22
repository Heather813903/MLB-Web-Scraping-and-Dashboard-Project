import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# --- SCRAPE RBI LEADERS ---
url_rbi = "https://www.baseball-almanac.com/hitting/hirbi5.shtml"
print(f"Scraping data from: {url_rbi}")
driver.get(url_rbi)

wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
time.sleep(2)  # <-- wait for full render

table = driver.find_element(By.XPATH, "//table[.//td[contains(text(), 'RBI')]]")
rows = table.find_elements(By.TAG_NAME, "tr")

rbi_data = []

for row in rows[1:]:  # Skip header row
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 4:
        try:
            year = cols[0].text.strip()
            player = cols[1].text.strip()
            rbi = cols[2].text.strip().replace(",", "")
            team = cols[3].text.strip()

            if rbi.isdigit():
                rbi_data.append({
                    "Year": year,
                    "Player": player,
                    "Team": team,
                    "RBI": int(rbi)
                })
        except Exception as e:
            print(f" Error parsing row: {e}")

if rbi_data:
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(rbi_data)
    df.to_csv("data/rbi_leaders_clean.csv", index=False)
    print(f" Saved {len(df)} rows to data/rbi_leaders_clean.csv")
else:
    print(" No RBI data scraped.")

# --- SCRAPE BATTING AVERAGE LEADERS ---
url_avg = "https://www.baseball-almanac.com/hitting/hibavg1.shtml"
print(f"Scraping data from: {url_avg}")
driver.get(url_avg)

batting_data = []

try:
    # Wait up to 10 seconds for the table to be present
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # Locate the table that contains the 'AVG' header cell
    table_avg = driver.find_element(By.XPATH, "//table[.//td[contains(text(), 'AVG')]]")
    rows_avg = table_avg.find_elements(By.TAG_NAME, "tr")

    batting_data = []

    for row in rows_avg[1:11]:  # Grab only top 10 rows, skipping header
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 2:
            try:
                player = cols[0].text.strip()
                avg_raw = cols[1].text.strip()
                avg_clean = avg_raw.split(" ")[0]  # Remove anything after space (like parentheses)
                batting_data.append({
                    "Player": player,
                    "BattingAverage": float(avg_clean)
                })
            except Exception as e:
                print(f"Error parsing batting average row: {e}")

except Exception as e:
    print(f"Failed to scrape batting average data: {e}")

if batting_data:
    import os
    import pandas as pd

    os.makedirs("data", exist_ok=True)
    df_batting = pd.DataFrame(batting_data)
    df_batting.to_csv("data/batting_avg_leaders.csv", index=False)
    print(f"Saved {len(df_batting)} rows to data/batting_avg_leaders.csv")
else:
    print("No batting average data scraped.")