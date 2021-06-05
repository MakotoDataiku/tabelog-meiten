import plotly.express as px
import dataiku
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dataiku import pandasutils as pdu
from gensim.models import word2vec
from dash.dependencies import Input, Output, State
import dash_table as dt

# Loading ramen model
folder_path = dataiku.Folder("m9JZdV7b").get_path()
model_path = folder_path + "/word2vec_ramen_model.model"
print(model_path)
ramen_model = word2vec.Word2Vec.load(model_path)

# Loading generic model
wiki_model_path = "/Users/mmiyazaki/dataiku/Design/DATA_DIR/managed_folders/WIKIPEDIAJP/jU2z0VpV/word2vec_model.model"
wiki_model = word2vec.Word2Vec.load(wiki_model_path)


# This loads dummy data into a dataframe



# Components

textbox = dcc.Textarea(
    id='word',
    value = 'ラーメン',
    style={'width': '100%', 'height': 40},
    )

ramen_table = dt.DataTable(
    id='ramen-table',
)

# Layouts
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(textbox),
    html.Button('Submit', id='word-button', n_clicks=0),
    html.Div(children = [
        html.Div(children = [
            html.Div("Ramen model"),
            html.Div(id='ramen-similar-words'),
            html.Div(ramen_table)
        ], style={'width': '40%', 'display': 'inline-block'}),
        html.Div(children = [
            html.Div("Generic model(Wikipedia) model"),
            html.Div(id='wiki-similar-words')
        ], style={'width': '40%', 'display': 'inline-block'})
    ])
    #html.Div(, style={'whiteSpace': 'pre-line'})
])

# Callbacks
@app.callback(
    Output('ramen-similar-words', 'children'),
    #Output('ramen-table', 'data'),
    Input('word-button', 'n_clicks'),
    State('word', 'value'),
)
def update_ramen_output(n_clicks, value):
    if n_clicks > 0:
        similar_words = ramen_model.wv.most_similar(value)
        df = pd.DataFrame(similar_words, columns=["words", "score"])
        text = ""
        for w in similar_words:
            #print(w)
            # text.join(str(w)+"\n")
            text = text + str(w) + "\n"
        #print(text)
        md = dcc.Markdown(text)
        print(df.to_dict('records'))

        return df.to_dict('rows')

@app.callback(
    Output('wiki-similar-words', 'children'),
    Input('word-button', 'n_clicks'),
    State('word', 'value'),
)
def update_wiki_output(n_clicks, value):
    if n_clicks > 0:
        similar_words = wiki_model.wv.most_similar(value)
        
        text = ""
        for w in similar_words:
            #print(w)
            # text.join(str(w)+"\n")
            text = text + str(w) + "\n"
        print(text)
        md = dcc.Markdown(text)
        return md