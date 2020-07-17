from dash.dependencies import Input, Output

from components.graphs import *

def register_callbacks(app):
    @app.callback(Output('cube', 'figure'),
                  [Input('theta', 'value')])
    def update_cube(theta):
        theta = theta*(math.pi/180)
        return cube_graph(theta)
