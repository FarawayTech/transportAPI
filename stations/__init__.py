from typing import Dict


class GeoPoint:
    latitude = None
    longitude = None

    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude


class Station:

    station_id = None
    name = None
    geo_point = None

    def __init__(self, station_id: str, name: str, geo_point: GeoPoint):
        self.station_id = station_id
        self.name = name
        self.geo_point = geo_point

    @staticmethod
    def from_dict(s: Dict):
        return Station(s['stop_id'], s['synonyms'][0], GeoPoint(s['location']['coordinates'][1],
                                                                s['location']['coordinates'][0]))

    def json(self):
        return {"id": self.station_id,
                "name": self.name,
                "coordinates": {
                    "latitude": self.geo_point.latitude,
                    "longitude": self.geo_point.longitude
                }}
