import math
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import datetime
import globals

dash.register_page(__name__, path='/')

### ---------------- *** S T Y L E S *** ---------------- ###

# Defined styles for components. This creates static positions and paddings around them to enforce the desired layout.
# Styles get injected into components

STATUS_STYLE = {
                'text-align':'right',
                'padding':'0px'
               }

TEXT_STYLE = {
                'margin-bottom':'2px',
                'margin-left':'8px'
             }

SENSOR_DATA_STYLE = {
                        # 'margin-left':'-20px',
                        'text-align':'right',
                        'padding':'0px'   
                    }

def serveLayout():
    if not globals.isSetup:
        return dcc.Location('location',pathname='/setup')
    return dbc.Row([
                    dbc.Col([dbc.Row(serveStatusLayout(),style={'padding-top':'12px','margin-left':'16px'}),
                             html.Br(),
                             dbc.Row(serveSensorDataLayout(),style={'padding-left':'0px','margin-left':'8px'})
                            ]),
                    dbc.Col([dbc.Row(serveLastUpdateLayout(),style={'text-align':'right', 'padding-right':'4px'}),
                             dbc.Row(serveMapLayout())],width=7,align='right',style={'margin-right':'0px'})
                   ])

# Page layout. Contains a Div which will host the dashboard, and an Interval to refresh the page contents every 1 second
layout = html.Div([html.Div([],id='dashboard'),dcc.Interval('update-interval', interval=1*1000, n_intervals=0)])

def serveStatusLayout():
    '''Module status layout. Displays a list of modules and whether they're working or not on the left column'''

    # Will get replaced by a function to retrieve data from another system
    # modules = globals.rdInst.getModuleStatus()
    modules = {'No modules :(':'Waiting on Status'}
    moduleStatus = [] # Dash element output list
    systemOk = True # Global system status. If one module goes down, this goes to false

    # Check status of each module in the dictionary
    for module in modules:
        # Module is online
        if modules[module] == True:
            status=html.Span("OK", className='me-1 badge bg-success')
        elif modules[module] == 'Waiting on Status':
            status=html.Span("Unknown", className='me-1 badge bg-primary')
        # Module is offline
        else:
            status=html.Span("OFFLINE", className='me-1 badge bg-danger')
            systemOk = False

        # Add module status to list and apply styles
        moduleStatus.append(dbc.Row([dbc.Col(module, TEXT_STYLE,width=8),
                                     dbc.Col(status,width=4,align='left',style=STATUS_STYLE)
                                    ]))

    # All modules ok
    if systemOk == True:
        statusClass = 'me-1 badge bg-success'
    # Something isn't ok
    else:
        statusClass = 'me-1 badge bg-danger'

    # Build the final layout before exiting
    finalLayout = [dbc.Col("System Status",className=statusClass, width=11, style={'font-size':'24px'})]
    finalLayout += moduleStatus

    return finalLayout

def serveSensorDataLayout():
    '''Sensor data layout. Contains a list of sensors and their associated data, displayed on the left column.'''
    return html.Div([
                    html.H3("Sensor Data"),
                    dbc.Row([
                            dbc.Col("Payload temperature", style=TEXT_STYLE, width=8),
                            dbc.Col(f"{globals.rdInst.msg['temperatureI']} K", style=SENSOR_DATA_STYLE, width=2)
                            ]),
                    dbc.Row([
                            dbc.Col("Outside temperature", style=TEXT_STYLE, width=8),
                            dbc.Col(f"{globals.rdInst.msg['temperatureE']} K", style=SENSOR_DATA_STYLE, width=2)
                            ]),
                    dbc.Row([
                            dbc.Col("Pressure", style=TEXT_STYLE, width=8),
                            dbc.Col(f"NUL pa", style=SENSOR_DATA_STYLE, width=2)
                            ]),
                    ])

def serveLastUpdateLayout():
    '''Calculates time between last packet received and the current time to display the time delta between them'''
    lastUpdateTime = globals.rdInst.msg['clock']
    # lastUpdateDelta = datetime.datetime.now()-lastUpdateTime
    # lastUpdateDSec = lastUpdateDelta.total_seconds()
    # lastUpdateStr = ""

    # # Build output string
    # # day
    # if lastUpdateDSec > 86400:
    #     lastUpdateStr += f"{math.floor(lastUpdateDSec/86400)}d "
    #     # If the seconds aren't removed as you go, you end up with an absurd number of seconds at the end
    #     lastUpdateDSec -= 86400 * math.floor(lastUpdateDSec/86400)
    # # hour
    # if lastUpdateDSec > 3600:
    #     lastUpdateStr += f"{math.floor(lastUpdateDSec/3600)}h "
    #     lastUpdateDSec -= 3600 * math.floor(lastUpdateDSec/3600)
    # # minute
    # if lastUpdateDSec > 60:
    #     lastUpdateStr += f"{math.floor(lastUpdateDSec/60)}m "
    #     lastUpdateDSec -= 60 * math.floor(lastUpdateDSec/60)
    # # second
    # lastUpdateStr += f"{int(lastUpdateDSec)}s"

    return html.H6(f"{globals.db.activeTable}\tLast update: {lastUpdateTime}, RSSI {globals.rbInst.msg['signalStrength']}")

def serveMapLayout():
    lat,long,alt = globals.rdInst.msg['latitude'],globals.rdInst.msg['longitude'],globals.rdInst.msg['altitude']
    
    return html.Div([
                    html.Br(),
                    dbc.Row([
                            dbc.Col("Latitude", style=TEXT_STYLE, width=8),
                            dbc.Col(lat, style=SENSOR_DATA_STYLE, width=3)
                            ]),
                    dbc.Row([
                            dbc.Col("Longitude", style=TEXT_STYLE, width=8),
                            dbc.Col(long, style=SENSOR_DATA_STYLE, width=3)
                            ]),
                    dbc.Row([
                            dbc.Col("Altitude", style=TEXT_STYLE, width=8),
                            dbc.Col(alt, style=SENSOR_DATA_STYLE, width=3)
                            ]),
                            html.Br(),
                    # dbc.Row([html.Img(src='assets/map-ex.png',style={'width':'380px'})])
                    ])

@callback(Output('dashboard','children'),
          Input('update-interval','n_intervals'),prevent_initial_call=True)
def updatePage(_):
    return serveLayout()