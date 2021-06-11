# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from gensim import corpora
from gensim import models
import MeCab
from gensim.models import word2vec
from gensim.models import TfidfModel
from operator import itemgetter

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
your_trip_advisor = dataiku.Dataset("trip_advisor_clustered_prepared")
df = your_trip_advisor.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
tfidf_path = dataiku.Folder("tMMk2S0T").get_path() + "/tf_idf"

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
client = dataiku.api_client()
project = client.get_project(dataiku.get_custom_variables()['projectKey'])
project_variables = project.get_variables()
clusters_to_select = project_variables['standard']['clusters_to_select']
list_vocabs = df[df['cluster_labels'].isin(clusters_to_select)]['words_concat'].values

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
ramen_word = list_vocabs[0].split(",") + list_vocabs[1].split(",")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
ramen_dictionary_path = dataiku.Folder("POe5uF4H").get_path() + "/ramen_dictionary"
dictionary = corpora.Dictionary.load(ramen_dictionary_path)
corpus = list(map(dictionary.doc2bow, [ramen_word]))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
tfidf_model = TfidfModel.load(tfidf_path)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
corpus_tfidf = tfidf_model[corpus]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
corpus_tfidf

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
texts_tfidf = []
for doc in corpus_tfidf:
    text_tfidf = []
    for word in doc:
        text_tfidf.append([dictionary[word[0]],word[1]])
    texts_tfidf.append(text_tfidf)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
texts_tfidf

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
texts_tfidf_sorted_top20 = []


for i in range(len(texts_tfidf)):
    soted = sorted(texts_tfidf[i], key=itemgetter(1), reverse=True)
    soted_top20 = soted[:20]
    word_list = []
    for k in range(len(soted_top20)):
        word = soted_top20[k][0]
        word_list.append(word)
    texts_tfidf_sorted_top20.append(word_list)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
texts_tfidf_sorted_top20

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
text_folder = dataiku.Folder("FXMfF0DU").get_path()
np.savetxt(text_folder + "/TripAdvisor_top_TFIDF_words.txt", texts_tfidf_sorted_top20[0], delimiter = ',', fmt = '%s')