# S&P 500 Daily Scraper

import requests
import yfinance as yf
from bs4 import BeautifulSoup

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

for ticker in tickers:
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if not data.empty:
        price = round(data["Close"].iloc[-1], 2)
        print(f"{ticker}: ${price}")
