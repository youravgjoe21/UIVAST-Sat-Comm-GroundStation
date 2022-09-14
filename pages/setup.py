import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/setup')

NEW_SESSION_LAYOUT = [
                      html.H4("Launch type"),
                      dbc.DropdownMenu(label='Select launch type', children=[dbc.DropdownMenuItem('Full Launch'),dbc.DropdownMenuItem('Tethered Launch'),dbc.DropdownMenuItem('Test')]),
                      html.P("Create a new session for the selected launch"),
                      dbc.Button("New session")
                     ]

OLD_SESSION_LAYOUT = [
                      
                     ]

layout = html.Div([html.H1("Welcome to Ground Station",style={'text-align':'center'}),
                   dbc.Button("Continue last session"),
                   html.Br(),
                   dbc.Row([dbc.Col(NEW_SESSION_LAYOUT,width=6),dbc.Col(OLD_SESSION_LAYOUT,width=6)])
                  ])
