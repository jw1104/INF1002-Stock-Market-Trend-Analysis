from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    stock_data = None
    chart_data = None
    symbol = ""   # default
    start = ""
    end = ""

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
            # Remove Dividends and Stock Splits columns if they exist
            hist = hist.drop(columns=[col for col in ["Dividends", "Stock Splits"] if col in hist.columns])

            #Converts the Date index into a normal column so it aligns with
            hist = hist.reset_index()

            hist_formatted = hist.copy()
            hist_formatted["Date"] = pd.to_datetime(hist_formatted["Date"]).dt.strftime("%Y-%m-%d")
            hist_formatted["Open"] = hist["Open"].map("${:.2f}".format)
            hist_formatted["High"] = hist["High"].map("${:.2f}".format)
            hist_formatted["Low"] = hist["Low"].map("${:.2f}".format)
            hist_formatted["Close"] = hist["Close"].map("${:.2f}".format)
            hist_formatted["Volume"] = hist["Volume"].map("{:,}".format)  # add commas for readability
            stock_data = hist_formatted.to_html(classes="table table-striped")

            # Prepare chart data (dates + closing prices)
            chart_data = {
                "dates": pd.to_datetime(hist["Date"]).dt.strftime("%Y-%m-%d").tolist(),
                "close": hist["Close"].tolist()  # keep raw float for chart
            }

        else:
            stock_data = "<p>No data found for that symbol and period.</p>"
    except Exception as e:
        stock_data = f"<p>Error: {str(e)}</p>"

    return render_template("index.html", stock_data=stock_data,
                           chart_data=chart_data, symbol=symbol,
                           start=start, end=end)

if __name__ == "__main__":
    app.run(debug=True)
