# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from get_lat_lon import get_lat_lon_from_address

import tqdm
import requests
from bs4 import BeautifulSoup
import time
import geocoder

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
raw_ramen = dataiku.Dataset("ramen_by_store_name")
df = raw_ramen.get_dataframe(limit=100)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df.head()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
addresses = df['address_cleaned'].tolist()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def geocoding_lat_lon(address):
    try:
        g = geocoder.mapquest(address, key='eOUDWog4FKpjWQmPZWRCzhiKr3GW0mEr')
        latitude = g.json['raw']['latLng']['lat']
        longitude = g.json['raw']['latLng']['lng']
        return latitude, longitude
    except:
        return np.nan, np.nan

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
df['latitude'], df['longitude'] = zip(*df['address_cleaned'].map(geocoding_lat_lon))

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
lat_lon = dataiku.Dataset("lat_lon")
lat_lon.write_with_schema(df)