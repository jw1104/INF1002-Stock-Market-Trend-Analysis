import yfinance as yf
import datetime as dt

def get_date_x_days_before(date_string, num_days_before):
    date_object = dt.datetime.strptime(date_string, "%Y-%m-%d")
    new_date = date_object - dt.timedelta(days=num_days_before)
    new_date_string = new_date.strftime("%Y-%m-%d")
    return new_date_string

stock = "AAPL"
start_date = "2015-01-01"
end_date = "2025-08-31"
num_periods = 20

# Get a few days before the start date to accommodate the period size
start_date_x_days_before = get_date_x_days_before(start_date, num_periods*2)

# Gets the stock data
stock_data = yf.download(stock, start=start_date_x_days_before, end=end_date)

# Calculate simple moving average
stock_data["SMA"] = stock_data["Close"].rolling(window=num_periods).mean()

# Now that we calculated the SMA, we can remove the dates before the actual
# start date that we want.
stock_data = stock_data[start_date:]

# test print SMA
print(stock_data["SMA"])