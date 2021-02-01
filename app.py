import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import re

import nltk 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import pandas as pd
import numpy as np

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
app.title = 'Text autocompletion app'

## Colors
title_main = '#DA4167'
sub_title = '#253D5B'
bg_color = '#bbf1fa'
fg_color = '#51c2d5'

## NLTK 
stop_words = set(stopwords.words('english'))  

## Data
NGrams = pd.read_csv("data/NGrams.csv", encoding='utf-8')

## Autocompletion function
def predictWord(string):
    preds_ = ""
    pred = ""
    string = string.lower()
    best_pred = pd.DataFrame()
    n_words = len(word_tokenize(string))
    if(n_words > 4):
        string_tokenized = word_tokenize(string)[-4:]
        string = " ".join(string_tokenized)
        n_words = 4
    if(n_words == 4):
        matching_pentagrams = NGrams.loc[NGrams['which']==5,['token','freq']][NGrams.loc[NGrams['which']==5,['token','freq']]['token'].str.startswith(string, na=False)]
        matching_pentagrams['prediction'] = matching_pentagrams['token'].str.extract(string+"\s([a-zA-Z]+)\s?", flags=re.IGNORECASE)
        matching_pentagrams.dropna(how = 'any', axis = 0, inplace = True)
        matching_pentagrams.sort_values(by = ['freq'],axis = 0, inplace = True, ascending=False)
        if(matching_pentagrams.empty==False):
            best_pred = pd.DataFrame(matching_pentagrams.iloc[0,1:3]).transpose()
        else:
            string_tokenized = word_tokenize(string)[-3:]
            string = " ".join(string_tokenized)
            n_words = 3
    if(n_words == 3):
        matching_tetragrams = NGrams.loc[NGrams['which']==4,['token','freq']][NGrams.loc[NGrams['which']==4,['token','freq']]['token'].str.startswith(string, na=False)]
        matching_tetragrams['prediction'] = matching_tetragrams['token'].str.extract(string+"[a-zA-Z]*\s([a-zA-Z]+)\s?", flags=re.IGNORECASE)
        matching_tetragrams.dropna(how = 'any', axis = 0, inplace = True)
        matching_tetragrams.sort_values(by = ['freq'],axis = 0, inplace = True, ascending=False)
        if(matching_tetragrams.empty==False):
            best_pred = pd.DataFrame(matching_tetragrams.iloc[0,1:3]).transpose()
        else:
            string_tokenized = word_tokenize(string)[-2:]
            string = " ".join(string_tokenized)
            n_words = 2
    if(n_words == 2):
        matching_trigrams = NGrams.loc[NGrams['which']==3,['token','freq']][NGrams.loc[NGrams['which']==3,['token','freq']]['token'].str.startswith(string, na=False)]
        matching_trigrams['prediction'] = matching_trigrams['token'].str.extract(string+"[a-zA-Z]*\s([a-zA-Z]+)\s?", flags=re.IGNORECASE)
        matching_trigrams.dropna(how = 'any', axis = 0, inplace = True)
        matching_trigrams.sort_values(by = ['freq'],axis = 0, inplace = True, ascending=False)
        if(matching_trigrams.empty==False):
            best_pred = pd.DataFrame(matching_trigrams.iloc[0,1:3]).transpose()
        else:
            string_tokenized = word_tokenize(string)[-1:]
            string = " ".join(string_tokenized)
            n_words = 1
    if(n_words == 1):
        matching_bigrams = NGrams.loc[NGrams['which']==2,['token','freq']][NGrams.loc[NGrams['which']==2,['token','freq']]['token'].str.startswith(string, na=False)]
        matching_bigrams['prediction'] = matching_bigrams['token'].str.extract(string+"[a-zA-Z]*\s([a-zA-Z]+)\s?", flags=re.IGNORECASE)
        matching_bigrams.dropna(how = 'any', axis = 0, inplace = True)
        matching_bigrams.sort_values(by = ['freq'],axis = 0, inplace = True, ascending=False)
        if(matching_bigrams.empty==False):
            best_pred = pd.DataFrame(matching_bigrams.iloc[0,1:3]).transpose()
    if(best_pred.empty==False):
        return(best_pred.iloc[0,1])
    return("N/A")

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
                                # debounce=True
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
        # Footer 
        html.Div(
            className = 'column',
            # style = {'margin':'1em'},
            children = [
                html.Div(
                    style = {'paddingTop':'2.4em','paddingLeft':'2.4em','paddingRight':'2.4em','paddingBottom':'0.4em','borderRadius':'25px'},
                    children = [
                        dcc.Markdown(
                            '''
## Summary 
Creating a text completion app using **NGram** modelling, which uses *bigrams*, 
*trigrams*, *tetragrams*, and *pentagram* created from various data sources:  
- News  
- Blogs  
- Twitter  
                            '''
                            )
                    ]
                ),
                html.Div(
                    style = {'paddingTop':'0.4em','paddingLeft':'2.4em','paddingRight':'2.4em','paddingBottom':'0.4em','borderRadius':'25px'},
                    children = [
                        html.P('''The Ngrams were created in RStudio’s R environment and has been published on kaggle as well as Rpubs, and the application was created in python using Dash by plotly.'''),
                        dcc.Markdown(
                            '''
Modelling   
- [Kaggle](https://www.kaggle.com/aquaregis32/text-mining-rmarkdown)  
- [Rpubs](https://rpubs.com/aquaregis32/textmining_analysisfor_autocomplete_byAR32)  
 
                            '''
                            )
                    ]
                ),
                html.Div(
                    style = {'paddingTop':'0.4em','paddingLeft':'2.4em','paddingRight':'2.4em','paddingBottom':'0.4em','borderRadius':'25px'},
                    children = [
                        dcc.Markdown(
                            '''
### NGram models 
The Ngrams were created for each of the data sources using NGramTokenizer and 
TermDocumentMatrix, which was then converted to matrix - The highest memory 
allocation required to build the matrices was 8gb during the process.  

Once created each of the bigrams, trigrams, tetragrams and pentagrams were combined into one
dataset by indicating type of NGram they represented using the *which* field.  

The dataset contains the *token*, frequency of occurance - *freq*, and the *which*  

### Application 
The application has been built completely using python, the R function to 
predict the word was rewritten in python instead of using RScript.   

The application uses Dash by plotly to create the web app which renders html
content to any supporting browser.   

The UI is fairly simple, with only some text describing the app and an input box
It useses bootstrap-grid.css available openly, and uses NLTK, pandas, re (for
regular expression) libraries for running the code and predicting the output.

User can input the sentence and once entered upon pressing return, the predicted
output/predicted next word for the sentence input will be displayed right below
text input box.   
                            '''
                            )
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
        return "{}".format(output)

@app.callback(
    Output("display", "children"),
    Input("output", "children"),
)
def display_predicted_word(input):
    if(input!=None):
        return "{}".format(input)




## Main
if __name__ == '__main__':
    app.run_server(debug=True)