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
stop_words = set(stopwords.words('english'))  

## Data
df_bigram = pd.read_csv("data/top_bigrams.csv", encoding='utf-8')
df_trigram = pd.read_csv("data/top_trigrams.csv", encoding='utf-8')
df_tetragram = pd.read_csv("data/top_tetragrams.csv", encoding='utf-8')

## Autocompletion function
def predictWord(string):
    preds_ = ""
    pred = ""
    string_tokenized = word_tokenize(string)  
    string_filtered = [x for x in string_tokenized if not x in stop_words]
    string = " ".join(string_filtered)
    best_pred = ""
    n_words = len(string_filtered)
    if(n_words == 3):
        matching_tetragrams = df_tetragram[df_tetragram['token'].str.contains(string, flags = re.IGNORECASE)]
        matching_tetragrams['prediction'] = matching_tetragrams['token'].str.extract(string+"[a-zA-Z]*\s([a-zA-Z]+)\s?", flags=re.IGNORECASE)
        matching_tetragrams.dropna(how = 'any', axis = 0, inplace = True)
        matching_tetragrams.sort_values(by = ['freq'],axis = 0, inplace = True, ascending=False)
        best_pred = pd.DataFrame(matching_tetragrams.iloc[0,1:3]).transpose()
    if(n_words == 2 or best_pred.empty):
        matching_trigrams = df_trigram[df_trigram['token'].str.contains(string, flags = re.IGNORECASE)]
        matching_trigrams['prediction'] = matching_trigrams['token'].str.extract(string+"[a-zA-Z]*\s([a-zA-Z]+)\s?", flags=re.IGNORECASE)
        matching_trigrams.dropna(how = 'any', axis = 0, inplace = True)
        matching_trigrams.sort_values(by = ['freq'],axis = 0, inplace = True, ascending=False)
        pred = pd.DataFrame(matching_trigrams.iloc[0,1:3]).transpose()
        if(n_words == 2):
            best_pred = pred
        else:
            if(pred.iloc[0,1]>best_pred.iloc[0,1]):
                best_pred = pred
    if(n_words == 1 or best_pred.empty):
        matching_bigrams = df_bigram[df_bigram['token'].str.contains(string, flags = re.IGNORECASE)]
        matching_bigrams['prediction'] = matching_bigrams['token'].str.extract(string+"[a-zA-Z]*\s([a-zA-Z]+)\s?", flags=re.IGNORECASE)
        matching_bigrams.dropna(how = 'any', axis = 0, inplace = True)
        matching_bigrams.sort_values(by = ['freq'],axis = 0, inplace = True, ascending=False)
        pred = pd.DataFrame(matching_bigrams.iloc[0,1:3]).transpose()
        if(n_words == 1):
            best_pred = pred
        else:
            if(pred.iloc[0,1]>best_pred.iloc[0,1]):
                best_pred = pred
    pred_word = best_pred.iloc[0,1]
    return(pred_word)

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
                        'backgroundImage': 'linear-gradient(to right top, #b0abc4, #a8aec8, #a0b2c9, #9ab5c9, #95b8c6)'},
                    children = [
                        html.Div(children = [
                            html.Div(children = [
                                html.H2(
                                    children = [
                                        'Text auto-completion app',
                                    ],
                                    style = {'color':sub_title, 'fontWeight': 'bold', 'textAlign':'center'},
                                ),
                                html.Div(
                                    className = 'column',
                                    style = {'paddingBottom':'1.2em'},
                                    children = [
                                        html.Div(
                                            className = 'four columns',
                                        ),   
                                        html.P('''Predicting the next word in the sentence using NGram models created using R'''),
                                        html.P('''Return/Enter to predict'''),
                                    ]
                                ),
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
                                autoComplete ='off',
                                debounce=True
                            ),
                            html.Div(
                                className = 'column',
                                style = {'paddingTop':'1.2em'},
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
                                        # className = 'four columns',
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
    string = " ".join(word_tokenize(input)[-3:])
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
    app.run_server()