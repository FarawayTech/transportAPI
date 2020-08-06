from abc import ABC, abstractmethod

from stations import GeoPoint


class BaseWeatherApi(ABC):
    @abstractmethod
    def get_forecast(self, location: GeoPoint):
        pass

    @abstractmethod
    def get_uvi_forecast(self, location: GeoPoint):
        pass

    @abstractmethod
    def get_uvi(self, location: GeoPoint):
        pass
