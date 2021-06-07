import plotly.express as px
import dataiku
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd





dataset = dataiku.Dataset("w2v_for_viz_clustered_prepared")
df = dataset.get_dataframe()

# colors
gridcolor = 'rgb(204, 204, 0)'
titlecolor = 'rgb(230, 230, 0)'


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
    legend=dict(
        yanchor="top",
        y=1.04,
        xanchor="left",
        x=0.01,
        font_color='white',
        title_font_color='white',
        orientation="h",
        font_size =20
    ),
    scene = dict(
        xaxis = dict(
            # backgroundcolor="rgb(200, 200, 230)",
            backgroundcolor="black",
            gridcolor=gridcolor,
            showbackground=True,
            zerolinecolor=gridcolor,
        ),
        yaxis = dict(
            # backgroundcolor="rgb(230, 200,230)",
            backgroundcolor="black",
            gridcolor=gridcolor,
            showbackground=True,
            zerolinecolor=gridcolor
        ),
        zaxis = dict(
            # backgroundcolor="rgb(230, 230,200)",
            backgroundcolor="black",
            gridcolor=gridcolor,
            showbackground=True,
            zerolinecolor=gridcolor,
        )))

fig.update_traces(marker=dict(size=2,
                              line=dict(
                                  width=0,
                                  color='DarkSlateGrey')),
                  # selector=dict(mode='markers')
                 )


app.layout = html.Div(children=[
    html.H1(
        children='Vizualizing the ramen universe',
        style={
            'backgroundColor':'black', 
            'color': titlecolor,
            'text-align': 'center'
        }),

    html.Div(dcc.Graph(
        id='example-graph',
        figure=fig,
        style={
            'height':1000, 
            'width':'100%', 
            'backgroundColor':'black'
        }
    ), style={'backgroundColor':'black'})
], style={'backgroundColor':'black'})
