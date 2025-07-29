#helpers#!pip install dash
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

#df7 = pd.read_csv(r'C:\Users\PC\OneDrive\Dashboard Project\Code\cleaned_data.csv')
df7 = pd.read_csv(r'Code\cleaned_data.csv')


def generate_graphs(driver):

    df = df7[df7['fullname'] == driver].copy()
    df['moving_avg'] = df['position'].rolling(window=3, min_periods=1).mean()
    df['cumulative_points'] = df['points'].cumsum()
    x = df['points'].cumsum()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    def ordinal(n):
        if 10 <= n % 100 <= 13:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"


##################### First Row
    fig_position = go.Figure()
    
    fig_position.add_trace(go.Bar(
        x = df['name'],
        y = df['position'],
        name = 'Race Position',
        marker_color = 'blue',
    ))

    fig_position.add_trace(go.Scatter(
        x = df['name'],
        y = df['moving_avg'],
        mode = 'lines+markers',
        name = 'Moving Average',
        line = dict(color='red', width=2),
    ))

    fig_position.update_layout(
        title=f'Position of {driver} in 2024 Season',
        xaxis_title = 'Grand Prix',
        barmode = 'overlay'
    )

#####################

    fig_points = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

    fig_points.add_trace(go.Bar(
        x = df['name'],
        y = df['points'],
        name = 'Points',
        marker_color = 'green',
    ))

    fig_points.add_trace(go.Scatter(
        x = df['name'],
        y = df['cumulative_points'],
        mode = 'lines+markers',
        name = 'Cumulative Points',
        line = dict(color='orange', width=2),
    ), secondary_y=True)

    fig_points.update_layout(
        title=f'Points of {driver} in 2024 Season',
        xaxis_title = 'Grand Prix',
        barmode = 'overlay'
    )

#####################
    df['123'] = df['position'].apply(lambda x: 1 if x in [1,2,3] else 0)
    card = [
    dbc.CardHeader(html.H2(f"{driver} Statistics")),
    dbc.CardBody([
        html.H4(f"Total points scored this season: {x.iloc[-1]} points.", style = {"textTransform": "lowercase"}),
        html.Br(),
        html.H4(f"Average points per race: {df['points'].mean().round(-1)} points.", style = {"textTransform": "lowercase"}),
        html.Br(),
        html.H4(f"Average position per race: {ordinal(df['position'].mean().round())}", style = {"textTransform" : "lowercase"}),
        html.Br(),
        html.H4(f"Number of races won: {(df['position'] == 1).sum()}", style = {"textTransform": "lowercase"}),
        html.Br(),
        html.H4(f"Number of Podiums: {(df['123'] == 1).sum()}", style = {"textTransform": "lowercase"})
        
        ])
    ]

####################
        
    df['123'] = df['position'].apply(lambda x: 1 if x in [1,2,3] else 0)
    number = df['123'].value_counts().sort_index()
    pie_chart_driver = go.Figure(go.Pie(
    labels=['Non-Podium', 'Podium'],
    values=[number.get(0, 0), number.get(1, 0)],
    textinfo='label+percent',
    hole=0.3
    ))


    return fig_position, fig_points, pie_chart_driver, card

###################Constructors Page
def update_constructors(selected_constructor):
    df_constructor = df7[df7['constructorRef'] == selected_constructor].copy()
    df_constructor['date'] = pd.to_datetime(df_constructor['date'])
    df_constructor = df_constructor.sort_values(by='date')
    df_constructor['constructor_points'] = df_constructor['points']
    df_constructor['constructor_points_cumulative'] = df_constructor['constructor_points'].groupby(df_constructor['constructorRef']).cumsum()
    df_constructor['cum_points'] = df_constructor.groupby('raceId')['constructor_points_cumulative'].transform('max')

    fig_constructor_points = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

    fig_constructor_points.add_trace(go.Bar(
        x = df_constructor['name'],
        y = df_constructor['constructor_points'],
        name = 'Points',
        marker_color = 'green',
    ))

    fig_constructor_points.add_trace(go.Scatter(
        x = df_constructor['name'],
        y = df_constructor['cum_points'],
        mode = 'lines+markers',
        name = 'Cumulative Points',
        line = dict(color='orange', width=2),
    ), secondary_y=True)


    return fig_constructor_points


################ Map Page 
def race_map_graph(_):
    df = df7.copy()
    race_map = go.Figure()

    race_map.add_trace(go.Scattergeo(
        lat = df['lat'],
        lon = df['lng'],
        text = df['circuit_name'] + ' Grand Prix',
        mode = 'markers',
        marker = dict(size=8, color='red'),
    ))

    return race_map


############ Map Page

def new_raced_map(_):
    df = df7.copy()
    new_race_graph = go.Figure()

    new_race_graph.add_trace(go.Scattermapbox(
        lat = df['lat'],
        lon = df['lng'],
        text = df['circuit_name'],
        mode = 'markers',
    ))

    new_race_graph.update_layout(
        mapbox_style="open-street-map",  # ✅ required
        mapbox_zoom=1.5,
        mapbox_center={"lat": df['lat'].mean(), "lon": df['lng'].mean()},
        #margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )    
    return new_race_graph

