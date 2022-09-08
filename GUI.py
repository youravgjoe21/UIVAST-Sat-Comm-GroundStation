from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
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

titlebar_Layout = dbc.Row([html.Img(src='assets/VASTSeal.png',style={'width':'80px','margin':'8px'}),
                           html.H3("VAST Mobile Ground Station",style={'width':'50%', 'display':'flex', 'justify-items':'center','align-items':'center','padding-left':'0px'})
                          ],
                           style={'background':'#304FFE'})

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
  app.run(debug=True)