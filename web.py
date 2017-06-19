from wsgiref import simple_server
import falcon
import json
from datetime import datetime
from dateutil import tz

from providers import get_api


class DeparturesResource:

    def on_get(self, req, resp):
        """Handles GET requests"""
        dep_time = req.get_param('time') or datetime.now(tz.gettz('UTC'))
        station_id = req.get_param('station_id') or None
        if station_id is None:
            raise falcon.HTTPBadRequest('Station ID is none',
                                        'Please specify a valid station ID')

        limit = req.get_param_as_int('limit') or 10
        api = get_api(station_id)
        resp.body = json.dumps(api.get_departures(station_id, dep_time))


app = falcon.API()
app.add_route('/departures', DeparturesResource())

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
