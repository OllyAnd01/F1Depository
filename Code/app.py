#application file
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.io as pio
import numpy as np

pio.templates.default = "ggplot2"


app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SOLAR])

#Define the navigation bar 
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Home', href='/')),
        dbc.NavItem(dbc.NavLink('Constructors', href='/constructors')),
        dbc.NavItem(dbc.NavLink('Races', href='/races'))
    ],
    brand="F1 Dashboard",
    brand_href="/",
    color="dark",
    dark=True,

)

#define footer
footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(html.A("Oliver Andrews", href='https://www.linkedin.com/in/oliver-andrews20/'))
        ]
    )
)

app.layout = html.Div([
    navbar,
    dash.page_container,
    footer
])

if __name__ == '__main__':
    app.run(port=8052, debug=True)
