import pandas as pd
import pymongo

client = pymongo.MongoClient('localhost', 27017, username='forkMVP7', password='future0fWork')
db = client["testdb"]  # makes a test database called "test"
collection = db["testcoll"]  # makes a collection called "test" in the "test" db
collection.insert_one({"foo": "bar"})  # add a document

