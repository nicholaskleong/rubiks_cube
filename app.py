import os

import dash
import dash_core_components as dcc
import dash_html_components as html

from layout.body import body_layout
from callbacks.callbacks import register_callbacks
app = dash.Dash(__name__)

server = app.server

app.layout = body_layout

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
