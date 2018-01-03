from wsgiref import simple_server
import falcon
import json
from datetime import datetime
from dateutil import tz

from providers import get_api
from stations import GeoPoint
from stations.repository.db import StationRepository


class ConnectionsResource:
    def __init__(self) -> None:
        super().__init__()
        self.station_repo = StationRepository()

    def on_get(self, req, resp):
        """Handles GET requests"""
        dep_time = req.get_param('time') or datetime.now(tz.gettz('UTC'))
        origin_id = req.get_param('origin', required=True)
        dest_id = req.get_param('destination', required=True)

        limit = req.get_param_as_int('limit') or 10
        api = get_api(origin_id)

        resp.body = json.dumps(api.get_connections(origin_id, dest_id, dep_time, limit))


class DeparturesResource:

    def __init__(self) -> None:
        super().__init__()
        self.station_repo = StationRepository()

    def on_get(self, req, resp):
        """Handles GET requests"""
        dep_time = req.get_param('time') or datetime.now(tz.gettz('UTC'))
        station_id = req.get_param('station_id', required=True)

        limit = req.get_param_as_int('limit') or 10
        api = get_api(station_id)

        origin = self.station_repo.get(station_id)
        departures = api.get_departures(origin, dep_time)
        # add station
        departures['station'] = origin.json()
        resp.body = json.dumps(departures)


class LocationsResource:

    def __init__(self) -> None:
        super().__init__()
        self.station_repo = StationRepository()

    def on_get(self, req, resp):
        """Handles GET requests"""
        latitude = float(req.get_param('lat', required=True))
        longitude = float(req.get_param('lon', required=True))

        limit = req.get_param_as_int('limit') or 10
        stations = [s.json() for s in self.station_repo.find_nearby_stations(GeoPoint(latitude, longitude), limit)]
        resp.body = json.dumps({'stations': stations})


class StationsResource:

    def __init__(self) -> None:
        super().__init__()
        self.station_repo = StationRepository()

    def on_get(self, req, resp):
        """Handles GET requests"""
        station_id = req.get_param('id')
        query = req.get_param('query')

        limit = req.get_param_as_int('limit') or 10
        if station_id:
            try:
                stations = [self.station_repo.get(station_id).json()]
            except StationRepository.NotFoundException:
                stations = []
        else:
            stations = [s.json() for s in self.station_repo.find_stations(query, limit)]
        resp.body = json.dumps({'stations': stations})


class StationsVoiceResource:

    def __init__(self) -> None:
        super().__init__()
        self.station_repo = StationRepository()

    def on_get(self, req, resp):
        """Handles GET requests"""
        query = req.get_param('query', required=True)

        limit = req.get_param_as_int('limit') or 10
        stations = [s.json() for s in self.station_repo.find_sound_stations(query, limit)]
        resp.body = json.dumps({'stations': stations})


app = falcon.API()
app.add_route('/v1/departures', DeparturesResource())
app.add_route('/v1/locations', LocationsResource())
app.add_route('/v1/stations/voice', StationsVoiceResource())
app.add_route('/v1/stations', StationsResource())
app.add_route('/v1/connections', ConnectionsResource())

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
