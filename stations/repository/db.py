from pymongo import MongoClient
import os
from . import MONGO_URI_ENV
from .. import GeoPoint, Station

MONGO_URI = os.environ.get(MONGO_URI_ENV)
if MONGO_URI is not None:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_URI.split('/')[-1]]
else:
    client = MongoClient()
    db = client['test']


class StationRepository:
    station_db = None

    def __init__(self):
        self.station_db = db['stations']

    def find_nearby_stations(self, geo_point: GeoPoint, limit: int):
        query = {'location':
                     {'$nearSphere':
                          {'$geometry':
                               {'type': 'Point',
                                'coordinates': [geo_point.longitude, geo_point.latitude]},
                           '$maxDistance': 10000}}}
        return [Station(s['station_id'], s['synonyms'][0], GeoPoint(s['location']['coordinates'][1],
                                                                    s['location']['coordinates'][0]))
                for s in self.station_db.find(query).limit(limit)]
