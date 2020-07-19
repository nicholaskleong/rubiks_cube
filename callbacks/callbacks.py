from dash.dependencies import Input, Output, State
import json
from components.graphs import *

def register_callbacks(app):
    @app.callback(Output('cube', 'figure'),
                  [Input('theta', 'value')])
    def update_cube(theta):
        theta = theta*(math.pi/180)
        return cube_graph(theta)

    @app.callback(
        Output('memory','data'),
        [Input('none','children'),
         Input('L', 'n_clicks')],
        [State('memory','data')]
    )
    def callback_update_rubik_state(_,L,state):
        if not state:
            R = init_rubiks()
        else:
            R = Rubik(None)
            state = json.loads(state)
            R.load_state(state)
            R.rotate_left()
        return json.dumps(R.get_state())

    @app.callback(Output('rubiks', 'figure'),
                [Input('memory','data')])
    def update_rubiks(state):
        if state:
            state = json.loads(state)
            return plot_rubiks(state)
        else:
            return go.Figure()

    # @app.callback(
    #     Output('memory', 'data'),
    #     [Input('L', 'n_clicks')],
    #     [State('memory','data')]
    # )
    # def callback_left(n_clicks,state):
    #     R = Rubik(None)
    #     R.load_state(state)
    #     R.rotate_left()
    #     return json.dumps(R.get_state)
