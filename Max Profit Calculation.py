import yfinance as yf
import datetime as dt

def get_date_x_days_before(date_string, num_days_before):
    date_object = dt.datetime.strptime(date_string, "%Y-%m-%d")
    new_date = date_object - dt.timedelta(days=num_days_before)
    new_date_string = new_date.strftime("%Y-%m-%d")
    return new_date_string

stock = "AAPL"
start_date = "2025-08-01"
end_date = "2025-08-08"  # Shorter range for intraday data
num_periods = 20
intervals = ["1y", "3mo", "1mo", "1d"]

start_date_x_days_before = get_date_x_days_before(start_date, num_periods*2)


for interval in intervals:
    print(f"\nDownloading data for interval: {interval}")
    stock_data = yf.ticker(stock).history(period=interval)

    # Find max profit (buy low, sell high, one transaction)
    #For each interval, it will show the best buy/sell times, prices, and the profit you could have made.
    if not stock_data.empty and 'Close' in stock_data:
        close_prices = stock_data['Close'].values
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
            buy_date = stock_data.index[buy_time]
            sell_date = stock_data.index[sell_time]
            print(f"Max profit for {interval}: ${max_profit:.2f} (Buy at {min_price:.2f} on {buy_date}, Sell at {close_prices[sell_time]:.2f} on {sell_date})")
        else:
            print(f"No profit opportunity for {interval} interval.")
    else:
        print(f"No data for {interval} interval.")
