import math
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import datetime
import globals
import plotly.graph_objects as go

dash.register_page(__name__, path='/')

### ---------------- *** S T Y L E S *** ---------------- ###

# Defined styles for components. This creates static positions and paddings around them to enforce the desired layout.
# Styles get injected into components

STATUS_STYLE = {
                'text-align':'right',
                # 'padding':'0px'
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

# ******************************************************************************************************
# NEW LAYOUT

backgroundcolor = '#343b41'
blockcolor = '#31363c'
headercolor = '#2b3034'
blockStyle = {'background':blockcolor}
headerStyle = {'background':headercolor, 'padding':'8px'}

def serveTempGauge():
    print(globals.rdInst.getSensorData()['external-temp'])
    gauge = go.Figure()
    gauge.add_trace(go.Indicator(
                                    domain = {'x': [0, 1], 'y': [0, 1]},
                                    title={'text':'Temperature','font_size':24},
                                    value=globals.rdInst.getSensorData()['external-temp'],
                                    mode='gauge',
                                    gauge={'shape':'angular',
                                           'axis': {
                                                    'range':[-100, 70]
                                                   },
                                            'bordercolor':'#ffffff'
                                          },
                                ))
    gauge.update_layout({'height':120,'width':200,'margin':go.layout.Margin(r=0,l=0,t=0,b=0),'modebar':go.layout.Modebar(remove=['toImage'])},
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',)

    return gauge

def serveModuleStatus():
    modules = globals.rdInst.getModuleStatus()

    statusOutput = []

    # Check status of each module in the dictionary
    for module in modules:
        # Module is online
        if modules[module] == 'online':
            status=html.Span("ONLINE", className='me-1 badge bg-success')
        # Module is idle
        elif modules[module] == 'idle':
            status=html.Span("IDLE", className='me-1 badge bg-warning')
        # Module status has not been returned
        elif modules[module] == 'Waiting on Status':
            status=html.Span("Unknown", className='me-1 badge bg-primary')
        # Module is offline
        else:
            status=html.Span("OFFLINE", className='me-1 badge bg-danger')

        statusOutput.append(dbc.Row([dbc.Col(module, TEXT_STYLE,width=8),
                                     dbc.Col(status,width=4,align='left',style=STATUS_STYLE)
                                    ]))

    return html.Div(statusOutput)

#                                     # ******* PAYLOAD LOCATION *******
# sixBlockLayout = html.Div([dbc.Row([dbc.Col(dbc.Row([html.H5('Payload Location',style=headerStyle),
#                                                      dbc.Col(html.Div([
#                                                                        html.Img(src='assets/map-ex.png',style={'width':'240px'})
#                                                                       ]),width=8),
#                                                      dbc.Col(html.Div('Col2',style={'background':'#ff0000'}))],style={'background':blockcolor,'margin-right':'0px'}),width=8),
#                                     # ******* MISSION CLOCK *******
#                                     dbc.Col(html.Div([
#                                       html.H5('Mission Clock',style=headerStyle),
#                                       html.Div('Col3')
#                                             ],style=blockStyle))
#                                    ]),
#                            html.Br(),
#                                     # ******* SENSOR DETAIL *******
#                            dbc.Row([dbc.Col(html.Div([html.H5('Sensor Detail', style=headerStyle),
#                                                       dcc.Graph(figure=serveTempGauge(),responsive=False)
#                                                      ],
#                                                      style=blockStyle)),
#                                     # ******* SENSOR GRAPHS *******
#                                     dbc.Col(html.Div([html.H5('Sensor Graphs', 
#                                                      style=headerStyle)],style=blockStyle)),
#                                     # ******* MODULE STATUS *******
#                                     dbc.Col(html.Div([html.H5('Module Status',style=headerStyle),
#                                                       serveModuleStatus()
#                                                      ],style=blockStyle))
#                                                      ])],
#                           style={'padding':'8px','background-color':backgroundcolor,'height':'100vh'})


# ****************************************************************************************************

def serveLayout():
    return html.Div([dbc.Row([dbc.Col(dbc.Row([html.H5('Payload Location',style=headerStyle),
                                                     dbc.Col(html.Div([
                                                                       html.Img(src='assets/map-ex.png',style={'width':'240px'})
                                                                      ]),width=8),
                                                     dbc.Col(html.Div('Col2',style={'background':'#ff0000'}))],style={'background':blockcolor,'margin-right':'0px'}),width=8),
                                    # ******* MISSION CLOCK *******
                                    dbc.Col(html.Div([
                                      html.H5('Mission Clock',style=headerStyle),
                                      html.Div('Col3')
                                            ],style=blockStyle))
                                   ]),
                           html.Br(),
                                    # ******* SENSOR DETAIL *******
                           dbc.Row([dbc.Col(html.Div([html.H5('Sensor Detail', style=headerStyle),
                                                      dcc.Graph(figure=serveTempGauge(),responsive=False,style={'border-radius':'50px'})
                                                     ],
                                                     style=blockStyle)),
                                    # ******* SENSOR GRAPHS *******
                                    dbc.Col(html.Div([html.H5('Sensor Graphs', 
                                                     style=headerStyle)],style=blockStyle)),
                                    # ******* MODULE STATUS *******
                                    dbc.Col(html.Div([html.H5('Module Status',style=headerStyle),
                                                      serveModuleStatus()
                                                     ],style=blockStyle))
                                                     ])],
                          style={'padding':'8px','background-color':backgroundcolor,'height':'100vh'})
    # if not globals.isSetup:
    #     return dcc.Location('location',pathname='/setup')
    # return dbc.Row([
    #                 dbc.Col([dbc.Row(serveStatusLayout(),style={'padding-top':'12px','margin-left':'16px'}),
    #                          html.Br(),
    #                          dbc.Row(serveSensorDataLayout(),style={'padding-left':'0px','margin-left':'8px'})
    #                         ]),
    #                 dbc.Col([dbc.Row(serveLastUpdateLayout(),style={'text-align':'right', 'padding-right':'4px'}),
    #                          dbc.Row(serveMapLayout())],width=7,align='right',style={'margin-right':'0px'})
    #                ])

# Page layout. Contains a Div which will host the dashboard, and an Interval to refresh the page contents every 1 second
layout = html.Div([html.Div([],id='dashboard'),dcc.Interval('update-interval', interval=1*1000, n_intervals=0)])

def serveStatusLayout():
    '''Module status layout. Displays a list of modules and whether they're working or not on the left column'''

    # Will get replaced by a function to retrieve data from another system
    modules = globals.rdInst.getModuleStatus()

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
    sensorData = globals.rdInst.getSensorData()

    return html.Div([
                    html.H3("Sensor Data"),
                    dbc.Row([
                            dbc.Col("Payload temperature", style=TEXT_STYLE, width=8),
                            dbc.Col(f"{sensorData['internal-temp']} C", style=SENSOR_DATA_STYLE, width=2)
                            ]),
                    dbc.Row([
                            dbc.Col("Outside temperature", style=TEXT_STYLE, width=8),
                            dbc.Col(f"{sensorData['external-temp']} C", style=SENSOR_DATA_STYLE, width=2)
                            ]),
                    dbc.Row([
                            dbc.Col("Pressure", style=TEXT_STYLE, width=8),
                            dbc.Col(f"{sensorData['pressure']} pa", style=SENSOR_DATA_STYLE, width=2)
                            ]),
                    ])

def serveLastUpdateLayout():
    '''Calculates time between last packet received and the current time to display the time delta between them'''
    lastUpdateTime = globals.rdInst.getUpdateTime()
    lastUpdateDelta = datetime.datetime.now()-lastUpdateTime
    lastUpdateDSec = lastUpdateDelta.total_seconds()
    lastUpdateStr = ""

    # Build output string
    # day
    if lastUpdateDSec > 86400:
        lastUpdateStr += f"{math.floor(lastUpdateDSec/86400)}d "
        # If the seconds aren't removed as you go, you end up with an absurd number of seconds at the end
        lastUpdateDSec -= 86400 * math.floor(lastUpdateDSec/86400)
    # hour
    if lastUpdateDSec > 3600:
        lastUpdateStr += f"{math.floor(lastUpdateDSec/3600)}h "
        lastUpdateDSec -= 3600 * math.floor(lastUpdateDSec/3600)
    # minute
    if lastUpdateDSec > 60:
        lastUpdateStr += f"{math.floor(lastUpdateDSec/60)}m "
        lastUpdateDSec -= 60 * math.floor(lastUpdateDSec/60)
    # second
    lastUpdateStr += f"{int(lastUpdateDSec)}s"

    return html.H6(f"{globals.db.activeTable}\tLast update: {lastUpdateStr} ago")

def serveMapLayout():
    lat,long,alt = globals.rdInst.getGPSData()
    
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