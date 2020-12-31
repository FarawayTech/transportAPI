import os
from typing import Dict

import requests

from stations import GeoPoint
from . import BaseWeatherApi

APP_KEY = os.environ.get("OPEN_WEATHER_KEY")


class OpenWeatherApi(BaseWeatherApi):

    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
    DAILY_FORECAST_URL = "https://api.openweathermap.org/data/2.5/onecall"

    @staticmethod
    def _get_ui_config(forecast_dict: Dict) -> Dict:
        main_type = ""
        intensity = 1
        weather_codes = set(str(w["id"]) for w in forecast_dict["weather"])
        main_codes = set(c[0] for c in weather_codes)
        if weather_codes.intersection({"615", "616"}):
            main_type = "mix-rain-snow"
        elif weather_codes.intersection({"611", "612", "613"}):
            main_type = "sleet"
        elif "2" in main_codes:
            if "212" in weather_codes:
                main_type = "severe"
                intensity = 1.25
            else:
                main_type = "thunder"
        elif "5" in main_codes:
            main_type = "rain"
            if weather_codes.intersection({"500", "520"}):
                intensity = 0.3
            if weather_codes.intersection({"501", "521"}):
                intensity = 0.5
            if weather_codes.intersection({"502", "522"}):
                intensity = 1
            if weather_codes.intersection({"511"}):
                intensity = 1
            if weather_codes.intersection({"503", "504", "531"}):
                intensity = 2
        elif "6" in main_codes:
            main_type = "snow"
            if weather_codes.intersection({"600", "620"}):
                intensity = 0.5
            if weather_codes.intersection({"601", "621"}):
                intensity = 1
            if weather_codes.intersection({"602", "622"}):
                intensity = 1.75
        elif weather_codes.intersection({"721", "731", "741", "751", "761"}):
            main_type = "haze"
            intensity = 0.5
        elif "711" in weather_codes:
            main_type = "smoke"
            intensity = 0.5
        elif "781" in weather_codes:
            main_type = "severe"
        elif "801" in weather_codes:
            main_type = "cloud"
            intensity = 0.1
        elif "802" in weather_codes:
            main_type = "cloud"
            intensity = 0.3
        elif "803" in weather_codes:
            main_type = "cloud"
            intensity = 0.5
        elif "804" in weather_codes:
            main_type = "cloud"
            intensity = 1
        elif "800" in weather_codes:
            main_type = "sun"
            intensity = 1

        classes = []

        # get name
        name = ", ".join(sorted(set(w["description"].title() for w in forecast_dict["weather"])))

        return {"type": main_type, "classes": classes, "intensity": intensity, "name": name}

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
        for d in result["daily"]:
            d["ui_params"] = OpenWeatherApi._get_ui_config(d)
        result["current"]["ui_params"] = OpenWeatherApi._get_ui_config(result["current"])
        return result
