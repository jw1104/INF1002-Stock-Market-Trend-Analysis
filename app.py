from flask import Flask, render_template, request
import pandas as pd
from INF1002_Stock_Market_Trend_Analysis.src.analysis.data_fetcher import data_fetcher
from INF1002_Stock_Market_Trend_Analysis.src.analysis.simple_moving_average import simple_moving_average
from INF1002_Stock_Market_Trend_Analysis.src.analysis.up_down_runs import calculate_directions, calculate_runs
from INF1002_Stock_Market_Trend_Analysis.src.analysis.daily_returns import daily_returns
import plotly.graph_objs as go

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_data = None
    symbol = ""
    period = ""
    sma = None
    sma_window = ""
    chart_html = None

    if request.method == "POST":
        symbol = request.form["symbol"].upper()
        period = request.form["period"].lower()
        sma_window = request.form["sma_window"]

        try:
            data = data_fetcher(symbol, period)
            
            closing_price = data["Close"].tolist()
            dates = data.index.strftime("%Y-%m-%d").tolist()
            sma_window_int = int(sma_window)
            sma = simple_moving_average(data, sma_window_int)
        
            chart_data = {
                "dates": dates,
                "close": closing_price,
                "sma": sma.tolist()
            }

            fig = go.Figure()

            returns = daily_returns(data)
            run_directions = calculate_directions(returns.tolist())
            runs = calculate_runs(run_directions)

            colors = []
            streak_info = []

            for direction, streak in runs:
                color = "green" if direction == "up" else "red" if direction == "down" else "blue"
                
                for i in range(streak):
                    colors.append(color)
                    streak_info.append({
                        'direction': direction,
                        'streak': streak,
                        'position_in_streak': i + 1
                    })

            max_segments = min(len(returns), len(colors), len(dates) - 1, len(closing_price) - 1)

            i = 0
            while i < max_segments:
                current_color = colors[i]
                current_streak_data = streak_info[i]
                
                start_idx = i
                while (i < max_segments and 
                    colors[i] == current_color and 
                    streak_info[i]['direction'] == current_streak_data['direction'] and
                    streak_info[i]['streak'] == current_streak_data['streak']):
                    i += 1
                
                end_idx = i
                
                x_data = dates[start_idx:end_idx + 1]
                y_data = closing_price[start_idx:end_idx + 1]
                
                direction = current_streak_data['direction'].title()
                streak = current_streak_data['streak']
                
                hover_text = []
                for j in range(len(x_data)):
                    if j < len(x_data) - 1:
                        actual_idx = start_idx + j
                        hover_text.append(
                            f"Date: {x_data[j]}<br>" +
                            f"Price: ${y_data[j]:.2f}<br>" +
                            f"Direction: {direction}<br>" +
                            f"Streak Length: {streak} days<br>" +
                            f"Day {actual_idx - start_idx + 1} of {streak}"
                        )
                    else:
                        hover_text.append(
                            f"Date: {x_data[j]}<br>" +
                            f"Price: ${y_data[j]:.2f}"
                        )
                
                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode="lines+markers",
                    line=dict(color=current_color, width=3),
                    marker=dict(size=4, color=current_color),
                    name=f"{direction} Run (Length: {streak})",
                    text=hover_text,
                    hovertemplate="%{text}<extra></extra>",
                    showlegend=False
                ))

            fig.update_layout(
                title=f'Closing Price with Run Directions for {symbol}',
                xaxis_title='Date',
                yaxis_title='Price (USD)',
                hovermode='closest',
                width=1000,
                height=600
            )
            
            chart_html = fig.to_html(full_html=False, include_plotlyjs=False)
            
        
        except Exception as e:
            print(f"Error: {str(e)}")

    return render_template("index.html",
                           chart_data=chart_data,
                           symbol=symbol,
                           period=period,
                           sma=sma,
                           sma_window=sma_window,
                           chart_html=chart_html
                           )


if __name__ == "__main__":
    app.run(debug=True)