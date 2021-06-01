# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
reviews_TF_IDF = dataiku.Dataset("reviews_TF_IDF")
reviews_TF_IDF_df = reviews_TF_IDF.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

similarity_scores_df = reviews_TF_IDF_df # For this sample code, simply copy input to output


# Write recipe outputs
similarity_scores = dataiku.Dataset("similarity_scores")
similarity_scores.write_with_schema(similarity_scores_df)
