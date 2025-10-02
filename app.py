from flask import Flask, render_template, request
from INF1002_Stock_Market_Trend_Analysis.src.analysis.data_fetcher import data_fetcher
from INF1002_Stock_Market_Trend_Analysis.src.analysis.simple_moving_average import simple_moving_average
from INF1002_Stock_Market_Trend_Analysis.src.analysis.daily_returns import daily_returns
from INF1002_Stock_Market_Trend_Analysis.src.visualization.create_price_sma_chart import create_price_sma_chart
from INF1002_Stock_Market_Trend_Analysis.src.visualization.create_run_direction_chart import create_run_direction_chart

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    price_sma_chart_html = None
    run_direction_chart_html = None
    symbol = ""
    period = ""
    sma_window = ""
    error_message = None

    if request.method == "POST":
        symbol = request.form.get("symbol", "").upper()
        period = request.form.get("period", "").lower()
        sma_window = request.form.get("sma_window", "")

        try:
            # Validate inputs
            if not symbol:
                raise ValueError("Stock symbol is required")
            if not period:
                raise ValueError("Period is required")
            if not sma_window:
                raise ValueError("SMA window is required")
            
            sma_window_int = int(sma_window)
            
            if sma_window_int <= 0:
                raise ValueError("SMA window must be a positive number")
            
            # Fetch stock data
            data = data_fetcher(symbol, period)
            
            # Prepare data for charts
            closing_prices = data["Close"].tolist()
            dates = data.index.strftime("%Y-%m-%d").tolist()
            
            # Validate SMA window size
            if sma_window_int > len(closing_prices):
                raise ValueError(f"SMA window ({sma_window_int}) cannot be larger than data length ({len(closing_prices)})")
            
            # Calculate SMA
            sma_values = simple_moving_average(closing_prices, sma_window_int)
            
            # Pad SMA values to match dates length (add None for initial periods)
            sma_padded = [None] * (sma_window_int - 1) + sma_values
            
            # Create price vs SMA chart
            price_sma_chart_html = create_price_sma_chart(dates, closing_prices, sma_padded, symbol)
            
            # Calculate daily returns
            returns = daily_returns(data)
            
            # Create run direction chart
            run_direction_chart_html = create_run_direction_chart(dates, closing_prices, returns, symbol)
            
        except ValueError as ve:
            error_message = str(ve)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(f"Error: {str(e)}")

    return render_template("index.html",
                           price_sma_chart_html=price_sma_chart_html,
                           run_direction_chart_html=run_direction_chart_html,
                           symbol=symbol,
                           period=period,
                           sma_window=sma_window,
                           error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)