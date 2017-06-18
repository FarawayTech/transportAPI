import os

from pymongo import MongoClient

client = MongoClient()
db = client['transport']

stations_db = db['stations']

# read properties
_MONGO_URI = os.environ.get('MONGO_URI')

if _MONGO_URI:
    client_remote = MongoClient(_MONGO_URI)
    db = client_remote[_MONGO_URI.split('/')[-1]]
    stations_db = db['stations']
