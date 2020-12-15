from abc import ABC, abstractmethod

from stations import GeoPoint


class BaseWeatherApi(ABC):
    @abstractmethod
    def get_hourly_forecast(self, location: GeoPoint):
        pass

    @abstractmethod
    def get_daily_forecast(self, location: GeoPoint):
        pass
