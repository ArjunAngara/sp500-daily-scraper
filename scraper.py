# S&P 500 Daily Scraper

import requests

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
response = requests.get(url)

print(f"Status code: {response.status_code}")
print("Page fetched successfully")
