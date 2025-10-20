from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import math

app = Dash()

def simulate_water_level():
    surfaceArea = 2.5
    outflowConstant = 0.035
    inflowIntensity = 0.05
    testPeriod = 0.1
    simulationTime = 1800
    level = [0.0]
    timestamp = [0.0]
    minLevel = 0.0
    maxLevel = 5.0

    for i in range(int(simulationTime / testPeriod)):
        timestamp.append(timestamp[-1] + testPeriod)
        x = (inflowIntensity - outflowConstant * math.sqrt(level[-1])) * testPeriod / surfaceArea + level[-1]
        level.append(min(maxLevel, max(minLevel, x)))

    return timestamp, level


app.layout = html.Div([
    html.H4('Water Tank Level Simulation'),
    html.P("Select line color:"),
    dcc.Dropdown(
        id="color-dropdown",
        options=[
            {"label": "Blue", "value": "blue"},
            {"label": "Red", "value": "red"},
            {"label": "Green", "value": "green"},
            {"label": "Orange", "value": "orange"}
        ],
        value="blue",
        clearable=False
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    Input("color-dropdown", "value")
)
def display_graph(color):
    timestamp, level = simulate_water_level()

    fig = go.Figure(
        data=go.Scatter(
            x=timestamp,
            y=level,
            mode='lines',
            line=dict(color=color),
            name='Water Level'
        )
    )
    fig.update_layout(
        xaxis_title="Time (s)",
        yaxis_title="Water Level (m)",
        template="plotly_white"
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
