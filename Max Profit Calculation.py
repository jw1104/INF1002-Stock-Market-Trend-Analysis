def get_date_x_days_before(date_string, num_days_before):
import yfinance as yf

stock = "AAPL"
start_date = "2025-08-01"
end_date = "2025-08-08"  # Shorter range for intraday data
intervals = ["1d", "1h", "5m", "1m"]

for interval in intervals:
    print(f"\nDownloading data for interval: {interval}")
    stock_data = yf.download(stock, start=start_date, end=end_date, interval=interval)
    if not stock_data.empty and 'Close' in stock_data:
        close_prices = stock_data['Close'].values
        min_price = float('inf')
        max_profit = 0.0
        buy_time = sell_time = None
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
