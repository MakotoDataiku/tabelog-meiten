# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from gensim import corpora
from gensim import models
import MeCab
from gensim.models import word2vec

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
your_trip_advisor = dataiku.Dataset("your_trip_advisor")
df = your_trip_advisor.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
folder_path = dataiku.Folder("m9JZdV7b").get_path()
model_path = folder_path + "/word2vec_ramen_model.model"
ramen_model = word2vec.Word2Vec.load(model_path)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
w2v_folder = dataiku.Folder("m9JZdV7b").get_path()
text_folder = dataiku.Folder("aLTWBozg").get_path()
wakati_folder = dataiku.Folder("0kM5kXKs").get_path()
tagger_path = '-Owakati -d ' + wakati_folder

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
tagger = MeCab.Tagger(tagger_path)#タグはMeCab.Tagger（neologd辞書）を使用
tagger.parse('')

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def tokenize_ja(text, lower):
    node = tagger.parseToNode(str(text))
    while node:
        if lower and node.feature.split(',')[0] in ["名詞","形容詞"]:#分かち書きで取得する品詞を指定
            yield node.surface.lower()
        node = node.next
def tokenize(content, token_min_len, token_max_len, lower):
    return [
        str(token) for token in tokenize_ja(content, lower)
        if token_min_len <= len(token) <= token_max_len and not token.startswith('_')
    ]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
wakati_ramen_text = []
for i in df['jp']:
    txt = tokenize(i, 2, 10000, True)
    wakati_ramen_text.append(txt)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#[w for w in sublist in wakati_ramen_text]
vocab = [w for sublist in wakati_ramen_text for w in sublist]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
words = []
vectors = []
for word in vocab:
    try:
        vector = ramen_model.wv[word]
        words.append(word)
        vectors.append(vector)
    except KeyError:
        None

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
vocab_df = pd.DataFrame(vectors)
vocab_df['words'] = words

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
trip_advisor_tf_idf = dataiku.Dataset("trip_advisor_vocabs")
trip_advisor_tf_idf.write_with_schema(vocab_df)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#ramen_dictionary_path = dataiku.Folder("POe5uF4H").get_path() + "/ramen_dictionary"
#dictionary = corpora.Dictionary.load(ramen_dictionary_path)
#corpus = list(map(dictionary.doc2bow, reviews_concat))