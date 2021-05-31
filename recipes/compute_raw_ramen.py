# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from tabelog import Tabelog

raw_ramen_df = Tabelog(base_url="https://tabelog.com/tokyo/rstLst/ramen/", test_mode=True, p_ward='東京都内')

# Write recipe outputs
raw_ramen = dataiku.Dataset("raw_ramen")
raw_ramen.write_with_schema(raw_ramen_df)
