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
clean_trip_advisor = dataiku.Dataset("clean_trip_advisor")
df = clean_trip_advisor.get_dataframe()

model_folder_path = dataiku.Folder("m9JZdV7b").get_path()
model_path = model_folder_path + "/word2vec_ramen_model.model"
ramen_model = word2vec.Word2Vec.load(model_path)

wakati_folder = dataiku.Folder("0kM5kXKs").get_path()
tagger_path = '-Owakati -d ' + wakati_folder

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df.head()

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
#コーパス作成
wakati_ramen_text = []
for i in df['review']:
    txt = tokenize(i, 2, 10000, True)
    wakati_ramen_text.append(txt)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
vocab = list(set([item for sublist in wakati_ramen_text for item in sublist]))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
len(vocab)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# max_vocab = 30000 #40000にしても結果は同じだった
# vocab = list(word2vec_ramen_model.wv.vocab.keys())[:max_vocab]
# vectors = [ramen_model.wv[word] for word in vocab]
vectors = []
vocabs = []
for word in vocab:
    try:
        vector = ramen_model.wv[word]
        vectors.append(vector)
        vocabs.append(word)
    except:
        None

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
len(vectors)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
vocab_df = pd.DataFrame(vectors)
vocab_df['words'] = vocabs

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
trip_advisor_vectorized = dataiku.Dataset("trip_advisor_vectorized")
trip_advisor_vectorized.write_with_schema(vocab_df)