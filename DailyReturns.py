import yfinance as yf
import pandas as pd


def stock_percentage_change(ticker, period):
    """
    Fetches stock data from Yahoo Finance and calculates day-to-day % change.

    Parameters:
        ticker (str): Stock symbol (e.g., "AAPL", "TSLA").
        period (str): Time period (e.g., "5d", "1mo", "3mo", "1y").

    Returns:
        DataFrame: Date, Close price, and % Change
    """
    # Download stock data
    data = yf.download(symbol, period=period)

    if data.empty:
        print("No data found. Check the ticker symbol or period.")
        return None

    # Keep only the closing prices
    data = data[["Close"]].copy()

    # Calculate daily % change
    data["% Change"] = data["Close"].pct_change() * 100

    # Round values
    data["Close"] = data["Close"].round(2)
    data["% Change"] = data["% Change"].round(2)

    # Format with $ and %
    data["Close"] = data["Close"].map(lambda x: f"${x:.2f}")
    data["% Change"] = data["% Change"].map(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")

    return data


# Example usage:
if __name__ == "__main__":
    symbol = input("Enter stock symbol (e.g., AAPL, TSLA, MSFT): ").upper()
    period = input("Enter period (e.g., 5d, 1mo, 3mo, 1y): ")
    result = stock_percentage_change(symbol, period)
    print(result)
