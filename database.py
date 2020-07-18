import pandas as pd
from pymongo import MongoClient
import ForkConfig as Fork


def get_all_professions():
    client = MongoClient(Fork.MONGO_HOST, Fork.MONGO_PORT, username=Fork.MONGO_USERNAME, password=Fork.MONGO_PASSWORD)
    db = client.graphs
    collection = db.node_profession
    df = pd.DataFrame(list(collection.find()))
    return df

def connect_mongo(host=Fork.MONGO_HOST, port=Fork.MONGO_PORT, username=Fork.MONGO_USERNAME,
                  password=Fork.MONGO_PASSWORD,
                  db=Fork.MONGO_JOB_DB):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]
