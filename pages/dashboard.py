import math
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import datetime
import globals
import plotly.graph_objects as go
import numpy as np
from numpy import sin, cos, pi

dash.register_page(__name__, path='/')

# ASCII art made using https://patorjk.com/software/taag/#p=display
# Fonts used are Small and Broadway KB

#  __   __ _    ___  ___    _    ___  _     ___  ___ 
#  \ \ / //_\  | _ \|_ _|  /_\  | _ )| |   | __|/ __|
#   \ V // _ \ |   / | |  / _ \ | _ \| |__ | _| \__ \
#    \_//_/ \_\|_|_\|___|/_/ \_\|___/|____||___||___/

# Our data from decoding will be stored here. We will optimize this later, but for now its easier for testing
dataframe = {'latitude': -117.01648, 
             'longitude': 46.72554, 
             'altitude': 11.92, 
             'temperatureE': 273.0, 
             'temperatureI': 270.0, 
             'signalStrength': 4.0, 
             'maxG': 0, 'PBS': 0, 
             'radio': (0, 0, 0, 0), 
             'GyroscopeFB': (0, 0, 0), 
             'Accelerometer': (0, 0, 0), 
             'Magnotometer': 0, 
             'clock': 0, 
             'cutdown': 26, 
             'Pressure': 0}

# *************************************
#   ___  _____ __   __ _     ___  ___ 
#  / __||_   _|\ \ / /| |   | __|/ __|
#  \__ \  | |   \ V / | |__ | _| \__ \
#  |___/  |_|    |_|  |____||___||___/
# 
# *************************************

# CSS styling applied to components

headercolor = '#2b3034'
HEADER_STYLE = {'background':headercolor, 'padding':'8px'}

blockcolor = '#31363c'
BLOCK_STYLE = {'background':blockcolor, 'min-height':'100%'}

backgroundcolor = '#343b41'

yellow = '#fdc903'

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

LED_DISPLAY_STYLE = {
                        'font-family':'DSEG14',
                        'color':yellow, 
                        'margin-bottom':'0px',
                        'text-align':'center'
                    }

# ****************************************
#   _       _ __   __ ___   _   _  _____ 
#  | |     /_\\ \ / // _ \ | | | ||_   _|
#  | |__  / _ \\ V /| (_) || |_| |  | |  
#  |____|/_/ \_\|_|  \___/  \___/   |_| 
# 
# ****************************************

# Functions here generate parts of the layout, which are passed back to the main layout function

#  ___    __    _     _     ___    __    ___       _     ___   __     __   _____  _   ___   _     
# | |_)  / /\  \ \_/ | |   / / \  / /\  | | \     | |   / / \ / /`   / /\   | |  | | / / \ | |\ | 
# |_|   /_/--\  |_|  |_|__ \_\_/ /_/--\ |_|_/     |_|__ \_\_/ \_\_, /_/--\  |_|  |_| \_\_/ |_| \| 

def serveGPSData():
    lat, long, alt = dataframe['latitude'], dataframe['longitude'], dataframe['altitude']*1000
    return html.Div([
                     dbc.Row([dbc.Col('Lat',style={'color':'#a5aeb5','padding-right':'0px'}),dbc.Col(f':{lat}',style={'padding':'0px','text-align':'left', 'color':yellow})]),
                     dbc.Row([dbc.Col('Long',style={'color':'#a5aeb5'}),dbc.Col(f':{long}',style={'text-align':'left', 'color':yellow})]),
                     dbc.Row([dbc.Col('Alt',style={'color':'#a5aeb5'}),dbc.Col(f':{alt}',style={'text-align':'left', 'color':yellow})]),
                     dbc.Row([dbc.Col('Velocity',style={'color':'#a5aeb5','padding-right':'0px'}),dbc.Col(f':{0}',style={'padding':'0px','text-align':'left', 'color':yellow})])
                    ])

#  _      _   __   __   _   ___   _          __    _     ___   __    _    
# | |\/| | | ( (` ( (` | | / / \ | |\ |     / /`  | |   / / \ / /`  | |_/ 
# |_|  | |_| _)_) _)_) |_| \_\_/ |_| \|     \_\_, |_|__ \_\_/ \_\_, |_| \ 

def serveLEDClock():
    return dbc.Col(html.P(datetime.datetime.now().strftime('%H:%M:%S'),style={'font-family':'DSEG14','font-size':'28px','text-align':'center','margin-bottom':'0px'}))

def serveLocationDetails():
    return dbc.Row([dbc.Col([dbc.Col([html.P('Distance',style={'margin-bottom':'0px','text-align':'center'}),html.P("245 KM",style=LED_DISPLAY_STYLE)]),
                             dbc.Col([html.P("Sunset in",style={'margin-bottom':'0px','text-align':'center'}),html.P('45 MINS',style=LED_DISPLAY_STYLE)])
                            ]), 
                   dbc.Col([dbc.Col([html.P("Current speed",style={'margin-bottom':'0px','text-align':'center'}),html.P("2555 KM/H",style=LED_DISPLAY_STYLE)]),
                            dbc.Col([html.P("Last update",style={'margin-bottom':'0px','text-align':'center'}),html.P(getUpdateDelta(),style=LED_DISPLAY_STYLE)])
                           ])])

#  __   ____  _      __   ___   ___       ___   ____ _____   __    _   _    
# ( (` | |_  | |\ | ( (` / / \ | |_)     | | \ | |_   | |   / /\  | | | |   
# _)_) |_|__ |_| \| _)_) \_\_/ |_| \     |_|_/ |_|__  |_|  /_/--\ |_| |_|__ 

def serveTempGauge():
    gauge = go.Figure()
    gauge.add_trace(go.Indicator(
                                    domain = {'x': [0, 1], 'y': [0, 1]},
                                    value=dataframe['temperatureE'] - 273.15,
                                    mode='gauge+number',
                                    gauge={'shape':'angular',
                                           'axis': {
                                                    'range':[-100, 70],
                                                    'visible':False,
                                                   },
                                            'bordercolor':'#ffffff',
                                          },
                                ))
    gauge.update_layout({'height':80,'width':245,'margin':go.layout.Margin(r=0,l=0,t=0,b=0),'modebar':go.layout.Modebar(remove=['toImage'])},
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font={'color':'#ffffff'})

    return gauge

def serverPowerIndicator():
    indicator = go.Figure()
    indicator.add_trace(go.Indicator(
                                        value = 100,
                                        mode='gauge',
                                        gauge = {
                                                'shape': "bullet",
                                                'axis' : {'range':[0, 100],'visible': False}},
                                    domain = {'x': [0, 1], 'y': [0, 1]}))
    indicator.update_layout({'height':40,'width':80,'margin':go.layout.Margin(r=0,l=0,t=0,b=0),'modebar':go.layout.Modebar(remove=['toImage'])},
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color':'#ffffff'})
    return indicator

def serveInertia():
    return dbc.Row([dbc.Col([html.P('Accel',style={'margin-bottom':'0px'}),html.P('Velocity',style={'margin-bottom':'0px'}),html.P('Heading',style={'margin-bottom':'0px'}),html.P('RSSI',style={'margin-bottom':'0px'})]),
                    dbc.Col([html.P(6,style={'margin-bottom':'0px'}),html.P(5,style={'margin-bottom':'0px'}),html.P(50,style={'margin-bottom':'0px'}),html.P(-140,style={'margin-bottom':'0px'})])],
                    style={'font-size':'12px'})

#  __   ____  _      __   ___   ___       __    ___    __    ___   _     __  
# ( (` | |_  | |\ | ( (` / / \ | |_)     / /`_ | |_)  / /\  | |_) | |_| ( (` 
# _)_) |_|__ |_| \| _)_) \_\_/ |_| \     \_\_/ |_| \ /_/--\ |_|   |_| | _)_) 

# TODO

#  _      ___   ___   _     _     ____      __  _____   __   _____  _     __  
# | |\/| / / \ | | \ | | | | |   | |_      ( (`  | |   / /\   | |  | | | ( (` 
# |_|  | \_\_/ |_|_/ \_\_/ |_|__ |_|__     _)_)  |_|  /_/--\  |_|  \_\_/ _)_) 

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

#  _       __    _   _          _      __    _     ___   _    _____ 
# | |\/|  / /\  | | | |\ |     | |    / /\  \ \_/ / / \ | | |  | |  
# |_|  | /_/--\ |_| |_| \|     |_|__ /_/--\  |_|  \_\_/ \_\_/  |_|  

def serveLayout():
    return html.Div([dbc.Row([dbc.Col(dbc.Row([html.H6('Payload Location',style=HEADER_STYLE),
                                                     dbc.Col(html.Div([
                                                                       html.Img(src='assets/map-ex.png',style={'width':'240px'})
                                                                      ]),width=7),
                                                     dbc.Col(serveGPSData())],style={'background':blockcolor,
                                                                                                                      'margin-left':'0px',
                                                                                                                      'margin-right':'0px'}),width=8),
                                    # ******* MISSION CLOCK *******
                                    dbc.Col(html.Div([
                                      html.H6('Mission Clock',style=HEADER_STYLE),
                                      html.Div([serveLEDClock(),
                                               serveLocationDetails()]
                                              )
                                            ],style=BLOCK_STYLE))
                                   ]),
                           html.Div(style={'margin-top':'8px'}),
                                    # ******* SENSOR DETAIL *******
                           dbc.Row([dbc.Col(html.Div([html.H6('Sensor Detail', style=HEADER_STYLE),
                                                      dbc.Row(dcc.Graph(figure=serveTempGauge(),responsive=False),align='center'),
                                                      dbc.Row('Outside Temperature',justify='center'),
                                                      html.Div(style={'height':'1px','width':'90%','background':'#42474d','margin':'auto','margin-bottom':'2px'}),
                                                      dbc.Row([dbc.Col([html.P("Power",style={'margin':'auto'}),
                                                                        dcc.Graph(figure=serverPowerIndicator(),responsive=False)
                                                                       ]),
                                                                dbc.Col([html.P("Inertia/Magneto",style={'margin':'auto'}),
                                                                         serveInertia()
                                                                        ])
                                                              ],style={'margin':'auto'})
                                                     ],
                                                     style=BLOCK_STYLE)),
                                    # ******* SENSOR GRAPHS *******
                                    dbc.Col(html.Div([html.H6('Sensor Graphs', 
                                                     style=HEADER_STYLE)],style=BLOCK_STYLE)),
                                    # ******* MODULE STATUS *******
                                    dbc.Col(html.Div([html.H6('Module Status',style=HEADER_STYLE),
                                                      serveModuleStatus()
                                                     ],style=BLOCK_STYLE))
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

# Old layout stuff
while False:
    # def serveStatusLayout():
    #     '''Module status layout. Displays a list of modules and whether they're working or not on the left column'''

    #     # Will get replaced by a function to retrieve data from another system
    #     modules = globals.rdInst.getModuleStatus()

    #     moduleStatus = [] # Dash element output list
    #     systemOk = True # Global system status. If one module goes down, this goes to false

    #     # Check status of each module in the dictionary
    #     for module in modules:
    #         # Module is online
    #         if modules[module] == True:
    #             status=html.Span("OK", className='me-1 badge bg-success')
    #         elif modules[module] == 'Waiting on Status':
    #             status=html.Span("Unknown", className='me-1 badge bg-primary')
    #         # Module is offline
    #         else:
    #             status=html.Span("OFFLINE", className='me-1 badge bg-danger')
    #             systemOk = False

    #         # Add module status to list and apply styles
    #         moduleStatus.append(dbc.Row([dbc.Col(module, TEXT_STYLE,width=8),
    #                                      dbc.Col(status,width=4,align='left',style=STATUS_STYLE)
    #                                     ]))

    #     # All modules ok
    #     if systemOk == True:
    #         statusClass = 'me-1 badge bg-success'
    #     # Something isn't ok
    #     else:
    #         statusClass = 'me-1 badge bg-danger'

    #     # Build the final layout before exiting
    #     finalLayout = [dbc.Col("System Status",className=statusClass, width=11, style={'font-size':'24px'})]
    #     finalLayout += moduleStatus

    #     return finalLayout

    # def serveSensorDataLayout():
    #     '''Sensor data layout. Contains a list of sensors and their associated data, displayed on the left column.'''
    #     sensorData = globals.rdInst.getSensorData()

    #     return html.Div([
    #                     html.H3("Sensor Data"),
    #                     dbc.Row([
    #                             dbc.Col("Payload temperature", style=TEXT_STYLE, width=8),
    #                             dbc.Col(f"{sensorData['internal-temp']} C", style=SENSOR_DATA_STYLE, width=2)
    #                             ]),
    #                     dbc.Row([
    #                             dbc.Col("Outside temperature", style=TEXT_STYLE, width=8),
    #                             dbc.Col(f"{sensorData['external-temp']} C", style=SENSOR_DATA_STYLE, width=2)
    #                             ]),
    #                     dbc.Row([
    #                             dbc.Col("Pressure", style=TEXT_STYLE, width=8),
    #                             dbc.Col(f"{sensorData['pressure']} pa", style=SENSOR_DATA_STYLE, width=2)
    #                             ]),
    #                     ])

    # def serveLastUpdateLayout():
    #     '''Calculates time between last packet received and the current time to display the time delta between them'''
    #     lastUpdateTime = globals.rdInst.getUpdateTime()
    #     lastUpdateDelta = datetime.datetime.now()-lastUpdateTime
    #     lastUpdateDSec = lastUpdateDelta.total_seconds()
    #     lastUpdateStr = ""

    #     # Build output string
    #     # day
    #     if lastUpdateDSec > 86400:
    #         lastUpdateStr += f"{math.floor(lastUpdateDSec/86400)}d "
    #         # If the seconds aren't removed as you go, you end up with an absurd number of seconds at the end
    #         lastUpdateDSec -= 86400 * math.floor(lastUpdateDSec/86400)
    #     # hour
    #     if lastUpdateDSec > 3600:
    #         lastUpdateStr += f"{math.floor(lastUpdateDSec/3600)}h "
    #         lastUpdateDSec -= 3600 * math.floor(lastUpdateDSec/3600)
    #     # minute
    #     if lastUpdateDSec > 60:
    #         lastUpdateStr += f"{math.floor(lastUpdateDSec/60)}m "
    #         lastUpdateDSec -= 60 * math.floor(lastUpdateDSec/60)
    #     # second
    #     lastUpdateStr += f"{int(lastUpdateDSec)}s"

    #     return html.H6(f"{globals.db.activeTable}\tLast update: {lastUpdateStr} ago")

    # def serveMapLayout():
    #     lat,long,alt = globals.rdInst.getGPSData()
        
    #     return html.Div([
    #                     html.Br(),
    #                     dbc.Row([
    #                             dbc.Col("Latitude", style=TEXT_STYLE, width=8),
    #                             dbc.Col(lat, style=SENSOR_DATA_STYLE, width=3)
    #                             ]),
    #                     dbc.Row([
    #                             dbc.Col("Longitude", style=TEXT_STYLE, width=8),
    #                             dbc.Col(long, style=SENSOR_DATA_STYLE, width=3)
    #                             ]),
    #                     dbc.Row([
    #                             dbc.Col("Altitude", style=TEXT_STYLE, width=8),
    #                             dbc.Col(alt, style=SENSOR_DATA_STYLE, width=3)
    #                             ]),
    #                             html.Br(),
    #                     # dbc.Row([html.Img(src='assets/map-ex.png',style={'width':'380px'})])
    #                     ])
    pass

# *******************************************************
#    ___    _    _     _     ___    _    ___  _  __ ___ 
#   / __|  /_\  | |   | |   | _ )  /_\  / __|| |/ // __|
#  | (__  / _ \ | |__ | |__ | _ \ / _ \| (__ | ' < \__ \
#   \___|/_/ \_\|____||____||___//_/ \_\\___||_|\_\|___/
# 
# *******************************************************
                                                      
# Dash utilizes callbacks to handle user interactions. Functions have an input from a component and output to a component

@callback(Output('dashboard','children'),
          Input('update-interval','n_intervals'),prevent_initial_call=True)
def updatePage(_):
    return serveLayout()

# ************************************************************************************************
#    ___  ___  _  _  ___  ___    _    _      ___  _   _  _  _   ___  _____  ___  ___   _  _  ___ 
#   / __|| __|| \| || __|| _ \  /_\  | |    | __|| | | || \| | / __||_   _||_ _|/ _ \ | \| |/ __|
#  | (_ || _| | .` || _| |   / / _ \ | |__  | _| | |_| || .` || (__   | |   | || (_) || .` |\__ \
#   \___||___||_|\_||___||_|_\/_/ \_\|____| |_|   \___/ |_|\_| \___|  |_|  |___|\___/ |_|\_||___/
# 
# ************************************************************************************************

def getUpdateDelta():
    lastUpdateTime = globals.rdInst.getUpdateTime()
    lastUpdateDelta = datetime.datetime.now()-lastUpdateTime
    lastUpdateDSec = lastUpdateDelta.total_seconds()
    lastUpdateStr = ""

    # Build output string
    # day
    if lastUpdateDSec > 86400:
        lastUpdateStr += f"{math.floor(lastUpdateDSec/86400)} d "
        # If the seconds aren't removed as you go, you end up with an absurd number of seconds at the end
        lastUpdateDSec -= 86400 * math.floor(lastUpdateDSec/86400)
    # hour
    if lastUpdateDSec > 3600:
        lastUpdateStr += f"{math.floor(lastUpdateDSec/3600)} h "
        lastUpdateDSec -= 3600 * math.floor(lastUpdateDSec/3600)
    # minute
    if lastUpdateDSec > 60:
        lastUpdateStr += f"{math.floor(lastUpdateDSec/60)} m "
        lastUpdateDSec -= 60 * math.floor(lastUpdateDSec/60)
    # second
    lastUpdateStr += f"{int(lastUpdateDSec)} s"

    return lastUpdateStr

def degree_to_radian(degrees):
    return degrees*pi/180

def drawCircularGauge(degree_start, degree_end, annotation_text, r=1.0, padding=0.2, tick_length=0.02, useBorder=False):
    radian_start, radian_end =  degree_to_radian(degree_start), degree_to_radian(degree_end)
    theta = np.linspace(radian_start,radian_end,5000)
    x = r * cos(theta)
    y = r * sin(theta)
    fig = go.Figure()

    # draw the bar
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='markers', marker_symbol='circle', marker_size=15, hoverinfo='skip'
    ))

    ## add text in the center of the plot
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode="text",
        text=[annotation_text],
        textfont=dict(size=30),
        textposition="middle center",
        hoverinfo='skip'
    ))

    if useBorder:
        # draw the outer border
        for r_outer in [r-padding,r+padding]:
            fig.add_shape(type="circle",
                xref="x", yref="y",
                x0=-r_outer, y0=-r_outer, x1=r_outer, y1=r_outer,
                line_color="black",
            )

        tick_theta = np.linspace(pi,-pi,13)
        tick_labels = np.linspace(0,330,12)
        tick_start_x, tick_end_x = (r+padding)*cos(tick_theta), (r+padding+tick_length)*cos(tick_theta)
        tick_start_y, tick_end_y = (r+padding)*sin(tick_theta), (r+padding+tick_length)*sin(tick_theta)
        tick_label_x, tick_label_y = (r+padding+0.04+tick_length)*cos(tick_theta), (r+padding+0.04+tick_length)*sin(tick_theta)

        # add ticks
        for i in range(len(tick_theta)):
            fig.add_trace(go.Scatter(
                x=[tick_start_x[i], tick_end_x[i]],
                y=[tick_start_y[i], tick_end_y[i]],
                mode='text+lines',
                marker=dict(color="black"),
                hoverinfo='skip'
            ))
        
        # add ticklabels
        fig.add_trace(go.Scatter(
            x=tick_label_x,
            y=tick_label_y,
            text=tick_labels,
            mode='text',
            hoverinfo='skip'
        ))

    ## get rid of axes, ticks, background
    fig.update_layout(
        showlegend=False,
        xaxis_range=[-1.5,1.5], yaxis_range=[-1.5,1.5], 
        xaxis_visible=False, xaxis_showticklabels=False, 
        yaxis_visible=False, yaxis_showticklabels=False, 
        template="plotly_white",
        width=800, height=800
    )
    return fig