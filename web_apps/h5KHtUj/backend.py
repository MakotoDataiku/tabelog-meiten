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
print("model_path")
ramen_model = word2vec.Word2Vec.load(model_path)

# Loading generic model



ramen_model.most_similar("山岸")

# This loads dummy data into a dataframe
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
}) \
 \
# Uncomment the following to read your own dataset
#dataset = dataiku.Dataset("YOUR_DATASET_NAME_HERE")
#df = dataset.get_dataframe()

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
