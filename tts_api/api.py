from abc import ABC, abstractmethod


class BaseTTSApi(ABC):
    @abstractmethod
    def get_voice_mp3(self, text: str):
        pass
