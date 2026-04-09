from abc import ABC, abstractmethod


class MediaItem(ABC):

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def matches(self, query: str) -> bool:
        pass
