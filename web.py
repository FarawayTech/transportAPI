from wsgiref import simple_server
import falcon
import json
from datetime import datetime
from dateutil import tz

from providers import get_api
from stations import GeoPoint
from stations.repository.db import StationRepository


class DeparturesResource:

    def on_get(self, req, resp):
        """Handles GET requests"""
        dep_time = req.get_param('time') or datetime.now(tz.gettz('UTC'))
        station_id = req.get_param('station_id', required=True)

        limit = req.get_param_as_int('limit') or 10
        api = get_api(station_id)
        resp.body = json.dumps(api.get_departures(station_id, dep_time))


class LocationsResource:

    def __init__(self) -> None:
        super().__init__()
        self.station_repo = StationRepository()

    def on_get(self, req, resp):
        """Handles GET requests"""
        latitude = float(req.get_param('lat', required=True))
        longitude = float(req.get_param('lon', required=True))

        limit = req.get_param_as_int('limit') or 10
        resp.body = json.dumps([s.json() for s in self.station_repo.find_nearby_stations(GeoPoint(latitude, longitude),
                                                                                         limit)])


app = falcon.API()
app.add_route('/v1/departures', DeparturesResource())
app.add_route('/v1/locations', LocationsResource())

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
