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

    def __init__(self, station_id, name, geo_point: GeoPoint):
        self.station_id = station_id
        self.name = name
        self.geo_point = geo_point

    def json(self):
        return {"id": self.station_id,
                "name": self.name,
                "coordinates": {
                    "latitude": self.geo_point.latitude,
                    "longitude": self.geo_point.longitude
                }}
