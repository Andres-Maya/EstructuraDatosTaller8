from typing import Optional, List
from data_structures import FilmReel
from models import Movie


class CatalogManager:

    def __init__(self):
        self._reel = FilmReel()

    # ── CRUD ──────────────────────────────────────────────────────

    def add_movie(self, **kwargs) -> Movie:
        movie = Movie(**kwargs)
        self._reel.append(movie)
        return movie

    def delete_movie(self, title: str) -> bool:
        bead = self._reel.find_by_title(title)
        if bead:
            self._reel.remove(bead)
            return True
        return False

    def edit_movie(self, title: str, **kwargs) -> Optional[Movie]:
        bead = self._reel.find_by_title(title)
        if not bead:
            return None
        bead.movie.update(**kwargs)
        return bead.movie

    def get_movie(self, title: str) -> Optional[Movie]:
        bead = self._reel.find_by_title(title)
        return bead.movie if bead else None

    def search(self, query: str) -> List[Movie]:
        if not query.strip():
            return self.all_movies()
        return [b.movie for b in self._reel.forward() if b.movie.matches(query)]

    def all_movies(self) -> List[Movie]:
        return self._reel.to_list()

    def filter_by_genre(self, genre: str) -> List[Movie]:
        return [m for m in self._reel.to_list() if m.genre == genre]

    def filter_by_score(self, min_score: float) -> List[Movie]:
        return [m for m in self._reel.to_list() if m.score >= min_score]

    def sort(self, field: str, reverse: bool = False):
        key_map = {
            "title":    lambda m: m.title.lower(),
            "year":     lambda m: m.year,
            "score":    lambda m: m.score,
            "director": lambda m: m.director.lower(),
        }
        if field not in key_map:
            raise ValueError(f"Campo de ordenamiento inválido: {field}")
        self._reel.sort_by(key_map[field], reverse=reverse)

    def stats(self) -> dict:
        movies = self.all_movies()
        if not movies:
            return {"total": 0}
        scores = [m.score for m in movies]
        genres = {}
        for m in movies:
            genres[m.genre] = genres.get(m.genre, 0) + 1
        top_genre = max(genres, key=genres.get)
        return {
            "total":     len(movies),
            "avg_score": round(sum(scores) / len(scores), 2),
            "max_score": max(scores),
            "min_score": min(scores),
            "top_genre": top_genre,
            "genres":    genres,
        }

    def __len__(self) -> int:
        return len(self._reel)
