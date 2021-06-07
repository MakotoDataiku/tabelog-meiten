import plotly.express as px
import dataiku
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd





# Uncomment the following to read your own dataset
dataset = dataiku.Dataset("w2v_for_viz_clustered_prepared")
df = dataset.get_dataframe()

fig = px.scatter_3d(df, x='x', y='y', z='z', 
                    opacity=0.8, 
                    color='cluster_labels',
                    size = pd.Series([3]*df.shape[0]),
                    #hover_data=["words"],
                    # hover_data='cluster_labels'
                   
                    hover_data={
                       'x':False,
                       'y':False,
                       'z':False,
                       'words':True,
                       'cluster_labels':False
                   }
                   
                   )

fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor="black",
    legend_bgcolor='white',
    # scene= {'bgcolor': "black"},
    scene = dict(
        xaxis = dict(
            # backgroundcolor="rgb(200, 200, 230)",
            backgroundcolor="black",
            gridcolor="white",
            showbackground=True,
            zerolinecolor="white",
        ),
        yaxis = dict(
            # backgroundcolor="rgb(230, 200,230)",
            backgroundcolor="black",
            gridcolor="white",
            showbackground=True,
            zerolinecolor="white"
        ),
        zaxis = dict(
            # backgroundcolor="rgb(230, 230,200)",
            backgroundcolor="black",
            gridcolor="white",
            showbackground=True,
            zerolinecolor="white",
        )))


app.layout = html.Div(children=[
    html.H1(
        children='Vizualizing the ramen universe',
        style={'backgroundColor':'white'}),

    html.Div(dcc.Graph(
        id='example-graph',
        figure=fig,
        style={
            'height':1000, 
            'width':'80%', 
            'backgroundColor':'black'
        }
    ), style={'backgroundColor':'black'})
])
