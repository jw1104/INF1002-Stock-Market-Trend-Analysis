import pandas as pd

def daily_returns(closing_prices):
    """
    Calculate the daily percentage returns based on closing prices.
   
    Args:
        closing_prices: Series of closing prices
       
    Returns:
        list: List containing percentage changes as numeric values
    """
    
    percent_changes = []
   
    for i in range(len(closing_prices)):
        if i == 0:
            # First row has no previous day to compare with
            percent_changes.append(None)
        else:
            prev_close = closing_prices[i - 1]  # Get the previous day's close
            current_close = closing_prices[i]  # Get the current day's close
           
            # Handle cases where Close might be None or NaN
            if pd.notna(prev_close) and pd.notna(current_close) and prev_close != 0:
                percent_change = ((current_close - prev_close) / prev_close) * 100
                percent_changes.append(round(percent_change, 2))
            else:
                percent_changes.append(None)
   
    return percent_changes


if __name__ == "__main__":
    import yfinance as yf
    stock = "AAPL"
    start_date = "2015-01-01"
    end_date = "2025-08-31"
    num_periods = 20


    # Grab the stock data
    stock_data = yf.Ticker(stock).history('3y')

    # Calculate simple moving average
    # stock_data["SMA"] = (stock_data["Close"].rolling(window=num_periods).mean()).round(2)

    # Remove the extra early dates
    # stock_data = stock_data[start_date:]

    stock_data = daily_returns(stock_data["Close"])

    print(stock_data)