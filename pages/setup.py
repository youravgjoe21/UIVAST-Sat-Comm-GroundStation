from re import L
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import globals
from datetime import datetime

dash.register_page(__name__, path='/setup')

NEW_SESSION_LAYOUT = [
                      html.H4("Launch type"),
                      dbc.DropdownMenu(label='Select launch type', children=[dbc.DropdownMenuItem('Full Launch',id='full-launch',n_clicks=0),
                                                                             dbc.DropdownMenuItem('Tethered Launch',id='tethered-launch',n_clicks=0),
                                                                             dbc.DropdownMenuItem('Test',id='test-launch',n_clicks=0)],
                                                                             id='launch-dropdown'),
                      html.P("Create a new session for the selected launch"),
                      dbc.Button("New session", id='new-session',href='/')
                     ]

OLD_SESSION_LAYOUT = [
                      
                     ]

selectedLaunch = 'Select Launch Type'

layout = html.Div([html.H1("Welcome to Ground Station",style={'text-align':'center'}),
                   dbc.Button("Continue last session",id='continue-session',href='/'),
                   html.Br(),
                   dbc.Row([dbc.Col(NEW_SESSION_LAYOUT,width=6),dbc.Col(OLD_SESSION_LAYOUT,width=6)])
                  ],style={'padding':'4px'})

@callback(Output('launch-dropdown','label'),
          [Input('full-launch', 'n_clicks'),
           Input('tethered-launch', 'n_clicks'),
           Input('test-launch', 'n_clicks')
          ],prevent_initial_call=True)
def selectLaunchType(_,__,___):
    '''Updates selected launch based on the button pressed'''
    global selectedLaunch

    # Use dash's built in callback context attribute to get the ID of the button that triggered the callback,
    # then update selectedLaunch accordingly
    if dash.callback_context.triggered_id == 'full-launch':
        selectedLaunch = 'Full Launch'
    elif dash.callback_context.triggered_id == 'tethered-launch':
        selectedLaunch = 'Tethered Launch'
    elif dash.callback_context.triggered_id == 'test-launch':
        selectedLaunch = 'Test Launch'

    return selectedLaunch

@callback(Output('new-session','children'), Input('new-session','n_clicks'), prevent_initial_call=True)
def createNewLaunch(_):
    datetimeStr = datetime.now().strftime("%Y-%m-%d")
    globals.db.createLaunchTable(f"{selectedLaunch}-{datetimeStr}")
    globals.isSetup = True

@callback(Output('continue-session','children'), Input('continue-session', 'n_clicks'), prevent_initial_call=True)
def continueLastSession(_):
    tables = globals.db.getTableNames()

    newestTable = datetime(1999,1,1) # We won't have a table from 1999 or older, since table dates are set based on the current date.
    newestTableIdx = 0

    # Strip dates from tables and change values.
    # Then, check the date on each table to see if its newer than the newest seen table.
    # If it is, set it as such
    for table in range(len(tables)):
        tableDate = datetime.strptime(tables[table][-10:],"%Y-%m-%d")
        if tableDate.date() > newestTable.date():
            newestTable = tableDate
            newestTableIdx = table

    globals.db.activeTable = tables[newestTableIdx]
    globals.isSetup = True