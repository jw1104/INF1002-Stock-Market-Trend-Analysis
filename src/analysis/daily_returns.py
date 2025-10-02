import pandas as pd

def daily_returns(stock_data):
    """
    Calculate the daily percentage returns based on closing prices.
   
    Args:
        stock_data: DataFrame with stock data including Close column
       
    Returns:
        list: List containing percentage changes as numeric values
    """
    percent_data = stock_data.copy()
   
    # Reset index to make Date a column instead of index
    percent_data.reset_index(inplace=True)
   
    # Calculate percent change based on Close prices
    percent_changes = []
   
    for i in range(len(percent_data)):
        if i == 0:
            # First row has no previous day to compare with
            percent_changes.append(None)
        else:
            prev_close = percent_data.at[i - 1, 'Close']  # Get the previous day's close
            current_close = percent_data.at[i, 'Close']  # Get the current day's close
           
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
    stock_data = yf.download(stock, start=start_date, end=end_date).round(2)

    # Calculate simple moving average
    stock_data["SMA"] = (stock_data["Close"].rolling(window=num_periods).mean()).round(2)

    # Remove the extra early dates
    stock_data = stock_data[start_date:]

    stock_data = daily_returns(stock_data)

    print(stock_data)