# S&P 500 Daily Scraper

import requests
import yfinance as yf
from bs4 import BeautifulSoup

# test yfinance on one stock before using it on all 500
stock = yf.Ticker("AAPL")
data = stock.history(period="1d")

print("AAPL data:")
print(data)
