# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
ramen_clusters_named = dataiku.Dataset("ramen_clusters_named")
ramen_clusters_named_df = ramen_clusters_named.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

tf_IDF_scores_df = ramen_clusters_named_df # For this sample code, simply copy input to output


# Write recipe outputs
tf_IDF_scores = dataiku.Dataset("TF_IDF_scores")
tf_IDF_scores.write_with_schema(tf_IDF_scores_df)
