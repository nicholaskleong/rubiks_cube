import dash_core_components as dcc
import dash_html_components as html

body_layout = html.Div([
    html.H2('Rubiks'),
    dcc.Store(id='memory'),

    html.Div(
        className = 'graph_container seven columns',
        children=[
            html.Button('L', id='L', n_clicks=0),
            html.Button('R', id='R', n_clicks=0),
            html.Button('U', id='U', n_clicks=0),
            html.Button('D', id='D', n_clicks=0),
            html.Button('F', id='F', n_clicks=0),
            html.Button('B', id='B', n_clicks=0)

    ]),
    html.Div(
        className='graph_container five columns',
        children=[
            dcc.Graph(id='rubiks'),
        ]),
    html.Div(id='none', children=[], style={'display': 'none'})
])
