import datetime as dt
import yfinance as yf
import pandas as pd

def get_date_x_days_before(date_string, num_days_before):
    date_object = dt.datetime.strptime(date_string, "%Y-%m-%d")
    new_date = date_object - dt.timedelta(days=num_days_before)
    new_date_string = new_date.strftime("%Y-%m-%d")
    return new_date_string

def add_percent_change_column(stock_data):
    percent_data = stock_data.copy()

    # Reset index to make Date a column instead of index
    percent_data.reset_index(inplace=True)

    # Rename columns
    percent_data.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume', "SMA"]

    for i in range(len(percent_data)):
        if i == 0:
            # First row has no previous day to compare with
            percent_data.at[i, '% Change'] = None
        else:
            prev_close = percent_data.at[i - 1, 'SMA']  # Get the previous day data
            current_close = percent_data.at[i, 'SMA']  # Get the current day data
            percent_change = ((current_close - prev_close) / prev_close) * 100
            percent_data.at[i, '% Change'] = round(percent_change, 2)
    # Convert the value return to a string that has + and % sign and missing value as N/A
    percent_data['% Change'] = percent_data['% Change'].apply(
        lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A"
    )

    # Set pandas display options for left alignment
    pd.set_option('display.colheader_justify', 'left')
    pd.set_option('display.unicode.east_asian_width', False)

    percent_data = percent_data.to_string(index=False, justify='left')

    return percent_data


# Ask user for stock symbol and number of days
stock = "AAPL"
start_date = "2015-01-01"
end_date = "2025-08-31"
num_periods = 20

# Get a few days before the start date to accommodate the period size
start_date_x_days_before = get_date_x_days_before(start_date, num_periods*2)

# Grab the stock data
stock_data = yf.download(stock, start=start_date, end=end_date).round(2)

# Calculate simple moving average
stock_data["SMA"] = (stock_data["Close"].rolling(window=num_periods).mean()).round(2)

# Remove the extra early dates
stock_data = stock_data[start_date:]

stock_data = add_percent_change_column(stock_data)

print(stock_data)
