# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
raw_ramen = dataiku.Dataset("raw_ramen")
raw_ramen_df = raw_ramen.get_dataframe()




# Write recipe outputs
word2vec = dataiku.Folder("m9JZdV7b")
word2vec_info = word2vec.get_info()
