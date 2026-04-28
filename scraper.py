# S&P 500 Daily Scraper

import os
import datetime
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup


def get_tickers():
    print("Scraping tickers from Wikipedia...")
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    tickers = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if cells:
            ticker = cells[0].get_text(strip=True)
            ticker = ticker.replace(".", "-")
            tickers.append(ticker)
    print(f"Found {len(tickers)} tickers")
    return tickers


def get_prices(tickers):
    print("Fetching price data, this takes a minute...")
    data = yf.download(tickers, period="2d", interval="1d",
                       auto_adjust=True, progress=False)
    close = data["Close"]
    volume = data["Volume"]
    results = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                            "Volume": vol, "Timestamp": timestamp})
        except Exception:
            continue
    print(f"Got data for {len(results)} stocks")
    return pd.DataFrame(results)


def save_csv(df):
    os.makedirs("output", exist_ok=True)
    filename = datetime.datetime.now().strftime("sp500_%Y%m%d_%H%M%S.csv")
    filepath = os.path.join("output", filename)
    df.sort_values("Daily Change (%)", ascending=False, inplace=True)
    df.to_csv(filepath, index=False)
    print(f"Saved to {filepath}")


def show_summary(df):
    avg = round(df["Daily Change (%)"].mean(), 2)
    print(f"\nAverage market change: {avg}%")

    print("\n--- Top 5 Gainers ---")
    for _, row in df.nlargest(5, "Change (%)").iterrows():
        print(f"  {row['Ticker']}: +{row['Daily Change (%)']}%")

    print("\n--- Top 5 Losers ---")
    for _, row in df.nsmallest(5, "Change (%)").iterrows():
        print(f"  {row['Ticker']}: {row['Daily Change (%)']}%")


tickers = get_tickers()
df = get_prices(tickers)
save_csv(df)
show_summary(df)
