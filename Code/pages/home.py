#home
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.io as pio 
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers import generate_graphs, update_constructors


pio.templates.default = "ggplot2"

#df7 = pd.read_csv(r'C:\Users\PC\OneDrive\Dashboard Project\Code\cleaned_data.csv')
df7 = pd.read_csv(r'Code\cleaned_data.csv')


dash.register_page(__name__, path='/')

layout = dbc.Container(
    [
##Dropdown Row
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id = "dropdown",
                    options = [{'label': i, 'value': i} for i in df7['fullname'].unique()],
                    value = df7['fullname'].unique()[0],
                    clearable = False,
                    className = "mb-3"
                )
            )
        ], class_name="mb-3"),

#First Graph Row
        dbc.Row([
            dbc.Col(dcc.Graph(id='graph-position'), width=12),

                ], class_name="mb-3"
        ),

        dbc.Row([
            dbc.Col(dcc.Graph(id='graph-points'), width=12), 
        ], class_name = "mb-3"),

        dbc.Row([
            dbc.Col(
                dbc.Card(id='info-card',
                    style = {'height': '100%',
                        'textAlign': 'center'}
                    ), width = 6,
                    style = {'minHeight': '500px'}
                ),
                dbc.Col(
                    dcc.Graph(id='pie_graph'), width = 6
                ) 
        ], class_name = "mb-3"),
    
    ], fluid=True
)

# define callbacks

@callback(
    [
        Output('graph-position', 'figure'),
        Output('graph-points', 'figure'),
        Output('pie_graph', 'figure'),
        Output('info-card', 'children'),
        Input('dropdown', 'value'),
    ]
)

def update_graphs(driver):
    return generate_graphs(driver)

def driver_pie(driver):
    return pie_chart_driver(driver)

