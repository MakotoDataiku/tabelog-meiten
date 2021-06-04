# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
ramen_vocab_clustered = dataiku.Dataset("ramen_vocab_clustered")
df = ramen_vocab_clustered.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
for cluster in df['cluster_labels'].unique():
    print(cluster)
    print(df[df['cluster_labels']==cluster].words.values[:100])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
labels = {
    "cluster_0":"レビュー",
    "cluster_1":"立地・外観",
    "cluster_2":"営業形態",
    "cluster_3":"味・具材",
    #"cluster_4":"交通手段",
    #"cluster_5":"営業形態",
    #"cluster_6":"具材",
    "cluster_outliers":"その他",
}

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
client = dataiku.api_client()

project = client.get_project(dataiku.get_custom_variables()['projectKey'])
project_variables = project.get_variables()
project_variables['standard']['labels'] = labels
project_variables = project.set_variables(project_variables)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

cluster_visualized_df = ramen_vocab_clustered_df # For this sample code, simply copy input to output


# Write recipe outputs
cluster_visualized = dataiku.Dataset("cluster_visualized")
cluster_visualized.write_with_schema(cluster_visualized_df)