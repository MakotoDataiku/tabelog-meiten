# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from tabelog import Tabelog

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
raw_ramen = Tabelog(base_url="https://tabelog.com/tokyo/rstLst/ramen/", 
                    test_mode=False, p_ward='東京都内', 
                    begin_page=31, end_page=40) # begin_page=31, end_page=40 5/6/2021

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
raw_ramen_df = raw_ramen.df

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
raw_ramen = dataiku.Dataset("raw_ramen")
raw_ramen.write_with_schema(raw_ramen_df)