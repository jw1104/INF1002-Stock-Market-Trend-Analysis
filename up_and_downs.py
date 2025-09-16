import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Download historical price data
ticker = "AAPL"
df = yf.download(ticker, start="2023-01-01", end="2025-12-31", auto_adjust=True, progress=False)
df = df[['Close']].copy()
df.reset_index(inplace=True)  # Ensure 'Date' is a column

# Step 2: Detect upward and downward runs
runs = []
start_idx = 0
direction = 0  # 1 = up, -1 = down, 0 = flat

for i in range(1, len(df)):
    prev_price = df['Close'].iloc[i - 1]
    curr_price = df['Close'].iloc[i]
    delta = np.sign(curr_price - prev_price).item()  #Ensure scalar float

    if delta == direction:
        continue
    else:
        if direction != 0:
            runs.append((start_idx, i - 1, direction))
        start_idx = i - 1
        direction = delta

# Add the last run
if direction != 0:
    runs.append((start_idx, len(df) - 1, direction))

# Step 3: Plot the price chart with highlighted runs
plt.figure(figsize=(14,6))
plt.plot(df['Date'], df['Close'], color='lightgray', label='Close Price')

for start, end, direction in runs:
    color = 'green' if direction == 1 else 'red'
    plt.plot(df['Date'].iloc[start:end+1], df['Close'].iloc[start:end+1], color=color, linewidth=2)

plt.title(f"{ticker} Price Chart with Highlighted Runs (Up = Green, Down = Red)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
