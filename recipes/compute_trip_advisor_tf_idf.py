# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
ramen_dictionary = dataiku.Folder("POe5uF4H")
ramen_dictionary_info = ramen_dictionary.get_info()
your_trip_advisor = dataiku.Dataset("your_trip_advisor")
your_trip_advisor_df = your_trip_advisor.get_dataframe()


# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

trip_advisor_tf_idf_df = your_trip_advisor_df # For this sample code, simply copy input to output


# Write recipe outputs
trip_advisor_tf_idf = dataiku.Dataset("trip_advisor_tf_idf")
trip_advisor_tf_idf.write_with_schema(trip_advisor_tf_idf_df)
