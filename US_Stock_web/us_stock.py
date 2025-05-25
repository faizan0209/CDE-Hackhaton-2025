from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Setup Chrome
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Optional, comment/uncomment as needed
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
driver.get("https://www.tradingview.com/markets/stocks-usa/market-movers-all-stocks/")
wait = WebDriverWait(driver, 20)

# Click "Load More" button until no more available
click_count = 0
while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        load_more_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "button-SFwfC2e0")))
        driver.execute_script("arguments[0].click();", load_more_btn)
        click_count += 1
        print(f"🔄 Clicked 'Load More' {click_count} times")
        time.sleep(2)
    except:
        print("✅ No more 'Load More' button. Loaded all rows.")
        break

# Get all rows
rows = driver.find_elements(By.CLASS_NAME, "row-RdUXZpkv")
print(f"📈 Total rows found: {len(rows)}")

data = []

# Get headers from first row (usually the first row is headers or use separate header row)
try:
    # Try to get headers from a header row if exists
    header_row = driver.find_element(By.CLASS_NAME, "row-header-RdUXZpkv")
    header_cells = header_row.find_elements(By.TAG_NAME, "div")
    headers = [cell.text.strip() for cell in header_cells if cell.text.strip()]
except:
    # If no separate header row, get headers from first data row
    first_row_cols = rows[0].find_elements(By.TAG_NAME, "td")
    headers = [col.text.strip() for col in first_row_cols]

print(f"📋 Headers found: {headers}")

# Extract all rows data (skipping the header row if it was found separately)
for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    row_data = [col.text.strip() for col in columns]
    if row_data and len(row_data) == len(headers):
        data.append(row_data)

# Convert to DataFrame
df = pd.DataFrame(data, columns=headers)

# Save to CSV
csv_file = 'tradingview_all_stocks_full.csv'
df.to_csv(csv_file, index=False, encoding='utf-8')
print(f"✅ Saved {len(df)} rows to '{csv_file}'")

driver.quit()
