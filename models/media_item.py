"""
Abstract base class for media items
"""
from abc import ABC, abstractmethod


class MediaItem(ABC):
    """Abstract base for any catalogueable media item."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize item to dictionary."""
        pass

    @abstractmethod
    def matches(self, query: str) -> bool:
        """Return True if item matches a search query."""
        pass
