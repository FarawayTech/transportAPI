from abc import ABC, abstractmethod


class Api(ABC):
    @abstractmethod
    def get_departures(self, station_id: str, time):
        pass

    @abstractmethod
    def get_connections(self, origin: str, destination: str, time, limit: int):
        pass
