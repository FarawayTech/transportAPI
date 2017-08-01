from pymongo import MongoClient
import os
import editdistance
from metaphone import doublemetaphone
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

    class NotFoundException(Exception):
        pass

    def __init__(self):
        self.station_db = db['stations']

    def find_nearby_stations(self, geo_point: GeoPoint, limit: int):
        query = {'location':
                     {'$nearSphere':
                          {'$geometry':
                               {'type': 'Point',
                                'coordinates': [geo_point.longitude, geo_point.latitude]},
                           '$maxDistance': 10000}}}
        return [Station.from_dict(s) for s in self.station_db.find(query).limit(limit)]

    def find_sound_stations(self, query: str, limit: int):
        metaquery1, metaquery2 = doublemetaphone(query)
        stations1 = stations2 = []
        if metaquery1:
            stations1 = [Station.from_dict(s) for s in self.station_db.find({"$text": {"$search": metaquery1}}).limit(limit)]
        if metaquery2:
            stations2 = [Station.from_dict(s) for s in self.station_db.find({"$text": {"$search": metaquery2}}).limit(limit)]
        stations = stations1 + stations2
        # sort by edit distance
        stations.sort(key=lambda s: editdistance.eval(query, s.name))

        return stations

    def get(self, station_id: str):
        s = self.station_db.find_one({'station_id': station_id})
        if s is None:
            raise StationRepository.NotFoundException()
        return Station(s['station_id'], s['synonyms'][0], GeoPoint(s['location']['coordinates'][1],
                                                                   s['location']['coordinates'][0]))
