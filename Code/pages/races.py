#home
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.io as pio 
import pandas as pd
import plotly.graph_objects as go
import numpy as np


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers import generate_graphs, update_constructors, new_raced_map 

pio.templates.default = "ggplot2"

#df7 = pd.read_csv(r'C:\Users\PC\OneDrive\Dashboard Project\Code\cleaned_data.csv')
df7 = pd.read_csv(r'Code\cleaned_data.csv')


dash.register_page(__name__, use_pages = True, path='/races')

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H4("Map of the races of 2024", style={'textAlign' : 'center'}),
                width = {'size': True},
            )
        ),
        
        dbc.Row(
            dbc.Col(
                [
                dcc.Store(id='dummy', data='load'),
                dcc.Graph(id='new_racing_graph')
                ], width=12
            )
        ),

        dbc.Row(
            dbc.Col(
                dcc.Graph(id='racer_graph'), width=12
            )
        )
    ]
)


#Define Callbacks 

@callback(
        Output('new_racing_graph', 'figure'),
        Input('dummy', 'data'),

)

def new_races_map(dummy_value):
    return new_raced_map(dummy_value)

@callback(
    Output('racer_graph', 'figure'),
    Input('new_racing_graph', 'clickData')
)

def cool_graph(clickData):
    if clickData is None:
        # Return an empty but valid figure
        return go.Figure()

    # Get clicked point's circuit name from `text`
    point = clickData['points'][0]
    circuit_name = point.get('text', None)

    if circuit_name is None:
        return go.Figure()

    # Filter your dataframe
    df = df7[df7['circuit_name'] == circuit_name].copy()


    # Create the bar chart
    race_position = go.Figure()

    race_position.add_trace(go.Bar(
        x = df['fullname'],
        y = df['points'],
        name = 'Points',
        marker_color = 'green',
    ))

    race_position.update_layout(title=f"Race Points at {circuit_name}")

    return race_position



