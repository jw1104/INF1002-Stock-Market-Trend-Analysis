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
    sma_short = ""
    sma_medium = ""
    sma_long = ""
    error_message = None

    if request.method == "POST":
        symbol = request.form.get("symbol", "").upper()
        period = request.form.get("period", "").lower()
        sma_short = request.form.get("sma_short", "")
        sma_medium = request.form.get("sma_medium", "")
        sma_long = request.form.get("sma_long", "")

        try:
            # Validate inputs
            if not symbol:
                raise ValueError("Stock symbol is required")
            if not period:
                raise ValueError("Period is required")
            if not sma_short or not sma_medium or not sma_long:
                raise ValueError("All SMA windows are required")
            
            sma_short_int = int(sma_short)
            sma_medium_int = int(sma_medium)
            sma_long_int = int(sma_long)
            
            if sma_short_int <= 0 or sma_medium_int <= 0 or sma_long_int <= 0:
                raise ValueError("SMA windows must be positive numbers")
            
            if not (sma_short_int < sma_medium_int < sma_long_int):
                raise ValueError("SMA windows must be in ascending order (Short < Medium < Long)")
            
            # Fetch stock data
            data = data_fetcher(symbol, period)
            
            if data is None or data.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
            # Prepare data for charts
            closing_prices = data["Close"].tolist()
            dates = data.index.strftime("%Y-%m-%d").tolist()
            
            # Validate SMA window sizes
            max_window = max(sma_short_int, sma_medium_int, sma_long_int)
            if max_window > len(closing_prices):
                raise ValueError(f"Largest SMA window ({max_window}) cannot be larger than data length ({len(closing_prices)})")
            
            # Calculate multiple SMAs
            sma_short_values = simple_moving_average(closing_prices, sma_short_int)
            sma_medium_values = simple_moving_average(closing_prices, sma_medium_int)
            sma_long_values = simple_moving_average(closing_prices, sma_long_int)
            
            # Pad SMA values to match dates length
            sma_short_padded = [None] * (sma_short_int - 1) + sma_short_values
            sma_medium_padded = [None] * (sma_medium_int - 1) + sma_medium_values
            sma_long_padded = [None] * (sma_long_int - 1) + sma_long_values
            
            # Create dictionary of SMA data
            sma_data = {
                'short': {'values': sma_short_padded, 'period': sma_short_int},
                'medium': {'values': sma_medium_padded, 'period': sma_medium_int},
                'long': {'values': sma_long_padded, 'period': sma_long_int}
            }
            
            # Create price vs multiple SMA chart
            price_sma_chart_html = create_price_sma_chart(dates, closing_prices, sma_data, symbol)
            
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
                           sma_short=sma_short,
                           sma_medium=sma_medium,
                           sma_long=sma_long,
                           error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)