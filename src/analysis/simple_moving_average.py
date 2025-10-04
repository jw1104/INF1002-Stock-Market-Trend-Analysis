def simple_moving_average(closing_prices, window_size):

    sma = []
    
    # Loop through the data to calculate the moving average
    for i in range(len(closing_prices) - window_size + 1):
        window = closing_prices[i:i + window_size]  # Get the slice for the current window
        window_average = sum(window) / window_size  # Calculate the average for this window
        sma.append(window_average)  # Append the average to the sma list
    
    return sma
    
    #sma = data["Close"].rolling(window=window_size).mean() # another way to find SMA
    
    #return sma