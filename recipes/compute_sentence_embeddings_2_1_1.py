# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import scipy.spatial

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Example: load a DSS dataset as a Pandas dataframe
mydataset = dataiku.Dataset("tabelog_w_stars_cleaned_prepared")
df = mydataset.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
folder = dataiku.Folder("CwbeZ55S")
model_path = folder.get_path()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# model_path = "/content/training_bert_japanese"
model = SentenceTransformer(model_path, show_progress_bar=True)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
sentences = df['review']

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
sentence_vectors = model.encode(sentences)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
len(sentence_vectors[0])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df['embedded_vector'] = sentence_vectors

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
py_recipe_output = dataiku.Dataset("tabelog_w_stars_embedded")
py_recipe_output.write_with_schema(df)