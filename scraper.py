# S&P 500 Daily Scraper

import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", {"id": "constituents"})
print("Found table:", table is not None)
