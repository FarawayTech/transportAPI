import os

import requests

from stations import GeoPoint
from . import BaseWeatherApi

APP_KEY = os.environ.get("OPEN_WEATHER_KEY")


class OpenWeatherApi(BaseWeatherApi):

    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
    DAILY_FORECAST_URL = "https://api.openweathermap.org/data/2.5/onecall"

    def get_hourly_forecast(self, location: GeoPoint):
        query = {
            "lat": location.latitude,
            "lon": location.longitude,
            "units": "metric",
            "appid": APP_KEY,
        }
        result = requests.get(self.FORECAST_URL, params=query).json()
        return result

    def get_daily_forecast(self, location: GeoPoint):
        query = {
            "lat": location.latitude,
            "lon": location.longitude,
            "units": "metric",
            "appid": APP_KEY,
            "exclude": "minutely,hourly"
        }
        result = requests.get(self.DAILY_FORECAST_URL, params=query).json()
        return result
