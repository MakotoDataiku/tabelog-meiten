import plotly.express as px
import dataiku
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dataiku import pandasutils as pdu
from gensim.models import word2vec

# Loading ramen model
folder_path = dataiku.Folder("m9JZdV7b").get_path()
model_path = folder_path + "/word2vec_ramen_model.model"
print(model_path)
ramen_model = word2vec.Word2Vec.load(model_path)

# Loading generic model
wiki_model_path = "/Users/mmiyazaki/dataiku/Design/DATA_DIR/managed_folders/WIKIPEDIAJP/jU2z0VpV/word2vec_model.model"
wiki_model = word2vec.Word2Vec.load(wiki_model_path)
print(ramen_model.most_similar("山岸"))

# This loads dummy data into a dataframe



# Components

textbox = dcc.Textarea(
        id='textarea',
        value='Textarea content initialized\nwith multiple lines of text',
        style={'width': '100%', 'height': 40},
    )
    

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(textbox),
    html.Div(id='textarea-output', style={'whiteSpace': 'pre-line'})
])
