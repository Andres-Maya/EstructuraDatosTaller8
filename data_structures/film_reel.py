"""
FilmReel - Doubly-linked list implementation
"""
from typing import Optional, List, Callable, TYPE_CHECKING
from .film_bead import FilmBead

if TYPE_CHECKING:
    from models import Movie


class FilmReel:
    """
    A doubly-linked chain of FilmBeads.
    Provides O(1) insertion/deletion at head and tail,
    and sequential traversal in both directions.

    Internally:
        _head  →  first bead
        _tail  →  last bead
        _size  →  number of beads (cached for O(1) len)
    """

    def __init__(self):
        self._head: Optional[FilmBead] = None
        self._tail: Optional[FilmBead] = None
        self._size: int = 0

    # ── Core mutations ────────────────────────────────────────────

    def append(self, movie: "Movie") -> FilmBead:
        """Add a movie at the tail of the reel. O(1)."""
        bead = FilmBead(movie)
        if self._tail is None:          # empty reel
            self._head = self._tail = bead
        else:
            bead.prev = self._tail
            self._tail.next = bead
            self._tail = bead
        self._size += 1
        return bead

    def prepend(self, movie: "Movie") -> FilmBead:
        """Add a movie at the head of the reel. O(1)."""
        bead = FilmBead(movie)
        if self._head is None:
            self._head = self._tail = bead
        else:
            bead.next = self._head
            self._head.prev = bead
            self._head = bead
        self._size += 1
        return bead

    def remove(self, bead: FilmBead) -> bool:
        """
        Remove a specific bead from anywhere in the reel.
        Re-links neighbours. O(1) given the bead reference.
        """
        if bead.prev:
            bead.prev.next = bead.next
        else:
            self._head = bead.next          # bead was head

        if bead.next:
            bead.next.prev = bead.prev
        else:
            self._tail = bead.prev          # bead was tail

        bead.prev = bead.next = None        # detach
        self._size -= 1
        return True

    def clear(self):
        """Remove all beads."""
        self._head = self._tail = None
        self._size = 0

    # ── Traversal ────────────────────────────────────────────────

    def forward(self):
        """Generator: iterate from head to tail."""
        current = self._head
        while current:
            yield current
            current = current.next

    def backward(self):
        """Generator: iterate from tail to head."""
        current = self._tail
        while current:
            yield current
            current = current.prev

    def find_by_title(self, title: str) -> Optional[FilmBead]:
        """Linear search by exact title (case-insensitive). O(n)."""
        for bead in self.forward():
            if bead.movie.title.lower() == title.lower():
                return bead
        return None

    def to_list(self) -> List["Movie"]:
        """Return all movies as a plain Python list."""
        return [bead.movie for bead in self.forward()]

    # ── Sorting (in-place bubble sort on the chain) ───────────────

    def sort_by(self, key_func: Callable, reverse: bool = False):
        """
        In-place bubble sort on the doubly-linked chain.
        Swaps movie payloads (not beads) for simplicity. O(n²).
        Fine for typical collection sizes (<1000 films).
        """
        if self._size < 2:
            return
        swapped = True
        while swapped:
            swapped = False
            current = self._head
            while current and current.next:
                a = key_func(current.movie)
                b = key_func(current.next.movie)
                if (a > b) if not reverse else (a < b):
                    # Swap payloads only
                    current.movie, current.next.movie = current.next.movie, current.movie
                    swapped = True
                current = current.next

    # ── Dunder helpers ────────────────────────────────────────────

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def __repr__(self) -> str:
        return f"FilmReel({self._size} beads)"
