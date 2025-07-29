import dash 
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.io as pio 
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers import update_constructors
#df7 = pd.read_csv(r'C:\Users\PC\OneDrive\Dashboard Project\Code\cleaned_data.csv')
df7 = pd.read_csv(r'Code\cleaned_data.csv')


dash.register_page(__name__,name="Constructors", path='/constructors')


layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H4("The 2024 Season", style={'textAlign' : 'center'}),
                width = {'size': True},
            )
        ),        
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id = "dropdown_constructors",
                    options = [{'label' : i, 'value' : i} for i in df7['constructorRef'].unique()],
                    value = df7['constructorRef'].unique()[0],
                    style = {'width' : '3'},
                )   
            )        
        ], className = "mb-3"),      
        
        dbc.Row([
            dbc.Col(dcc.Graph(id='constructor_performance'), width=12),
        ], className = "mb-3"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='constructor_pie_chart'), width = 12),
        ], className = "mb-3")
    ], fluid=True
)

@callback(
    Output('constructor_performance', 'figure'),
    Input('dropdown_constructors', 'value'),
)

def constructors_graph(constructors):
    return update_constructors(constructors) 


@callback(
        Output('constructor_pie_chart', 'figure'),
        Input('dropdown_constructors', 'value')
)

def contructor_pie(constructors):

    df = df7.copy()

    df = df7[df7['constructorRef'] == constructors].copy()

    df['123'] = df['position'].apply(lambda x: 1 if x in [1,2,3] else 0)
    number = df['123'].value_counts().sort_index()
    
    pie_chart_constructor = go.Figure(go.Pie(
    labels=['Non-Podium', 'Podium'],
    values=[number.get(0, 0), number.get(1, 0)],
    textinfo='label+percent',
    hole=0.3
    ))

    return pie_chart_constructor


