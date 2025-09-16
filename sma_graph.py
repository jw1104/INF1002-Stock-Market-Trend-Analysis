import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt

def get_date_x_days_before(date_string, num_days_before):
    date_object = dt.datetime.strptime(date_string, "%Y-%m-%d")
    new_date = date_object - dt.timedelta(days=num_days_before)
    new_date_string = new_date.strftime("%Y-%m-%d")
    return new_date_string

stock       = "AAPL"
start_date  = "2025-01-01"
end_date    = "2025-08-31"
num_periods = 20

# Get a few days before the start date to accommodate the period size
start_date_x_days_before = get_date_x_days_before(start_date, num_periods*2)

# Grab the stock data
stock_data = yf.download(stock, start=start_date_x_days_before, end=end_date)

# Compute the simple moving average (SMA)
stock_data["SMA"] = stock_data["Close"].rolling(window=num_periods).mean()

# Now that we calculated the SMA, we can remove the dates before the actual
# start date that we want.
stock_data = stock_data[start_date:]
# print(stock_data["SMA"])
plt.plot(stock_data["SMA"], label='SMA', color='blue')
plt.plot(stock_data["Close"], label='Closing Price', color='brown')

plt.title("Apple Stock Closing Prices VS SMA (2022)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid()
plt.show()

