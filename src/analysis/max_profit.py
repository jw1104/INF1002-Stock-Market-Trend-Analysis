import yfinance as yf
import datetime as dt
from data_fetcher import data_fetcher

def max_profit(data):
    close_prices = data['Close']
    
    min_price = float('inf') #set to infinity initially to check for min
    max_profit = 0.0
    buy_time = sell_time = None # Initialize buy and sell times
    for i, price in enumerate(close_prices):
        if price < min_price:
            min_price = price
            min_index = i
        profit = price - min_price
        if profit > max_profit:
            max_profit = profit
            buy_time = min_index
            sell_time = i
    if max_profit > 0 and buy_time is not None and sell_time is not None:
        buy_date = data.index[buy_time].strftime("%Y-%m-%d")
        buy_price = data["Close"].iloc[buy_time]
        sell_date = data.index[sell_time].strftime("%Y-%m-%d")
        sell_price = data["Close"].iloc[sell_time]
        
        return {
            "max_profit": round(max_profit, 2),
            "buy_date": buy_date,
            "buy_price": buy_price.round(2),
            "sell_date": sell_date,
            "sell_price": sell_price.round(2)
        }
    else:
        raise ValueError(f"No profit opportunity.")