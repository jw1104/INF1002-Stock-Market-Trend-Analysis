def simple_moving_average(data, window_size):
    sma = data["Close"].rolling(window=window_size).mean() # implement own sma algorithm
    
    return sma