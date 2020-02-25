import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import base64
import os
from itertools import islice

# Selected Dash style template
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Getting some data for plotting
filename = 'I-2020-02-05-21-20-50-1k'
N = 32 #channels
with open(filename) as fd:
    fd.seek(6) #Sury said first two values in each RasPi recording file are garbage values

    #get array of k samles from recording: rows = sampels, columns = channels
    A = np.asarray([i.strip() for i in islice(fd, N)]).reshape((1, 32))
    for k in range(50):
        data = np.asarray([i.strip() for i in islice(fd, N)]).reshape((1, 32))
        A = np.append(A, data, axis=0)
    #print(A)


# Prepare Brangeneers logo
image_filename = 'b_crop.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Actual webpage components are put together here
app.layout = html.Div(children=[
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height=40),
    html.H1(children='ePhys Portal'),

    dcc.Input(id='input', value='1', type='text'),
    html.Div(id='output-graph'),

])

# Interactivity
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')])

def update_graph(input_data):

    if input_data is '':
        return dcc.Graph(id='example-graph', figure={})

    num = int(input_data)
    if num<0 or num>N:
        return dcc.Graph(id='example-graph', figure={})


    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                #{'x': [1, 2, 3], 'y': [1, 2, 3], 'type': 'line'}
                {'y': A[:,num], 'type': 'line', 'name': num},
            ],
            'layout': {
                'title': 'Channel ' + str(num),
            }
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)
