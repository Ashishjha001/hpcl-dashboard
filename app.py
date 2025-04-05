import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Simulated fuel station data
stations = pd.DataFrame({
    'Station': ['Mumbai', 'Delhi', 'Kolkata', 'Chennai', 'Ahmedabad'],
    'Latitude': [19.0760, 28.7041, 22.5726, 13.0827, 23.0225],
    'Longitude': [72.8777, 77.1025, 88.3639, 80.2707, 72.5714],
    'Fuel_Demand_Today': [8200, 9500, 6700, 7200, 6100],
})

# Simulated time series for selected station
def get_time_series_data(station):
    dates = pd.date_range(start='2025-04-01', periods=7)
    demand = {
        'Mumbai': [8100, 8150, 8200, 8300, 8400, 8500, 8550],
        'Delhi': [9400, 9450, 9500, 9600, 9650, 9700, 9750],
        'Kolkata': [6600, 6650, 6700, 6750, 6780, 6800, 6820],
        'Chennai': [7100, 7150, 7200, 7250, 7280, 7300, 7320],
        'Ahmedabad': [6000, 6050, 6100, 6150, 6180, 6200, 6220]
    }
    return pd.DataFrame({'Date': dates, 'Predicted Demand': demand[station]})

# Initialize app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("HPCL Fuel Demand Forecast Dashboard", style={'textAlign': 'center'}),
    
    html.Div([
        dcc.Graph(
            id='map',
            figure=px.scatter_mapbox(
                stations,
                lat='Latitude',
                lon='Longitude',
                size='Fuel_Demand_Today',
                hover_name='Station',
                zoom=4,
                mapbox_style='open-street-map',
                color_discrete_sequence=['red']
            )
        )
    ]),
    
    html.Div([
        html.Label("Select a Station to View 7-Day Forecast:"),
        dcc.Dropdown(
            id='station-dropdown',
            options=[{'label': s, 'value': s} for s in stations['Station']],
            value='Mumbai'
        ),
        dcc.Graph(id='line-chart')
    ])
])

@app.callback(
    Output('line-chart', 'figure'),
    Input('station-dropdown', 'value')
)
def update_graph(station_name):
    df = get_time_series_data(station_name)
    fig = px.line(df, x='Date', y='Predicted Demand', markers=True,
                  title=f"7-Day Forecast for {station_name}")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True)
