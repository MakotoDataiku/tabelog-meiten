# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import pickle
from gensim.models import word2vec
import MeCab

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
#raw_ramen = dataiku.Dataset("raw_ramen")
#df = raw_ramen.get_dataframe()
#df_ramen = df.groupby(['store_name','score','review_cnt'])['review'].apply(list).apply(' '.join).reset_index().sort_values('score', ascending=False)

df_ramen = dataiku.Dataset("ramen_by_store_name").get_dataframe().drop(["store_id", "address", "ward"], axis=1)

w2v_folder = dataiku.Folder("m9JZdV7b").get_path()
text_folder = dataiku.Folder("aLTWBozg").get_path()
wakati_folder = dataiku.Folder("0kM5kXKs").get_path()
tagger_path = '-Owakati -d ' + wakati_folder
tagger_path

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df_ramen.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
tagger = MeCab.Tagger(tagger_path)
tagger.parse('')

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def tokenize_ja(text, lower):
    node = tagger.parseToNode(str(text))
    while node:
        if lower and node.feature.split(',')[0] in ["名詞","形容詞"]:
            yield node.surface.lower()
        node = node.next
def tokenize(content, token_min_len, token_max_len, lower):
    return [
        str(token) for token in tokenize_ja(content, lower)
        if token_min_len <= len(token) <= token_max_len and not token.startswith('_')
    ]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
wakati_ramen_text = []
for i in df_ramen['review']:
    txt = tokenize(i, 2, 10000, True)
    wakati_ramen_text.append(txt)
np.savetxt(text_folder + "/ramen_corpus.txt", wakati_ramen_text, fmt = '%s', delimiter = ',')

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
word2vec_ramen_model = word2vec.Word2Vec(wakati_ramen_text, sg = 1, size = 300, window = 5, min_count = 5, iter = 100, workers = 3)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
word2vec_ramen_model.save(w2v_folder+"/word2vec_ramen_model.model")

max_vocab = 30000
vocab = list(word2vec_ramen_model.wv.vocab.keys())[:max_vocab]
vectors = [word2vec_ramen_model.wv[word] for word in vocab]

vocab_df = pd.DataFrame(vectors)
vocab_df['words'] = vocab

py_recipe_output = dataiku.Dataset("ramen_vocab")
py_recipe_output.write_with_schema(vocab_df)