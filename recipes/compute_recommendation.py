# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
word2vec = dataiku.Folder("m9JZdV7b")
word2vec_info = word2vec.get_info()
reviews_TF_IDF = dataiku.Dataset("reviews_TF_IDF")
reviews_TF_IDF_df = reviews_TF_IDF.get_dataframe()
tripAdvisor_top_TFIDF_words = dataiku.Folder("FXMfF0DU")
tripAdvisor_top_TFIDF_words_info = tripAdvisor_top_TFIDF_words.get_info()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

recommendation_df = reviews_TF_IDF_df # For this sample code, simply copy input to output


# Write recipe outputs
recommendation = dataiku.Dataset("recommendation")
recommendation.write_with_schema(recommendation_df)
