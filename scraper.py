# S&P 500 Daily Scraper

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
           "NVDA", "META", "JPM", "V", "BRK-B"]

print(f"Tracking {len(tickers)} stocks:")
for i, ticker in enumerate(tickers, 1):
    print(f"  {i}. {ticker}")
