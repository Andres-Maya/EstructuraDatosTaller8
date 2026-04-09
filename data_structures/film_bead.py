"""
FilmBead - Node for doubly-linked list
"""
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Movie


class FilmBead:
    """
    A single link in the FilmReel chain.
    Acts as the node of the doubly-linked list.
    Each bead holds one Movie and points to the previous and next bead.
    """

    def __init__(self, movie: "Movie"):
        self.movie: "Movie" = movie
        self.prev: Optional["FilmBead"] = None
        self.next: Optional["FilmBead"] = None

    def __repr__(self) -> str:
        return f"FilmBead({self.movie.title!r})"
