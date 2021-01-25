import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from datetime import date, datetime as dt
import time
import re

from urllib.request import urlopen
import json

import pandas as pd
import numpy as np
import pickle

import plotly.express as px

## dash app + server initialize
app = dash.Dash(__name__,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                    {'name': 'author', 'content':'Anandu R'},
                    {'name': 'description', 'content':'Text autocompletion'},
                ],
) 

server = app.server
app.title = 'House price app'

## Colors
title_main = '#ec4646'
sub_title = '#663f3f'
bg_color = '#bbf1fa'
fg_color = '#51c2d5'

app.layout = html.Div(
    className = 'row',
    #style = {'padding':'1em'},
    children = [
        html.Div(
            className = 'row',
            style = {'margin':'1em'},
            children = [
                html.Div(
                    className='div-user-controls',
                    style = {'padding':'2.4em','borderRadius':'25px'},
                    children = [
                        html.Div(children = [
                            html.H2(
                                children = [
                                    'Text auto-completion app',
                                ],
                                style = {'color':title_main, 'fontWeight': 'bold'},
                            ),
                            html.P('''Predicting the next word in the sentence using NGram models created using R'''),
                        ]),
                    ]
                ),
            ]
        ),
    ],
)








## Main
if __name__ == '__main__':
    app.run_server(debug = True)