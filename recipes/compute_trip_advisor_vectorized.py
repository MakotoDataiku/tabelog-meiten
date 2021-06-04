# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
clean_trip_advisor = dataiku.Dataset("clean_trip_advisor")
clean_trip_advisor_df = clean_trip_advisor.get_dataframe()
word2vec = dataiku.Folder("m9JZdV7b")
word2vec_info = word2vec.get_info()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

trip_advisor_vectorized_df = clean_trip_advisor_df # For this sample code, simply copy input to output


# Write recipe outputs
trip_advisor_vectorized = dataiku.Dataset("trip_advisor_vectorized")
trip_advisor_vectorized.write_with_schema(trip_advisor_vectorized_df)
