from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup Chrome
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Optional for headless mode
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

base_url = "https://sarmaaya.pk/mutual-funds/?page={}"
all_data = []

for page in range(1, 26):  # 1 to 25 pages
    url = base_url.format(page)
    driver.get(url)
    print(f"📄 Loading Page {page}...")

    # Optional wait to ensure data loads
    time.sleep(3)

    # Locate table rows
    try:
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows[1:]:  # Skip header row
            cols = row.find_elements(By.TAG_NAME, "td")
            row_data = [col.text.strip() for col in cols]
            if row_data:
                all_data.append(row_data)

    except Exception as e:
        print(f"⚠️ Error on page {page}: {e}")

print(f"📈 Total rows collected: {len(all_data)}")

# Extract headers from the first table
driver.get(base_url.format(1))
time.sleep(3)
table = driver.find_element(By.TAG_NAME, "table")
header_elements = table.find_elements(By.TAG_NAME, "th")
headers = [header.text.strip() for header in header_elements]

driver.quit()

# Save to pandas DataFrame
df = pd.DataFrame(all_data, columns=headers)
csv_file = "sarmaaya_mutual_funds.csv"
df.to_csv(csv_file, index=False, encoding='utf-8')
print(f"✅ Saved {len(df)} rows to '{csv_file}'")
