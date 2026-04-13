# S&P 500 Daily Scraper

import requests
import pandas as pd
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

data = yf.download(tickers, period="2d", interval="1d",
                   auto_adjust=True, progress=False)

close = data["Close"]
volume = data["Volume"]
results = []

for ticker in tickers:
    try:
        prices = close[ticker].dropna()
        if len(prices) < 2:
            continue
        prev = round(float(prices.iloc[-2]), 2)
        current = round(float(prices.iloc[-1]), 2)
        change = round(((current - prev) / current) * 100, 2)
        vol = int(volume[ticker].dropna().iloc[0])
        results.append({"Ticker": ticker, "Previous Close": prev,
                        "Current Price": current, "Daily Change (%)": change,
                        "Volume": vol})
    except Exception:
        continue

df = pd.DataFrame(results)
print(df.head(10))
