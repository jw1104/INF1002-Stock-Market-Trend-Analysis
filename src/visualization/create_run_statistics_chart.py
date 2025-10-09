import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_run_statistics_chart(dates, runs, stats):
    """
    Create visualization for run statistics.
    Works directly with tuple format from calculate_runs.
    
    Args:
        runs: List of tuples [('up', 3), ('down', 2), ...]
        stats: Dictionary from analyze_runs()
        
    Returns:
        Plotly figure html string
    """
    if not runs:
        raise ValueError("No run data to visualize")
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Run Lengths Over Time', 'Run Distribution Comparison'),
        column_widths=[0.6, 0.4]
    )
    
    # Extract run values with sign for plotting
    run_values = []
    colors = []
    for direction, streak in runs:
        if direction == 'up':
            run_values.append(streak)
            colors.append('green')
        elif direction == 'down':
            run_values.append(-streak)
            colors.append('red')
        else:  # flat
            run_values.append(0)
            colors.append('gray')
    
    # Left: Run lengths timeline
    fig.add_trace(
        go.Bar(
            x=dates,
            y=run_values,
            marker_color=colors,
            name='Run Length',
            showlegend=False,
            hovertemplate='Run: %{y} days<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add average lines
    fig.add_hline(y=stats['avg_upward_run'], line_dash="dash", 
                  line_color="green", 
                  annotation_text=f"Avg Up: {stats['avg_upward_run']}",
                  row=1, col=1)
    fig.add_hline(y=-stats['avg_downward_run'], line_dash="dash",
                  line_color="red",
                  annotation_text=f"Avg Down: {stats['avg_downward_run']}",
                  row=1, col=1)
    
    # Right: Box plot comparison
    upward_runs = [streak for direction, streak in runs if direction == 'up']
    downward_runs = [streak for direction, streak in runs if direction == 'down']
    
    fig.add_trace(
        go.Box(
            y=upward_runs,
            name='Upward Runs',
            marker_color='green',
            boxmean='sd'
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Box(
            y=downward_runs,
            name='Downward Runs',
            marker_color='red',
            boxmean='sd'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text="Run Statistics",
        height=600,
        template='plotly_white'
    )
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="Run Length (days)", row=1, col=1)
    fig.update_yaxes(title_text="Run Length (days)", row=1, col=2)
    
    return fig.to_html(full_html=False, include_plotlyjs=False)