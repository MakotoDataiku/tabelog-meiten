import plotly.express as px
import dataiku
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from gensim.models import word2vec
from googletrans import Translator
from dash.dependencies import Input, Output, State
from deep_translator import GoogleTranslator
import plotly.graph_objects as go
import numpy as np
import dash_daq as daq


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

df_dict = {}
for c in df['cluster_labels'].unique():
    df_dict[c] = df[df['cluster_labels']==c]

clusters = df['cluster_labels'].values

# colors
gridcolor = 'rgb(204, 204, 0)'
titlecolor = 'rgb(230, 230, 0)'
palette = px.colors.qualitative.Light24
clusters_unique = df['cluster_labels'].unique()
color_dict = {clusters_unique[i]:palette[i] for i in range(len(clusters_unique))}
cluster_color = [color_dict[c] for c in clusters]


# others
translator = GoogleTranslator(source='japanese', target='english')  # output -> Weiter so, du bist großartig

# Components
switchClustering = daq.ToggleSwitch(
    id='switch-clustering',
    value=False,
    size = 50,
    labelPosition='top',
    label = dict(
        label='Clustering', 
        style={'color':"white"}
        )
    )

legend_dict = dict(
    itemsizing="constant",
    #itemwidth=30,
    yanchor="top",
    y=1.04,
    xanchor="left",
    x=0.01,
    font_color='white',
    title_font_color='white',
    orientation="h",
    font_size =20,

)

scene_dict = dict(
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
    )
)

textbox_pos = dcc.Textarea(
    id='text-pos',
    value = 'ラーメン 北海道',
    style={'width': '40%', 'height': 20, 'horizontal-align':'middle'},
    )

textbox_neg = dcc.Textarea(
    id='text-neg',
    value = '',
    style={'width': '40%', 'height': 20},
    )


scatterPlot = dcc.Graph(
        id='scatter-plot',
        #figure=fig,
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
submitButton2 = html.Button('Submit', id='word-button-2', n_clicks=0),

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
                        html.Div(
                            switchClustering, 
                            style={'height':100}
                        ),
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
            
        ),
        html.Div(
            children = [
                html.Div(
                    children=[
                        html.H2("Words to add", style={'color':'white'}),
                        html.Div(textbox_pos)
                    ],
                    style={
                        'backgroundColor':'black', 
                        'width': '40%',
                        'display': 'inline-block',
                        'textAlign': 'center'
                    }
                ),
                html.Div(
                    children=[
                        html.H2("Words to subtract", style={'color':'white'}),
                        html.Div(textbox_neg)
                    ],
                    style={
                        'backgroundColor':'black', 
                        'width': '40%',
                        'display': 'inline-block',
                        'textAlign': 'center'
                    }
                ),
                html.Div(
                    submitButton2,
                    style={
                        'backgroundColor':'black', 
                        'width': '10%',
                        'display': 'inline-block',
                        'textAlign': 'center'
                    }
                    
                )
            ]
        ),
        html.Div(
            id="word-play-box",
            style={
                'backgroundColor':'black',
                'textAlign': 'center'
            }
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
        try:
            similar_words = ramen_model.wv.most_similar(value)
            print(similar_words)
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
        except KeyError:
            return html.P("Ramen model doesn't know the word {}.".format(str(value)), style = {'color':'white'})
    
    
@app.callback(
    Output('wiki-similar-words', 'children'),
    Input('word-button', 'n_clicks'),
    State('word', 'value'),
)
def update_wiki_output(n_clicks, value):
    if n_clicks > 0:
        try:
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
        except KeyError:
            return html.P("Wiki model doesn't know the word {}.".format(str(value)), style = {'color':'white'})
    

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('word-button', 'n_clicks'),
    State('word', 'value'),
)
def update_plot(n_clicks, value):
    if n_clicks == 0:
        
        fig = go.Figure()
        for c in df_dict.keys():
            df_c = df_dict[c]
            x = df_c['x'].values
            y = df_c['y'].values
            z = df_c['z'].values
            words = df_c['words'].values
            fig.add_trace(
                go.Scatter3d(
                    x=x, 
                    y=y,
                    z=z,
                    mode='markers',
                    name=c,
                    text = words,
                    hovertemplate = '%{text}<extra></extra>',
                    marker=dict(
                        size=3,
                        opacity=0.8
                    ),
                ),
            )
            
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor="black",
            legend = legend_dict,
            scene = scene_dict
        )
        
        return fig
            
    elif n_clicks > 0:
        similar_words = ramen_model.wv.most_similar(value)
        list_words = [w[0] for w in similar_words]
        print(list_words)
        df_selected = df[df['words'].isin(list_words)]
        x_selected = df_selected['x'].values
        y_selected = df_selected['y'].values
        z_selected = df_selected['z'].values
        words_selected = df_selected['words'].values
        words_translated = [translator.translate(w) for w in words_selected]
        print(words_translated)
        fig = go.Figure()
        
        for c in df_dict.keys():
            df_c = df_dict[c]
            x = df_c['x'].values
            y = df_c['y'].values
            z = df_c['z'].values
            words = df_c['words'].values
            fig.add_trace(
                go.Scatter3d(
                    x=x, y=y, z=z,
                    mode='markers',
                    name=c,
                    text = words,
                    hovertemplate = '%{text}<extra></extra>',
                    marker=dict(
                        size=3,
                        opacity=0.8
                    ),
                ),
            )
        
        fig.add_trace(
            go.Scatter3d(
                x = x_selected,
                y = y_selected,
                z = z_selected,
                mode='markers',
                name="Similar words",
                text = ['{}:{}'.format(w, t) for w, t in zip(words_selected, words_translated)],
                hovertemplate = '%{text}<extra></extra>',
                marker=dict(
                    size=30,
                    opacity=1,
                    color="yellow",
                ),
            )
        )
        
            
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor="black",
            legend = legend_dict,
            scene = scene_dict
        )
        
        return fig

@app.callback(
    Output('word-play-box', 'children'),
    Input('word-button-2', 'n_clicks'),
    State('text-pos', 'value'),
    State('text-neg', 'value'),
)
def update_word_play(n_clicks, value_pos, value_neg):
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
        #list_words = [w[0] for w in similar_words]
        textarea = []
        for w in similar_words:
            # w_en = translator.translate(w[0], dest='en').text
            w_en = translator.translate(w[0])
            pair = str(w[0]) + " : " + str(w_en)
            textarea.append(pair)
            textarea.append(html.Br()) 
        div = html.P(
            children = [
                html.H3("Result"),
                html.Div(textarea)
            ],
            style = {'color':'white'})
        return div