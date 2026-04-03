import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


#Calculations
#PI

### Previous version where the error is calculated per iteration

# def calculate_voltage(kp, Tp, Ti, e):
#    voltage_max = 0.95
#    voltage_min = 0.0
#    new_voltage = kp * (e[-1] + (Tp / Ti) * sum(e))
#    new_voltage = max(voltage_min, min(voltage_max, new_voltage))

#    return new_voltage


def calculate_voltage(proportional_gain, sampling_period, integration_constant, current_error, error_sum):
    voltage_max = 0.95
    voltage_min = 0.0
    new_voltage = proportional_gain * (current_error + (sampling_period / integration_constant) * error_sum)
    new_voltage = max(voltage_min, min(voltage_max, new_voltage))

    return new_voltage


### Previous version where the error was calculated per iteration

#sim
    for n in range(int(simulation_time / sampling_period)):
        e.append(requested_water_temp - temperature[-1])
        u = calculate_voltage(kp, sampling_period, integration_constant,e)
        requiredPower = u * heater_power #power required to heat water
        heater_power_list.append(requiredPower)
        heat_capacity = water_heat_const * water_density * volume
        heat_change = (requiredPower * sampling_period) / heat_capacity # heat change over time
        flow_temp = (water_flow * sampling_period / volume) * (temperature[-1] - inflow_temp) # temperature change due mixign
        x = temperature[-1] + heat_change - flow_temp
        x = max(0, x)

        temperature.append(x)
        timestamp.append(timestamp[-1] + sampling_period)
    return temperature, timestamp, heater_power_list


def simulate(requested_water_temp, sampling_period, integration_constant, boiler_volume, heat):
    heater_power = heat
    simulation_time = 3000
    water_heat_const = 4184
    water_density = 997
    water_flow = 0.00005
    inflow_temp = 10
    proportional_gain = 0.075

    temperature = [inflow_temp]
    volume = boiler_volume
    heater_power_list = []
    timestamp = [0]
    error_sum = 0.0

    for n in range(int(simulation_time / sampling_period)):
        current_error = requested_water_temp - temperature[-1]
        error_sum += current_error
        control_signal = calculate_voltage(proportional_gain, sampling_period, integration_constant, current_error, error_sum)

        requiredPower = control_signal * heater_power  # power required to heat water
        heater_power_list.append(requiredPower)

        heat_capacity = water_heat_const * water_density * volume
        heat_change = (requiredPower * sampling_period) / heat_capacity
        flow_temp = (water_flow * sampling_period / volume) * (temperature[-1] - inflow_temp)  #

        x = temperature[-1] + heat_change - flow_temp
        x = max(0, x)

        temperature.append(x)
        timestamp.append(timestamp[-1] + sampling_period)

    return temperature, timestamp, heater_power_list


#App configuration
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Boiler Heating Simulation",
            style={
                'textAlign': 'center',
                'padding': '40px 0',
                'margin': '0',
                'backgroundColor': '#8BAE66',
                'color': 'white',
                'borderBottom': '5px solid #2d3436'
            }),

    html.Div([
        # Boiler and Heater Settings
        html.Div([
            html.Label("Boiler Size (Volume):", style={'fontWeight': 'bold', 'color': '#2d3436'}),
            dcc.Dropdown(
                id='boiler-size',
                options=[
                    {'label': 'Small (5 L)', 'value': 0.005},
                    {'label': 'Medium (10 L)', 'value': 0.01},
                    {'label': 'Big (20 L)', 'value': 0.02}
                ],
                value=0.02,
                clearable=False,
                style={'marginBottom': '20px', 'color': 'black'}
            ),

            html.Label("Heater Power (W):", style={'fontWeight': 'bold', 'color': '#2d3436'}),
            dcc.Dropdown(
                id='heater-power',
                options=[
                    {'label': 'Weak (6 kW)', 'value': 6000},
                    {'label': 'Average (12 kW)', 'value': 12000},
                    {'label': 'Large (20 kW)', 'value': 20000}
                ],
                value=20000,
                clearable=False,
                style={'color': 'black'}
            ),
        ], style={'width': '35%', 'padding': '30px', 'backgroundColor': '#f8f9fa', 'borderRadius': '15px',
                  'margin': '10px'}),

        #Sliders
        html.Div([
            html.Label("Required Water Temperature (°C)", style={'fontWeight': 'bold', 'color': '#2d3436'}),
            dcc.Slider(id='temperature', min=30, max=70, step=1, value=50, marks={i: f'{i}°' for i in range(30, 71, 10)}),

            html.Label("Sampling Time",
                       style={'fontWeight': 'bold', 'color': '#2d3436', 'marginTop': '20px', 'display': 'block'}),
            dcc.Slider(id='sampling', min=0.1, max=1, step=0.1, value=0.1, marks={i / 10: str(i / 10) for i in range(1, 11, 2)}),

            html.Label("Integration Constant",
                       style={'fontWeight': 'bold', 'color': '#2d3436', 'marginTop': '20px', 'display': 'block'}),
            dcc.Slider(id='integration', min=1, max=100, step=5, value=5, marks={i: str(i) for i in range(0, 101, 20)}),

        ], style={'width': '55%', 'padding': '30px', 'backgroundColor': '#f8f9fa', 'borderRadius': '15px',
                  'margin': '10px'})

    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'padding': '20px',
        'backgroundColor': '#dfe6e9'
    }),

    #Run button
    html.Div([
        html.Button(
            "Run Simulation",
            id='run-button',
            n_clicks=0,
            style={
                'backgroundColor': '#8BAE66',
                'color': 'white',
                'fontSize': '18px',
                'fontWeight': 'bold',
                'padding': '15px 50px',
                'border': 'none',
                'borderRadius': '30px',
                'cursor': 'pointer',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.2)',
                'marginTop': '20px',
                'transition': '0.3s'
            }
        )
    ], style={'textAlign': 'center', 'backgroundColor': '#dfe6e9', 'paddingBottom': '20px'}),

    # Graphs
    html.Div([
        html.Div([dcc.Graph(id='temp-graph')], style={'width': '48%', 'minWidth': '400px'}),
        html.Div([dcc.Graph(id='power-graph')], style={'width': '48%', 'minWidth': '400px'})
    ], style={
        'display': 'flex',
        'justifyContent': 'space-evenly',
        'flexWrap': 'wrap',
        'padding': '30px',
        'backgroundColor': '#2d3436'
    })
])

@app.callback(
    [Output('temp-graph', 'figure'),
     Output('power-graph', 'figure')],
    [Input('run-button', 'n_clicks')],
    [State('temperature', 'value'),
     State('sampling', 'value'),
     State('integration', 'value'),
     State('boiler-size', 'value'),
     State('heater-power', 'value')]
)
def update_graph(n_clicks, temperature, sampling_period, integration_constant, boiler_volume, heater_power):
    if n_clicks == 0:
        return go.Figure(), go.Figure()

    y, x, p = simulate(temperature, sampling_period, integration_constant, boiler_volume, heater_power)

    #graph 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y, x=x, mode='lines', name='Temperature',
        line=dict(
            color="lime",
            width=3,
            dash="solid"
        ),
        fill="tozeroy",
        fillcolor="rgba(100, 255, 100, 0.2)"
        ))
    #display style
    fig.update_layout(
        xaxis=dict(
            color="white",
            title="Time [s]",
            title_font=dict(color="white", size=16),
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            color="white",
            title="Temperature [°C]",
            title_font=dict(color="white", size=16),
            tickfont=dict(size=14)
        ),
        legend=dict(
            font=dict(color="white", size=14),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="gray",
            borderwidth=1
        ),
        plot_bgcolor="#1E1E1E",
        paper_bgcolor="#1E1E1E",
        font=dict(color="white")
    )

    #graph 2
    fig_power = go.Figure()
    fig_power.add_trace(
        go.Scatter(y=p, x=x, mode='lines', name='Heater Power',
            line=dict(
                color="red",
                width=3,
                dash="solid"
            ),
            fill="tozeroy",
            fillcolor="rgba(255, 100, 100, 0.2)"))

    #display tyle 2
    fig_power.update_layout(
        xaxis=dict(
            color="white",
            title="Time [s]",
            title_font=dict(color="white", size=16),
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            color="white",
            title="Power [W]",
            title_font=dict(color="white", size=16),
            tickfont=dict(size=14)
        ),
        legend=dict(
            font=dict(color="white", size=14),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="gray",
            borderwidth=1
        ),
        plot_bgcolor="#1E1E1E",
        paper_bgcolor="#1E1E1E",
        font=dict(color="white")
    )

    return fig, fig_power

if __name__ == "__main__":
    app.run(debug=True)
