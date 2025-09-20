import yfinance as yf
from .utils.clean_data import clean_data

def data_fetcher(ticker, period):
    ticker = ticker.upper()
    period = period.lower()
    stock_data = yf.Ticker(ticker).history(period)
    cleaned_data = clean_data(stock_data)
    
    return cleaned_data
