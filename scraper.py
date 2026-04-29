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
            change = round(((current - prev) / prev) * 100, 2)
            vol = int(volume[ticker].dropna().iloc[0
