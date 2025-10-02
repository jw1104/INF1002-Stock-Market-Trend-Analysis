import plotly.graph_objects as go

def create_price_sma_chart(dates, closing_prices, sma_values, symbol):
    """
    Create a Plotly chart showing closing prices and SMA.
    
    Args:
        dates: List of date strings
        closing_prices: List of closing prices
        sma_values: List of SMA values
        symbol: Stock symbol string
        
    Returns:
        HTML string of the Plotly chart
    """
    fig = go.Figure()
    
    # Add closing price trace
    fig.add_trace(go.Scatter(
        x=dates,
        y=closing_prices,
        mode='lines',
        name='Closing Price',
        line=dict(color='blue', width=2)
    ))
    
    # Add SMA trace
    fig.add_trace(go.Scatter(
        x=dates,
        y=sma_values,
        mode='lines',
        name='SMA',
        line=dict(color='red', width=2)
    ))
    
    fig.update_layout(
        title=f'Closing Prices vs SMA for {symbol}',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        hovermode='x unified',
        width=900,
        height=600,
        showlegend=True
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False)