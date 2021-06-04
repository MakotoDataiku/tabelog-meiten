# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from clear_stop_words import clean_text

# Read recipe inputs
raw_ramen = dataiku.Dataset("your_trip_advisor")
df = raw_ramen.get_dataframe()

df["review"] = df["jp"].apply(clean_text)

# Write recipe outputs
clean_ramen = dataiku.Dataset("clean_trip_advisor")
clean_ramen.write_with_schema(df)
