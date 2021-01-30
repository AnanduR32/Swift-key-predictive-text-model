import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from datetime import date, datetime as dt
import time
import re

import nltk 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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
title_main = '#DA4167'
sub_title = '#253D5B'
bg_color = '#bbf1fa'
fg_color = '#51c2d5'

## NLTK 
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))  

## Autocompletion function
def predictWord(input):
    return(input)

app.layout = html.Div(
    className = 'columns',
    #style = {'padding':'1em'},
    children = [
        html.Div(
            className = 'row',
            style = {'margin':'1em'},
            children = [
                html.Div(
                    className='div-user-controls',
                    style = {'padding':'2.4em','borderRadius':'25px'},
                    
                ),
            ]
        ),
        html.Div(
            className = 'row',
            style = {'margin':'1em'},
            children = [
                html.Div(
                    className = 'three columns',
                    style = {'padding':'2.4em'},
                ),
                html.Div(
                    className='div-user-controls six columns',
                    style = {
                        'padding':'2.4em',
                        'borderRadius':'25px', 
                        'background-image': 'linear-gradient(to right top, #b0abc4, #a8aec8, #a0b2c9, #9ab5c9, #95b8c6)'},
                    children = [
                        html.Div(children = [
                            html.Div(children = [
                                html.H2(
                                    children = [
                                        'Text auto-completion app',
                                    ],
                                    style = {'color':sub_title, 'fontWeight': 'bold', 'text-align':'center'},
                                ),
                                html.P('''Predicting the next word in the sentence using NGram models created using R'''),
                                html.Div(
                                    style = {'height':'1em'},
                                )
                            ]),
                            dcc.Input(
                                id="input", 
                                className = 'eleven columns',
                                style = {
                                    'borderRadius':'25px', 
                                },
                                type="text", 
                                placeholder="Enter the sentence",
                                debounce=True
                            ),
                            html.Div(
                                className = 'column',
                                style = {'padding-top':'1.2em'},
                                children = [
                                    html.Div(
                                        className = 'four columns'
                                    ),   
                                    html.Div(
                                        children = [
                                            html.P(
                                                '''Predicted word: '''
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        className = 'four columns',
                                        id = 'display'
                                    )   
                                ]
                            )

                        ]),
                    ]
                ),
            ]
        ),
        # data
        html.Div(id = 'output', style = {'display':'none'}),
    ],
)

@app.callback(
    Output("output", "children"),
    Input("input", "value"),
)
def get_input(input):
    output = predictWord(input)
    if(input!=None):
        return "{} {}".format(input, output)

@app.callback(
    Output("display", "children"),
    Input("output", "children"),
)
def display_predicted_word(input):
    if(input!=None):
        return "{}".format(input)




## Main
if __name__ == '__main__':
    app.run_server(debug = True)