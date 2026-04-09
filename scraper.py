# S&P 500 Daily Scraper

import requests
import yfinance as yf
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

data = yf.download(tickers[:20], period="2d", interval="1d",
                   auto_adjust=True, progress=False)

close = data["Close"]

for ticker in tickers[:10]:
    try:
        prices = close[ticker].dropna()
        if len(prices) < 2:
            continue
        prev = float(prices.iloc[-2])
        current = float(prices.iloc[-1])
        change = round(((current - prev) / current) * 100, 2)
        print(f"{ticker}: {change}%")
    except Exception:
        continue
