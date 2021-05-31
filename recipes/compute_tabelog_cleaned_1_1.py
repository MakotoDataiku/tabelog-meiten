# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import re
import neologdn
import emoji
from clear_stop_words import clean_text

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
tabelog = dataiku.Dataset("tabelog_w_stars")
df = tabelog.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df["review_cleaned"] = df["review"].apply(clean_text)

df.loc[df['stars']=="-", "stars"] = df['rate']

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
tabelog_cleaned = dataiku.Dataset("tabelog_w_stars_cleaned")
tabelog_cleaned.write_with_schema(df)