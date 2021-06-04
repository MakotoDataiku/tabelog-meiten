# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora
from gensim import models

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
df = dataiku.Dataset("ramen_clusters_named").get_dataframe()
raw_ramen_df = dataiku.Dataset("raw_ramen").get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
client = dataiku.api_client()
project = client.get_project(dataiku.get_custom_variables()['projectKey'])
project_variables = project.get_variables()
clusters_to_select = project_variables['standard']['clusters_to_select']
list_vocabs = df[df['cluster_labels'].isin(['営業形態', '味・具材'])]['words_concat'].values

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
ramen_word = list_vocabs[0].split(",") + list_vocabs[1].split(",")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
folder_path = dataiku.Folder("aLTWBozg").get_path()
text_path = folder_path + "/ramen_corpus.txt"

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
f = open(text_path,'r',encoding="utf-8")
trainings = []

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
for i,data in enumerate(f):
    word = data.replace("'",'').replace('[','').replace(']','').replace(' ','').replace('\n','').split(",")
    trainings.append([i for i in word if i in ramen_word])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
len(trainings)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
dictionary = corpora.Dictionary(trainings)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
dictionary.num_docs, dictionary.num_pos

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# saving the dictionary in a folder
# for later use
folder_path = dataiku.Folder("POe5uF4H").get_path()
filename = folder_path + "/ramen_dictionary"
dictionary.save(filename)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
corpus = list(map(dictionary.doc2bow, trainings))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE

test_model = models.TfidfModel(corpus) # fit tfidf model

# saving tf-idf model
tf_idf_folder_path = dataiku.Folder("tMMk2S0T").get_path()
path_tf_idf = tf_idf_folder_path + "/tf_idf"
test_model.save(path_tf_idf)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
corpus_tfidf = test_model[corpus] # apply model to the corpus (just like 'transform' in scikit-learn)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# id->単語へ変換
texts_tfidf = [] # id -> 単語表示に変えた文書ごとのTF-IDF
for doc in corpus_tfidf:
    text_tfidf = []
    for word in doc:
        text_tfidf.append([dictionary[word[0]],word[1]])
    texts_tfidf.append(text_tfidf)

from operator import itemgetter

texts_tfidf_sorted_top20 = []

# TF-IDF値を高い順に並び替え上位単語20個に絞る。
# 各ラーメン店のレビューにおいて、TF-IDF値の高い20単語だけが残る。
for i in range(len(texts_tfidf)):
    soted = sorted(texts_tfidf[i], key=itemgetter(1), reverse=True)
    soted_top20 = soted[:20]
    word_list = []
    for k in range(len(soted_top20)):
        word = soted_top20[k][0]
        word_list.append(word)
    texts_tfidf_sorted_top20.append(word_list)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
ramen_by_restaurant = raw_ramen_df.groupby(['store_name', 'address', 'ward', 'score', 'review_cnt'])['review'].apply(list).apply(' '.join).reset_index().sort_values('score', ascending=False)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
ramen_by_restaurant.shape

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
ramen_by_restaurant.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
ramen_by_restaurant['texts_tfidf_sorted_top20'] = texts_tfidf_sorted_top20

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
ramen_by_restaurant['id'] = ['ID-' + str(i + 1).zfill(6) for i in range(len(ramen_by_restaurant.index))]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
ramen_by_restaurant = ramen_by_restaurant.reset_index(drop=True)


py_recipe_output = dataiku.Dataset("reviews_TF_IDF")
py_recipe_output.write_with_schema(ramen_by_restaurant)