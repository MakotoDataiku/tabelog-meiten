# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from clear_stop_words import clean_text

# Read recipe inputs
raw_ramen = dataiku.Dataset("raw_ramen")
df = raw_ramen.get_dataframe()

df["review"] = df["review"].apply(clean_text)

# Write recipe outputs
clean_ramen = dataiku.Dataset("clean_ramen")
clean_ramen.write_with_schema(df)
