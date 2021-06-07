import plotly.express as px
import dataiku
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from gensim.models import word2vec
from googletrans import Translator
from dash.dependencies import Input, Output, State
from deep_translator import GoogleTranslator


# Loading ramen model
folder_path = dataiku.Folder("m9JZdV7b").get_path()
model_path = folder_path + "/word2vec_ramen_model.model"
print(model_path)
ramen_model = word2vec.Word2Vec.load(model_path)

# Loading generic model
wiki_model_path = "/Users/mmiyazaki/dataiku/Design/DATA_DIR/managed_folders/WIKIPEDIAJP/jU2z0VpV/word2vec_model.model"
wiki_model = word2vec.Word2Vec.load(wiki_model_path)



# Loading dataset
dataset = dataiku.Dataset("w2v_for_viz_clustered_prepared")
df = dataset.get_dataframe()
df['size'] = 3

# colors
gridcolor = 'rgb(204, 204, 0)'
titlecolor = 'rgb(230, 230, 0)'

# others
# translator = Translator(service_urls=['translate.googleapis.com'])
translator = GoogleTranslator(source='japanese', target='english')  # output -> Weiter so, du bist großartig

# Components
fig = px.scatter_3d(df, x='x', y='y', z='z', 
                    opacity=0.8, 
                    color='cluster_labels',
                    # size = pd.Series([3]*df.shape[0]),
                    size = 'size',
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
        font_size =15
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

list_words = ["豚骨", "醤油"]
df_points = df[df['words'].isin(list_words)]
indices = df_points.index
df.loc[df['words'].isin(list_words), 'size'] = 50
#print(indices)
#sizes = pd.Series([3]*df.shape[0])
#sizes[indices] = 15
# colors = ['blue',]*10
# colors[point["pointNumber"]] = 'red'

        
fig.update_traces(marker=dict(
    #size=2,
    #size = df['size'],
    line=dict(
        width=0,
        color='DarkSlateGrey')),
                  # selector=dict(mode='markers')
                 )

fig.add_traces(
    data=[px.scatter_3d(df_points, x='x', y='y', z='z')]
    
)


scatterPlot = dcc.Graph(
        id='3d-plot',
        figure=fig,
        style={
            'height':1000, 
            'width':'100%', 
            'backgroundColor':'black'
        }
    )


textbox = dcc.Textarea(
    id='word',
    value = 'ラーメン',
    style={'width': '80%', 'height': 20},
    )
submitButton = html.Button('Submit', id='word-button', n_clicks=0),


# Layouts
app.layout = html.Div(
    children=[
        html.H1(
            children='Vizualizing the ramen universe',
            style={
                'backgroundColor':'black', 
                'color': titlecolor,
                'text-align': 'center'
            }
        ),
        html.Div(
            children=[
                html.Div(
                    scatterPlot, 
                    style={
                        'backgroundColor':'black', 
                        'width': '80%',
                        'display': 'inline-block',
                        'vertical-align': 'middle'
                    }),
                html.Div(
                    children=[
                        html.Div(textbox),
                        html.Div(submitButton),
                        html.Div(id='ramen-similar-words'),
                        html.Div(id='wiki-similar-words')
                    ],
                    style={
                        'backgroundColor':'black', 
                        'width': '20%',
                        'display': 'inline-block',
                        'vertical-align': 'middle'
                    }
                )
            ],
            
        )
    ], 
    style={'backgroundColor':'black'})


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
            # w_en = translator.translate(w[0], dest='en').text
            w_en = translator.translate(w[0])
            pair = str(w[0]) + " : " + str(w_en)
            textarea.append(pair)
            textarea.append(html.Br()) 
        div = html.P(
            children = [
                html.H3("Ramen model"),
                html.Div(textarea)
            ],
            style = {'color':'white'})
        return div
    
    
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
            # w_en = translator.translate(w[0], dest='en').text
            w_en = translator.translate(w[0])
            pair = str(w[0]) + " : " + str(w_en)
            textarea.append(pair)
            textarea.append(html.Br())      
        div = html.P(
            children = [
                html.H3("Wikipedia model"),
                html.Div(textarea)
            ],
            style = {'color':'white'})
        return div
    
"""
@app.callback(
    Output('3d-plot', 'figure'),
    Input('word-button', 'n_clicks'),
    State('word', 'value'),
)
def update_plot(n_clicks, value):
    if n_clicks > 0:
        similar_words = ramen_model.wv.most_similar(value)
        list_words = [w[0] for w in simliar_words]
        indices = df[df['words'].isin(list_words)].index
        
        fig = px.scatter_3d(df, x='x', y='y', z='z', 
                        opacity=0.8, 
                        color='cluster_labels',
                        size = pd.Series([3]*df.shape[0]),
                        size[df["words"].isin(list_words)] = 15,
                        hover_data={
                           'x':False,
                           'y':False,
                           'z':False,
                           'words':True,
                           'cluster_labels':False
                        }
                           )
        
        sizes = pd.Series([3]*df.shape[0])
        sizes[indices] = 15
        # colors = ['blue',]*10
        # colors[point["pointNumber"]] = 'red'
        fig.update_traces(
            marker_size=sizes, 
            #marker_color=colors
        )
        # fig.add_trace(px.scatter_3d(0,0,0))
        return fig
"""