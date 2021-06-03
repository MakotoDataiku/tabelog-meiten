# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu



# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

your_trip_advisor_df = ... # Compute a Pandas dataframe to write into your_trip_advisor


# Write recipe outputs
your_trip_advisor = dataiku.Dataset("your_trip_advisor")
your_trip_advisor.write_with_schema(your_trip_advisor_df)
