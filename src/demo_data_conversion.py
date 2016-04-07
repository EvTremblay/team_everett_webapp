import clean_data_code
import pymongo
from pymongo import MongoClient
import pandas as pd

mcl = MongoClient()
mdb = mcl['events']
events_in = mdb['incoming']
json_input = events_in.find_one()
df = clean_data_code.mongo_to_df(json_input)
abt = clean_data_code.transform_df(df)

print abt.info(type)
