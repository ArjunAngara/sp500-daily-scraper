# S&P 500 Daily Scraper

import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", {"id": "constituents"})
tickers = []

for row in table.find_all("tr")[1:]:
    cells = row.find_all("td")
    if cells:
        ticker = cells[0].get_text(strip=True)
        tickers.append(ticker)

print(f"Found {len(tickers)} tickers")
print(tickers[:10])
