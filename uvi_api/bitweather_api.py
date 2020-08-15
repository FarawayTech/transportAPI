import os

import requests

from stations import GeoPoint
from . import BaseUVIApi

API_KEY = os.environ.get("BITWEATHER_API_KEY")


class OpenUVApi(BaseUVIApi):

    UVI_FORECAST_URL = "https://api.weatherbit.io/v2.0/forecast/daily"
    UVI_URL = "https://api.weatherbit.io/v2.0/current"

    def get_uvi_forecast(self, location: GeoPoint):
        query = {"lat": location.latitude, "lon": location.longitude, "key": API_KEY}
        result = requests.get(self.UVI_FORECAST_URL, params=query).json()
        return result

    def get_uvi(self, location: GeoPoint):
        query = {"lat": location.latitude, "lon": location.longitude, "key": API_KEY}
        result = requests.get(self.UVI_URL, params=query).json()
        return self._current_uvi_to_default(result)

    @staticmethod
    def _current_uvi_to_default(result: dict):
        data = result["data"][0]
        return {
            "uv": data["uv"],
            "uv_time": data["ob_time"],
            "sun_info": {
                "sun_times": {"sunset": data["sunset"], "sunrise": data["sunrise"]}
            },
        }
