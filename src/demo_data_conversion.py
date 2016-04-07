import clean_data_code
import pymongo
from pymongo import MongoClient
import pandas as pd
import graphlab as gl


mcl = MongoClient()
mdb = mcl['events']
events_in = mdb['incoming']
json_input = events_in.find_one()
df = clean_data_code.mongo_to_df(json_input)
abt = clean_data_code.transform_df(df)
model = gl.load_model('../models/btc_priceless_v1.gl')
sf = gl.SFrame(abt)
pred = model.predict(sf)
prob = model.predict(sf, output_type='probability')
