import plotly.express as px
import dataiku
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd





# Uncomment the following to read your own dataset
dataset = dataiku.Dataset("w2v_for_viz")
df = dataset.get_dataframe()

fig = px.scatter_3d(df, x='x', y='y', z='z', 
                    opacity=0.4, 
                    hover_data=["vocabs"])

fig.update_layout(plot_bgcolor='black')


app.layout = html.Div(children=[
    html.H1(
        children='Vizualizing the ramen universe',
        style={'backgroundColor':'black'}),

    dcc.Graph(
        id='example-graph',
        figure=fig,
        style={
            'height':1000, 
            'width':'100%', 
            'backgroundColor':'black'
        }
    )
])
