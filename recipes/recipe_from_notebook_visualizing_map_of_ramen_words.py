# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE_MAGIC_CELL
# Automatically replaced inline charts by "no-op" charts
# %pylab inline
import matplotlib
matplotlib.use("Agg")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd
from gensim.models import word2vec
from sklearn.manifold import TSNE
import re
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Example: load a DSS dataset as a Pandas dataframe
mydataset = dataiku.Dataset("ramen_vocab")
df = mydataset.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
folder_path = dataiku.Folder("m9JZdV7b").get_path()
model_path = folder_path + "/word2vec_ramen_model.model"
print(model_path)
ramen_model = word2vec.Word2Vec.load(model_path)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
vocabs = list(ramen_model.wv.vocab.keys())
X = ramen_model.wv[vocabs]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df = pd.DataFrame(X_tsne, index=vocabs, columns=['x', 'y'])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
"""
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.scatter(df['x'], df['y'])
for word, pos in df.iterrows():
    ax.annotate(word, pos)
plt.show()
"""

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
py_recipe_output = dataiku.Dataset("w2v_for_viz")
py_recipe_output.write_with_schema(df)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Recipe outputs
w2v_for_viz = dataiku.Dataset("w2v_for_viz")
w2v_for_viz.write_with_schema(pandas_dataframe)