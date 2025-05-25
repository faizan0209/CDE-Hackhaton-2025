import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

all_data = []

base_url = "https://www.tradingview.com/markets/stocks-usa/market-movers-all-stocks/"
headers = {"User-Agent": "Mozilla/5.0"}

# Manually set total_pages based on total stocks (4574) and estimated stocks per page (100)
total_pages = 46  # You can adjust this number based on actual site inspection

for page_num in range(1, total_pages + 1):
    print(f"Scraping page {page_num} of {total_pages}...")
    url = f"{base_url}?page={page_num}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_num}, status code: {response.status_code}")
        continue  # Skip this page and move to the next one
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Parse stock data - adjust selectors based on actual HTML structure
    rows = soup.select(".tv-data-table__row")
    if not rows:
        print(f"No data rows found on page {page_num}")
    
    for row in rows:
        try:
            symbol = row.select_one(".tv-screener__symbol").text.strip()
            company = row.select_one(".tv-screener__description").text.strip()
            price = row.select_one(".tv-screener__last").text.strip()
            change = row.select_one(".tv-screener__change").text.strip()
            data = {
                "Symbol": symbol,
                "Company": company,
                "Price": price,
                "Change": change
            }
            all_data.append(data)
        except Exception as e:
            print(f"Error parsing row on page {page_num}: {e}")
    
    time.sleep(1)  # Delay to respect rate limits

# Save to CSV
df = pd.DataFrame(all_data)
df.to_csv("us_stock_symbols.csv", index=False)
print("Scraping completed. Data saved to us_stock_symbols.csv.")
