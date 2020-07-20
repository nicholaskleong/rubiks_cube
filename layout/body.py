import dash_core_components as dcc
import dash_html_components as html

body_layout = html.Div([
    html.H2('Rubiks'),
    dcc.Store(id='memory'),
    html.Div(
        className='graph_container twelve columns',
        children=[
            dcc.Graph(id='rubiks'),
        ]),
    html.Div(
        className = 'graph_container twelve columns',
        children=[
            html.Button('L', id='L',className ='button', n_clicks=0),
            html.Button('R', id='R',className ='button', n_clicks=0),
            html.Button('U', id='U',className ='button', n_clicks=0),
            html.Button('D', id='D',className ='button', n_clicks=0),
            html.Button('F', id='F',className ='button', n_clicks=0),
            html.Button('B', id='B',className ='button', n_clicks=0)

    ]),

    html.Div(id='none', children=[], style={'display': 'none'})
])
