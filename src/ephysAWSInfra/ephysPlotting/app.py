# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import base64


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
num = 1

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

image_filename = 'b_crop.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


app.layout = html.Div(children=[
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height=40),
    html.H1(children='ePhys Portal'),

    dcc.Input(id='input', value='Enter UUID', type='text'),
    html.Div(id='output'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
            ],
            'layout': {
                'title': 'Channel ' + str(num),
            }
        }
    )
])

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')])

def update_value(input_data):
    return "Input: {}".format(input_data)

if __name__ == '__main__':
    app.run_server(debug=True)
