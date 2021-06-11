# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from gensim.models import word2vec
import itertools
from itertools import product
from itertools import combinations 
from tqdm import tqdm

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
model_folder_path = dataiku.Folder("m9JZdV7b").get_path()
model_path = model_folder_path + "/word2vec_ramen_model.model"
ramen_model = word2vec.Word2Vec.load(model_path)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
reviews_TF_IDF = dataiku.Dataset("reviews_TF_IDF")
df = reviews_TF_IDF.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
tripAdvisor_path = dataiku.Folder("FXMfF0DU").get_path() + "/TripAdvisor_top_TFIDF_words.txt"
f = open(tripAdvisor_path,'r',encoding="utf-8")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
words_ta = []
for i,data in enumerate(f):
    word = data.replace("'",'').replace('[','').replace(']','').replace(' ','').replace('\n','')
    words_ta.append(word)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
word_ta_vectors = [ramen_model.wv[w] for w in words_ta]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
word_list = []
arr = df['texts_tfidf_sorted_top20'].values
for a in arr:
    l = a.replace("'", "").replace("[", "").replace("]", "").replace(" ", "").split(",")
    word_list.append(l)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
word_list.append(words_ta)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
i = 0
for l in word_list:
    for w in l:
        i += 1

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
print("{} words detected before removing duplicates".format(i))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
uniq_words = list(set(itertools.chain.from_iterable(word_list)))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
print("{} words detected after removing duplicates".format(len(uniq_words)))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def combine(arr, s): 
    return list(combinations(arr, s))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
len(combine(uniq_words, 2))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#scores = {}
#for word1, word2 in product(uniq_words, repeat=2):
#    # print(word1, word2)
#    scores[(word1, word2)] =  cos_sim(ramen_model.wv[word1], ramen_model.wv[word2])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
scores = {}
for touple in tqdm(combine(uniq_words, 2)):
    # print(word1, word2)
    similarity = cos_sim(ramen_model.wv[touple[0]], ramen_model.wv[touple[1]])
    scores[(touple[0], touple[1])] = similarity
    scores[(touple[1], touple[0])] = similarity

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# score of the same words is 1
for w in tqdm(uniq_words):
    scores[(w, w)] = 1

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
"""
avg_avg_scores = []
for word_2 in tqdm(words_ta):
    avg_scores = []
    for review in df["texts_tfidf_sorted_top20"].values:
        review = review.replace("'", "").replace("[", "").replace("]", "").replace(" ", "").split(",")
        word_cross_scores = []
        for word_1 in review:
            score = scores[(word_1, word_2)]
            word_cross_scores.append(score)
        avg_scores.append(np.mean(word_cross_scores))
    avg_avg_scores.append(np.mean(avg_scores))
"""

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
avg_avg_scores = []
for review in tqdm(df["texts_tfidf_sorted_top20"].values):
    review = review.replace("'", "").replace("[", "").replace("]", "").replace(" ", "").split(",")
    avg_scores = []
    for word_1 in review:
        word_cross_scores = []
        for word_2 in words_ta:
            score = scores[(word_1, word_2)]
            word_cross_scores.append(score)
        avg_scores.append(np.mean(word_cross_scores))
    avg_avg_scores.append(np.mean(avg_scores))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
len(avg_avg_scores)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df['similarity_score'] = avg_avg_scores

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
recommendation = dataiku.Dataset("recommendation")
recommendation.write_with_schema(df)