from datetime import datetime
from .media_item import MediaItem


class Movie(MediaItem):

    VALID_GENRES = [
        "Acción", "Aventura", "Animación", "Comedia", "Crimen",
        "Documental", "Drama", "Fantasía", "Horror", "Musical",
        "Misterio", "Romance", "Sci-Fi", "Thriller", "Western"
    ]

    VALID_RATINGS = ["G", "PG", "PG-13", "R", "NC-17", "NR"]

    def __init__(
        self,
        title: str,
        director: str,
        year: int,
        genre: str,
        rating: str,
        score: float,
        notes: str = ""
    ):
        # Validate on construction — fail fast
        self._title = self._validate_title(title)
        self._director = self._validate_non_empty(director, "Director")
        self._year = self._validate_year(year)
        self._genre = self._validate_choice(genre, self.VALID_GENRES, "Género")
        self._rating = self._validate_choice(rating, self.VALID_RATINGS, "Clasificación")
        self._score = self._validate_score(score)
        self._notes = notes.strip()
        self._added_on = datetime.now().strftime("%Y-%m-%d")

    # ── Validators ───────────────────────────────────────────────

    @staticmethod
    def _validate_title(value: str) -> str:
        v = value.strip()
        if not v:
            raise ValueError("El título no puede estar vacío.")
        if len(v) > 120:
            raise ValueError("El título no puede superar 120 caracteres.")
        return v

    @staticmethod
    def _validate_non_empty(value: str, field: str) -> str:
        v = value.strip()
        if not v:
            raise ValueError(f"{field} no puede estar vacío.")
        return v

    @staticmethod
    def _validate_year(value) -> int:
        try:
            y = int(value)
        except (ValueError, TypeError):
            raise ValueError("El año debe ser un número entero.")
        current_year = datetime.now().year
        if not (1888 <= y <= current_year + 2):
            raise ValueError(f"El año debe estar entre 1888 y {current_year + 2}.")
        return y

    @staticmethod
    def _validate_choice(value: str, choices: list, field: str) -> str:
        if value not in choices:
            raise ValueError(f"{field} inválido. Opciones: {', '.join(choices)}")
        return value

    @staticmethod
    def _validate_score(value) -> float:
        try:
            s = float(value)
        except (ValueError, TypeError):
            raise ValueError("La puntuación debe ser un número.")
        if not (0.0 <= s <= 10.0):
            raise ValueError("La puntuación debe estar entre 0.0 y 10.0.")
        return round(s, 1)

    # ── Properties (read-only public surface) ────────────────────

    @property
    def title(self) -> str:
        return self._title

    @property
    def director(self) -> str:
        return self._director

    @property
    def year(self) -> int:
        return self._year

    @property
    def genre(self) -> str:
        return self._genre

    @property
    def rating(self) -> str:
        return self._rating

    @property
    def score(self) -> float:
        return self._score

    @property
    def notes(self) -> str:
        return self._notes

    @property
    def added_on(self) -> str:
        return self._added_on

    # Allow updates through explicit setters (validated)
    def update(self, **kwargs):
        """Update fields; each goes through the same validators."""
        if "title" in kwargs:
            self._title = self._validate_title(kwargs["title"])
        if "director" in kwargs:
            self._director = self._validate_non_empty(kwargs["director"], "Director")
        if "year" in kwargs:
            self._year = self._validate_year(kwargs["year"])
        if "genre" in kwargs:
            self._genre = self._validate_choice(kwargs["genre"], self.VALID_GENRES, "Género")
        if "rating" in kwargs:
            self._rating = self._validate_choice(kwargs["rating"], self.VALID_RATINGS, "Clasificación")
        if "score" in kwargs:
            self._score = self._validate_score(kwargs["score"])
        if "notes" in kwargs:
            self._notes = kwargs["notes"].strip()

    # ── MediaItem interface ───────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "title": self._title,
            "director": self._director,
            "year": self._year,
            "genre": self._genre,
            "rating": self._rating,
            "score": self._score,
            "notes": self._notes,
            "added_on": self._added_on,
        }

    def matches(self, query: str) -> bool:
        q = query.lower()
        return (
            q in self._title.lower()
            or q in self._director.lower()
            or q in self._genre.lower()
            or q == str(self._year)
        )

    def score_stars(self) -> str:
        filled = round(self._score / 2)
        return "★" * filled + "☆" * (5 - filled)

    def __repr__(self) -> str:
        return f"Movie({self._title!r}, {self._year}, {self._score})"
