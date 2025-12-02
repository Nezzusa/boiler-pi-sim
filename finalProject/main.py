import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


def errorCalc(Tw, current_temp, Tp, Ti, I_prev, kp):
    e = Tw - current_temp
    I = I_prev + (Tp / Ti) * e
    u = kp * (e + I)
    u = max(0, min(1, u))

    return e, I, u


def calculateTankArea(tank_height, tank_bottom_area):
    return tank_height * tank_bottom_area


def simulate(requested_water_temp, sampling_period, integration_constant):
    # constants (put your real values here!)
    heater_power = 3000
    water_heat_const = 4184 #J/Kg
    water_density = 997 # hg/m^3
    tank_bottom_area = 0.2 # meter
    tank_height = 1 # meter
    water_flow = 0.035 # constant for input / output

    start_temp = 20

    temperature = [start_temp]       # initial temperature
    e = []

    volume = calculateTankArea(tank_height, tank_bottom_area) #get tank volume
    for n in range(1000):

        new_error, I_term, u = errorCalc(requested_water_temp, temperature[-1], sampling_period, integration_constant)
        e.append(new_error)
        requiredPower = u * heater_power
        heat_capacity = water_heat_const * water_density * volume
        temperature_ratio = 1 - (water_flow/volume)
        x = ((requiredPower * sampling_period) / heat_capacity)  + temperature_ratio * temperature[-1]
        temperature.append(x)

    return temperature


# -------------------- Dash App --------------------

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Temperature Simulation (Tw, tp, ti)"),

    html.Label("Tw (setpoint)"),
    dcc.Slider(id='Tw', min=0, max=5, step=0.1, value=1),

    html.Label("tp (sampling time)"),
    dcc.Slider(id='tp', min=0.01, max=1, step=0.01, value=0.1),

    html.Label("ti (integral time)"),
    dcc.Slider(id='ti', min=0.1, max=10, step=0.1, value=1),

    dcc.Graph(id='temp-graph')
])


@app.callback(
    Output('temp-graph', 'figure'),
    [Input('Tw', 'value'),
     Input('tp', 'value'),
     Input('ti', 'value')]
)
def update_graph(Tw, tp, ti):
    t = simulate(Tw, tp, ti)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=t,
        mode='lines',
        name='Temperature'
    ))
    fig.update_layout(
        title="Temperature Evolution",
        xaxis_title="Iteration",
        yaxis_title="Temperature"
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
