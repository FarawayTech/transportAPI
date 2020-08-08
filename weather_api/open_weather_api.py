import os

import requests

from stations import GeoPoint
from . import BaseWeatherApi

APP_KEY = os.environ.get("OPEN_WEATHER_KEY")


class OpenWeatherApi(BaseWeatherApi):

    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

    def get_forecast(self, location: GeoPoint):
        query = {
            "lat": location.latitude,
            "lon": location.longitude,
            "units": "metric",
            "appid": APP_KEY,
        }
        result = requests.get(self.FORECAST_URL, params=query).json()
        return result
