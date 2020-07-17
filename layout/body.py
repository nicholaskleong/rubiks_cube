import dash_core_components as dcc
import dash_html_components as html

body_layout = html.Div([
    html.H2('Rubiks'),
    html.Div(
        className='graph_container five columns',
        children = [
            dcc.Graph(id='cube'),
    ]),
    html.Div(
        className='graph_container five columns',
        children =[
            dcc.Slider(
            id='theta',
            min=0,
            max=360,
            step=2,
            value=0,
            updatemode='drag'
        )
    ]),
    html.Div(id='none', children=[], style={'display': 'none'})
])
