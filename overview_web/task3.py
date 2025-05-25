from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# TASK 3: Scrape Stock Overview Pages
# Source: TradingView – Stock Overview (Example: https://www.tradingview.com/symbols/NASDAQ-AAPL/)

# ================================
# CONFIGURATION
# ================================
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
# Uncomment below if you want headless (no browser UI)
# options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# ================================
# READ SYMBOLS FROM CSV
# ================================
symbols = []
with open("tradingview_all_stocks.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        symbols.append(row[0])

print(f"🔎 Total symbols to scrape: {len(symbols)}")

# ================================
# SCRAPE DATA
# ================================
data = []
for idx, symbol in enumerate(symbols, 1):
    url = f"https://www.tradingview.com/symbols/{symbol}/"
    driver.get(url)
    
    # Optional: Wait for the page to load completely
    time.sleep(3)
    
    try:
        # Wait for the company header to appear (adjust class name if needed)
        title_element = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "tv-symbol-header__first-line")
        ))
        title = title_element.text.strip()
        
        # Get company description (adjust class name if needed)
        description_element = driver.find_element(
            By.CLASS_NAME, "tv-symbol-profile__description"
        )
        description = description_element.text.strip()
        
        # You can extract additional data here if needed, e.g., industry, sector, market cap
        
        # Add to data list
        data.append([symbol, title, description])
        print(f"✅ {idx}/{len(symbols)}: Fetched data for {symbol}")
    
    except Exception as e:
        print(f"❌ {idx}/{len(symbols)}: Failed for {symbol} — {e}")
        data.append([symbol, "N/A", "N/A"])

# ================================
# SAVE SCRAPED DATA TO CSV
# ================================
output_file = "tradingview_symbol_details.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Symbol', 'Title', 'Description'])  # CSV header
    writer.writerows(data)

print(f"\n✅ Done! Saved detailed data for {len(symbols)} symbols to '{output_file}'.")
driver.quit()
