"""Create chart data for web app"""
import pymongo
from pymongo import MongoClient
import pandas as pd
import graphlab as gl


mcl = MongoClient()
mdb = mcl['events']
events_in = mdb['incoming']


def get_predictions():
    """Return all predictions from the database"""
    mongo_query = {'_pred': {'$exists': 1} }
    mongo_cursor = events_in.find(mongo_query)

    df = pd.DataFrame(columns=['_id',
                               'generation_time',
                               'prediction',
                               'probability',
                               ])
    for item in mongo_cursor:
        df.loc[df.index.max()+1] = [
            item['_id'],
            item['_id'].generation_time.strftime('%Y-%m-%d %H:%M'),
            item['_pred'],
            item['_prob']
        ]
