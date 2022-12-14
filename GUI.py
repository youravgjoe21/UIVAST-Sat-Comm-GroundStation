from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash

### ---------------- *** S T Y L E S *** ---------------- ###

# Defined styles for components. This creates static positions and paddings around them to enforce the desired layout.
# Styles get injected into components

BUTTON_STYLE= {
                'padding':'20px',
                'padding-top':'26px',
                'padding-bottom':'30px',
                'border-radius':'20px',
                'width':'120px',
                'font-size':'48px'
              }

### ---------------- *** L A Y O U T S *** ---------------- ###

# Component layouts which will be injected into the webpage

# Top bar containing logo, name, and a few buttons
titlebar_Layout = dbc.Row([dbc.Col(html.Img(src='assets/VASTSeal.png',style={'width':'60px','margin':'8px'}),width=1),
                           dbc.Col(html.H3("VAST Mobile Ground Station",style={'margin-left':'12px'}),align='center',width=7),
                           # Buttons serving extra functions, such as database setup and exit 
                           dbc.Col(dbc.Row([
                                           dbc.Button(html.I(className='fa-solid fa-gear',style={'font-size':'30px'}),href='/setup',style={'width':'60px','margin':'8px'}),
                                           dbc.Button(html.I(className='fa-solid fa-right-from-bracket',style={'font-size':'30px'}),style={'width':'60px','margin':'8px'})
                                           ],justify='right'),
                                   align='center',width=4)
                          ],
                          style={'background':'#304FFE'})

# Sidebar containing hyperlink buttons to switch between dashboard and map views
sidebar_Layout = dbc.Row(dbc.Col([dbc.Button(html.I(className='fa-solid fa-th-list'),href='/',style=BUTTON_STYLE,className='me-1 mt-1 btn btn-info'), 
                          html.Br(), html.Br(), html.Br(),
                          dbc.Button(html.I(className='fa-solid fa-map-marked'),href='/map',style=BUTTON_STYLE,className='me-1 mt-1 btn btn-info')],
                         width=3,style={'padding':'0px','margin-left':'-60px','margin-top':'30px'}),
                        justify='center')

### ---------------- *** I N I T I A L I Z A T I O N *** ---------------- ###

app = Dash(__name__, 
           use_pages=True, 
           external_stylesheets=['assets/css/darkly-bootstrap.min.css', 'assets/css/all.css'], 
           meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])

app.layout = html.Div([titlebar_Layout,
                       dbc.Row([dbc.Col(sidebar_Layout, width=2, align='center'),dbc.Col(dash.page_container,width=10,align='start')])])


def start():
  app.run(debug=True,host='0.0.0.0')