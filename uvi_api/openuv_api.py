import os

import requests

from stations import GeoPoint
from . import BaseUVIApi

API_KEY = os.environ.get("OPENUV_API_KEY")


class OpenUVApi(BaseUVIApi):

    UVI_FORECAST_URL = "https://api.openuv.io/api/v1/forecast"
    UVI_URL = "https://api.openuv.io/api/v1/uv"

    def get_uvi_forecast(self, location: GeoPoint):
        headers = {'x-access-token': 'OPENUV_API_KEY'}
        query = {'lat': location.latitude, 'lng': location.longitude}
        result = requests.get(self.UVI_FORECAST_URL, params=query, headers=headers).json()
        return result

    def get_uvi(self, location: GeoPoint):
        headers = {'x-access-token': 'OPENUV_API_KEY'}
        query = {'lat': location.latitude, 'lng': location.longitude}
        result = requests.get(self.UVI_URL, params=query, headers=headers).json()
        return result
