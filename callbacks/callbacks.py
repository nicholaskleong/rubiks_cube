import dash
from dash.dependencies import Input, Output, State
import json
from components.graphs import *

def register_callbacks(app):
    @app.callback(
        Output('memory','data'),
        [Input('none','children'),
         Input('L', 'n_clicks'),
         Input('R', 'n_clicks'),
         Input('F', 'n_clicks'),
         Input('B', 'n_clicks'),
         Input('U', 'n_clicks'),
         Input('D', 'n_clicks')],
        [State('memory','data')]
    )
    def callback_update_rubik_state(_,L,R,F,B,T,D,state):
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = 'No clicks yet'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        button_id_method = {'L':'rotate_left',
                            'R': 'rotate_right',
                            'F':'rotate_front',
                            'B':'rotate_back',
                            'U': 'rotate_up',
                            'D': 'rotate_down',
        }
        if not state:
            R = init_rubiks()
        else:
            R = Rubik(None)
            state = json.loads(state)
            R.load_state(state)
            rotation_to_call = getattr(R, button_id_method[button_id])
            rotation_to_call()
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
