import pandas as pd

def daily_returns(data):
    close_price = data["Close"]
    price_changes = close_price.pct_change() * 100

    return price_changes