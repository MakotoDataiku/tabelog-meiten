import plotly.express as px
import dataiku
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dataiku import pandasutils as pdu
from gensim.models import word2vec
from dash.dependencies import Input, Output, State
import dash_table as dt
from googletrans import Translator

# Loading ramen model
folder_path = dataiku.Folder("m9JZdV7b").get_path()
model_path = folder_path + "/word2vec_ramen_model.model"
print(model_path)
ramen_model = word2vec.Word2Vec.load(model_path)

# Loading generic model
wiki_model_path = "/Users/mmiyazaki/dataiku/Design/DATA_DIR/managed_folders/WIKIPEDIAJP/jU2z0VpV/word2vec_model.model"
wiki_model = word2vec.Word2Vec.load(wiki_model_path)

# Some functions
translator = Translator(service_urls=['translate.googleapis.com'])

# Components

textbox = dcc.Textarea(
    id='word',
    value = 'ラーメン',
    style={'width': '100%', 'height': 40},
    )

textbox_pos = dcc.Textarea(
    id='text-pos',
    value = 'ラーメン 北海道',
    style={'width': '100%', 'height': 40},
    )

textbox_neg = dcc.Textarea(
    id='text-neg',
    value = '',
    style={'width': '100%', 'height': 40},
    )


# Layouts
app.layout = html.Div(children=[
    html.H1(children='Lost in the Ramen Universe'),
    html.Div(textbox),
    html.Button('Submit', id='word-button', n_clicks=0),
    html.Div(children = [
        html.Div(children = [
            html.Div("Ramen model"),
            html.Div(id='ramen-similar-words'),
        ], style={'width': '40%', 'display': 'inline-block'}),
        html.Div(children = [
            html.Div("Generic model(Wikipedia) model"),
            html.Div(id='wiki-similar-words')
        ], style={'width': '40%', 'display': 'inline-block'})
    ]),
    html.Div(children=[
        html.Div(textbox_pos, style={'width': '40%', 'display': 'inline-block'}),
        html.Div(textbox_neg, style={'width': '40%', 'display': 'inline-block'})
    ]),
    html.Button('Submit', id='word-button2', n_clicks=0),
    html.Div(children = [
        html.Div(children = [
            html.Div("Ramen model"),
            html.Div(id='ramen-wordplay'),
        ], style={'width': '40%', 'display': 'inline-block'}),
        html.Div(children = [
            html.Div("Generic model(Wikipedia) model"),
            html.Div(id='wiki-wordplay')
        ], style={'width': '40%', 'display': 'inline-block'})
    ]),
])

# Callbacks
@app.callback(
    Output('ramen-similar-words', 'children'),
    Input('word-button', 'n_clicks'),
    State('word', 'value'),
)
def update_ramen_output(n_clicks, value):
    if n_clicks > 0:
        similar_words = ramen_model.wv.most_similar(value)
        textarea = []
        for w in similar_words:
            y = list(w)
            # y[1] = round(y[1], 4)
            y[1] = translator.translate(y[0], dest='en').text
            w = tuple(y)
            textarea.append(str(w))
            textarea.append(html.Br())      
        return html.P(textarea)

@app.callback(
    Output('wiki-similar-words', 'children'),
    Input('word-button', 'n_clicks'),
    State('word', 'value'),
)
def update_wiki_output(n_clicks, value):
    if n_clicks > 0:
        similar_words = wiki_model.wv.most_similar(value)
        textarea = []
        for w in similar_words:
            y = list(w)
            # y[1] = round(y[1], 4)
            y[1] = translator.translate(y[0], dest='en').text
            w = tuple(y)
            textarea.append(str(w))
            textarea.append(html.Br())      
        return html.P(textarea)
    
@app.callback(
    Output('ramen-wordplay', 'children'),
    Input('word-button2', 'n_clicks'),
    State('text-pos', 'value'),
    State('text-neg', 'value'),
)
def update_ramen_output(n_clicks, value_pos, value_neg):
    if n_clicks > 0:
        print(value_pos, value_neg)
        list_pos = value_pos.replace(" ", ",").replace("　", ",").replace("、", ",").split(",")
        list_neg = value_neg.replace(" ", ",").replace("　", ",").replace("、", ",").split(",")
        print(list_pos, list_neg)
        if len(list_neg) == 1 and len(list_neg[0]) == 0:
            similar_words = ramen_model.most_similar(positive=list_pos)
        else:
            similar_words = ramen_model.most_similar(positive=list_pos, negative=list_neg)
        print(similar_words)
        textarea = []
        for w in similar_words:
            y = list(w)
            y[1] = round(y[1], 4)
            y[0] = translator.translate(y[0], dest='en').text
            w = tuple(y)
            textarea.append(str(w))
            textarea.append(html.Br())      
        return html.P(textarea)

@app.callback(
    Output('wiki-wordplay', 'children'),
    Input('word-button2', 'n_clicks'),
    State('text-pos', 'value'),
    State('text-neg', 'value'),
)
def update_ramen_output(n_clicks, value_pos, value_neg):
    if n_clicks > 0:
        print(value_pos, value_neg)
        list_pos = value_pos.replace(" ", ",").replace("　", ",").replace("、", ",").split(",")
        list_neg = value_neg.replace(" ", ",").replace("　", ",").replace("、", ",").split(",")
        print(list_pos, list_neg)
        if len(list_neg) == 1 and len(list_neg[0]) == 0:
            similar_words = wiki_model.most_similar(positive=list_pos)
        else:
            similar_words = wiki_model.most_similar(positive=list_pos, negative=list_neg)
        print(similar_words)
        textarea = []
        for w in similar_words:
            y = list(w)
            y[1] = round(y[1], 4)
            y[0] = translator.translate(y[0], dest='en').text
            w = tuple(y)
            textarea.append(str(w))
            textarea.append(html.Br())      
        return html.P(textarea)