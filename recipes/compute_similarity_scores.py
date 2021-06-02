# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from itertools import product
from gensim.models import word2vec
import itertools
from tqdm import tqdm

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
reviews_TF_IDF = dataiku.Dataset("reviews_TF_IDF")
df = reviews_TF_IDF.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
folder_path = dataiku.Folder("m9JZdV7b").get_path()
model_path = folder_path + "/word2vec_ramen_model.model"
ramen_model = word2vec.Word2Vec.load(model_path)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
store_cross = []
for ids in product(df['id'], repeat=2):
    store_cross.append(ids)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
store_cross_df = pd.DataFrame(store_cross, columns=['id_x', 'id_y'])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
store_cross_detail = store_cross_df.merge(df[['id','store_name','score','review_cnt','texts_tfidf_sorted_top20']], 
                                          how='inner', 
                                          left_on='id_x', 
                                          right_on='id').drop(columns='id').merge(df[['id','store_name','score','review_cnt','texts_tfidf_sorted_top20']], 
                                                                                  how='inner', 
                                                                                  left_on='id_y', 
                                                                                  right_on='id').drop(columns='id')

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
store_cross_detail.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# store_cross_detail = store_cross_detail[store_cross_detail['id_x'].isin(df['id'].loc[0:50])]
store_cross_detail = store_cross_detail.reset_index(drop=True).sort_values(['id_x'])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
##ラーメン店xに対してラーメン店yの類似度を算出
#コサイン類似度を算出する関数を定義
def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#cossimだけの組み合わせ（同じワード同士の組みあわせがでてくるため）
#2次元を１次元にする　setが重複を削除てきなやつ。
# uniq_words = list(set(itertools.chain.from_iterable(df['texts_tfidf_sorted_top20'].values)))
word_list = []
arr = df['texts_tfidf_sorted_top20'].values
for a in arr:
    l = a.replace("'", "").replace("[", "").replace("]", "").replace(" ", "").split(",")
    word_list.append(l)
uniq_words = list(set(itertools.chain.from_iterable(word_list)))    
scores = {}
for word1, word2 in product(uniq_words, repeat=2):
    # print(word1, word2)
    scores[(word1, word2)] =  cos_sim(ramen_model.wv[word1], ramen_model.wv[word2])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
store_cross_detail.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
avg_avg_scores = []
for i in tqdm(range(len(store_cross_detail['texts_tfidf_sorted_top20_x']))):
    avg_scores = []
    x_list = store_cross_detail['texts_tfidf_sorted_top20_x'][i].replace("'", "").replace("[", "").replace("]", "").replace(" ", "").split(",")
    for j in range(len(x_list)):
        word_cross_scores = []
        word_a = x_list[j]
        y_list = store_cross_detail['texts_tfidf_sorted_top20_y'][i].replace("'", "").replace("[", "").replace("]", "").replace(" ", "").split(",")
        for k in range(len(y_list)):
            word_b = y_list[k]
            score = scores[(word_a, word_b)]#単語間のスコアを出す。
            word_cross_scores.append(score)
        avg_scores.append(np.mean(word_cross_scores))#20個の単語間スコアの平均値
    avg_avg_scores.append(np.mean(avg_scores))#20個の単語間スコアの平均値の平均値

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
store_cross_detail.insert(6, 'avg_cos_sim_rate', avg_avg_scores)
# 「二郎」と類似度が高いラーメン屋を高い順に表示
store_cross_detail = store_cross_detail.sort_values(['id_x', 'avg_cos_sim_rate'], ascending=[True, False])
df_sim_x = store_cross_detail[store_cross_detail['store_name_x'].str.contains('二郎')]
df_sim_x.reset_index(drop=True)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def min_max(x, axis=None):
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    result = (x-min)/(max-min)
    return result
b = df_sim_x['avg_cos_sim_rate']
c = min_max(b.values)
df_sim_x.insert(7, '正規化', c)
df_sim_x.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
similarity_scores = dataiku.Dataset("jiro_similar")
similarity_scores.write_with_schema(avg_avg_scores)