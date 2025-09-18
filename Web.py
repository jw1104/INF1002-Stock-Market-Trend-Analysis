from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    stock_data = None
    chart_html = None
    symbol = ""
    start = ""
    end = ""
    sma_period = 20  # You can change this or make it dynamic later

    if request.method == "POST":
        symbol = request.form["symbol"].upper()
        start = request.form["start"]
        end = request.form["end"]

        try:
            stock = yf.Ticker(symbol)
            if start and end:
                hist = stock.history(start=start, end=end)
            else:
                hist = stock.history(period="10d")

            if not hist.empty:
                # Clean up unused columns
                hist = hist.drop(columns=[col for col in ["Dividends", "Stock Splits"] if col in hist.columns])
                hist = hist.reset_index()

                # Calculate SMA starting from the first data point
                hist["SMA"] = hist["Close"].rolling(window=sma_period, min_periods=1).mean()

                # Format table values
                hist_formatted = hist.copy()
                hist_formatted["Date"] = pd.to_datetime(hist_formatted["Date"]).dt.strftime("%Y-%m-%d")
                hist_formatted["Open"] = hist["Open"].map("${:.2f}".format)
                hist_formatted["High"] = hist["High"].map("${:.2f}".format)
                hist_formatted["Low"] = hist["Low"].map("${:.2f}".format)
                hist_formatted["Close"] = hist["Close"].map("${:.2f}".format)
                hist_formatted["SMA"] = hist["SMA"].map(lambda x: "${:.2f}".format(x) if pd.notna(x) else "—")
                hist_formatted["Volume"] = hist["Volume"].map("{:,}".format)

                stock_data = hist_formatted.to_html(classes="table table-striped", index=False)

                # Detect upward/downward runs
                runs = []
                start_idx = 0
                direction = 0  # 1 = up, -1 = down, 0 = flat
                close_prices = hist["Close"].tolist()

                for i in range(1, len(close_prices)):
                    delta = np.sign(close_prices[i] - close_prices[i - 1])
                    if delta == direction:
                        continue
                    else:
                        if direction != 0:
                            runs.append((start_idx, i - 1, direction))
                        start_idx = i - 1
                        direction = delta

                if direction != 0:
                    runs.append((start_idx, len(close_prices) - 1, direction))

                # Create Plotly figure
                fig = go.Figure()

                # Base gray closing price line
                fig.add_trace(go.Scatter(
                    x=hist["Date"],
                    y=hist["Close"],
                    mode="lines",
                    line=dict(color="lightgray", width=1),
                    name="Close Price"
                ))

                # Add SMA line (starts from first date)
                fig.add_trace(go.Scatter(
                    x=hist["Date"],
                    y=hist["SMA"],
                    mode="lines",
                    line=dict(color="blue", width=2),
                    name=f"{sma_period}-Day SMA"
                ))

                # Highlight runs
                for start_run, end_run, dir_run in runs:
                    color = 'green' if dir_run == 1 else 'red'
                    fig.add_trace(go.Scatter(
                        x=hist["Date"].iloc[start_run:end_run + 1],
                        y=hist["Close"].iloc[start_run:end_run + 1],
                        mode="lines",
                        line=dict(color=color, width=2),
                        name="Up Run" if dir_run == 1 else "Down Run",
                        showlegend=False
                    ))

                fig.update_layout(
                    title=f"{symbol} Price Chart with {sma_period}-Day SMA and Runs",
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    template="plotly_white",
                    height=500
                )

                chart_html = fig.to_html(full_html=False)

            else:
                stock_data = "<p>No data found for that symbol and period.</p>"

        except Exception as e:
            stock_data = f"<p>Error: {str(e)}</p>"

    return render_template("index.html",
                           stock_data=stock_data,
                           chart_html=chart_html,
                           symbol=symbol,
                           start=start,
                           end=end)

if __name__ == "__main__":
    app.run(debug=True)
