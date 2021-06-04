# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
ramen_vocab_clustered = dataiku.Dataset("ramen_vocab_clustered")
ramen_vocab_clustered_df = ramen_vocab_clustered.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

cluster_visualized_df = ramen_vocab_clustered_df # For this sample code, simply copy input to output


# Write recipe outputs
cluster_visualized = dataiku.Dataset("cluster_visualized")
cluster_visualized.write_with_schema(cluster_visualized_df)
