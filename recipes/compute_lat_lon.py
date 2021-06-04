# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from get_lat_lon import get_lat_lon_from_address

# Read recipe inputs
raw_ramen = dataiku.Dataset("raw_ramen")
df = raw_ramen.get_dataframe()



# Compute recipe outputs from inputs
# TODO: Replace this part by your actual code that computes the output, as a Pandas dataframe
# NB: DSS also supports other kinds of APIs for reading and writing data. Please see doc.

lat_lon_df = raw_ramen_df # For this sample code, simply copy input to output


# Write recipe outputs
lat_lon = dataiku.Dataset("lat_lon")
lat_lon.write_with_schema(lat_lon_df)
