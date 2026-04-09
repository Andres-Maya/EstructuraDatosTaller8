"""
╔══════════════════════════════════════════════════════════════════╗
║              CineVault — Personal Film Collection Manager        ║
║                                                                  ║
║  Architecture:                                                   ║
║    • FilmBead       → Doubly-linked list node                    ║
║    • FilmReel       → Doubly-linked list collection              ║
║    • Movie          → Domain entity (encapsulated)               ║
║    • CatalogManager → Business logic layer (CRUD + search)       ║
║    • CineVaultApp   → Tkinter GUI presentation layer             ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List, Callable


# ─────────────────────────────────────────────────────────────────
#  DOMAIN LAYER
# ─────────────────────────────────────────────────────────────────

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


class Movie(MediaItem):
    """
    Represents a single movie entry in the collection.
    All attributes are private; accessed via properties (encapsulation).
    """

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
        """Return a star string representation of the score."""
        filled = round(self._score / 2)
        return "★" * filled + "☆" * (5 - filled)

    def __repr__(self) -> str:
        return f"Movie({self._title!r}, {self._year}, {self._score})"


# ─────────────────────────────────────────────────────────────────
#  DATA STRUCTURE LAYER  —  Doubly-Linked List (no "Node" / "DoublyLinkedList")
# ─────────────────────────────────────────────────────────────────

class FilmBead:
    """
    A single link in the FilmReel chain.
    Acts as the node of the doubly-linked list.
    Each bead holds one Movie and points to the previous and next bead.
    """

    def __init__(self, movie: Movie):
        self.movie: Movie = movie
        self.prev: Optional["FilmBead"] = None
        self.next: Optional["FilmBead"] = None

    def __repr__(self) -> str:
        return f"FilmBead({self.movie.title!r})"


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

    def append(self, movie: Movie) -> FilmBead:
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

    def prepend(self, movie: Movie) -> FilmBead:
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

    def to_list(self) -> List[Movie]:
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


# ─────────────────────────────────────────────────────────────────
#  BUSINESS LOGIC LAYER
# ─────────────────────────────────────────────────────────────────

class CatalogManager:
    """
    Manages all CRUD operations and queries over the FilmReel.
    This layer is completely independent of the UI.
    """

    def __init__(self):
        self._reel = FilmReel()

    # ── CRUD ──────────────────────────────────────────────────────

    def add_movie(self, **kwargs) -> Movie:
        """Create a Movie and append it to the reel."""
        movie = Movie(**kwargs)
        self._reel.append(movie)
        return movie

    def delete_movie(self, title: str) -> bool:
        """Remove a movie by title. Returns True if found and deleted."""
        bead = self._reel.find_by_title(title)
        if bead:
            self._reel.remove(bead)
            return True
        return False

    def edit_movie(self, title: str, **kwargs) -> Optional[Movie]:
        """Update fields of an existing movie."""
        bead = self._reel.find_by_title(title)
        if not bead:
            return None
        bead.movie.update(**kwargs)
        return bead.movie

    def get_movie(self, title: str) -> Optional[Movie]:
        bead = self._reel.find_by_title(title)
        return bead.movie if bead else None

    # ── Queries ───────────────────────────────────────────────────

    def search(self, query: str) -> List[Movie]:
        """Return all movies matching the query string."""
        if not query.strip():
            return self.all_movies()
        return [b.movie for b in self._reel.forward() if b.movie.matches(query)]

    def all_movies(self) -> List[Movie]:
        return self._reel.to_list()

    def filter_by_genre(self, genre: str) -> List[Movie]:
        return [m for m in self._reel.to_list() if m.genre == genre]

    def filter_by_score(self, min_score: float) -> List[Movie]:
        return [m for m in self._reel.to_list() if m.score >= min_score]

    # ── Sorting (delegates to FilmReel) ──────────────────────────

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

    # ── Statistics ────────────────────────────────────────────────

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


# ─────────────────────────────────────────────────────────────────
#  PRESENTATION LAYER  —  Tkinter GUI
# ─────────────────────────────────────────────────────────────────

# Color palette — dark cinematic theme
PALETTE = {
    "bg":        "#0D0D0D",
    "surface":   "#1A1A1A",
    "surface2":  "#242424",
    "accent":    "#E8C547",    # golden yellow
    "accent2":   "#C49A22",
    "text":      "#F0EFE6",
    "text_dim":  "#888880",
    "danger":    "#E05252",
    "success":   "#5ABF6B",
    "border":    "#333333",
    "row_even":  "#1E1E1E",
    "row_odd":   "#232323",
}


class FormDialog(tk.Toplevel):
    """
    Reusable modal dialog for adding / editing a movie.
    Receives pre-filled data (edit mode) or empty fields (add mode).
    Returns result via self.result dict; None if cancelled.
    """

    def __init__(self, parent, title: str, prefill: dict = None):
        super().__init__(parent)
        self.title(title)
        self.result: Optional[dict] = None
        self._prefill = prefill or {}
        self.resizable(False, False)
        self.configure(bg=PALETTE["bg"])
        self.grab_set()             # make modal

        self._build_ui()
        self._center(parent)
        self.wait_window()

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width() // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{pw - w//2}+{ph - h//2}")

    def _build_ui(self):
        """Build the form layout inside the dialog."""
        pad = {"padx": 18, "pady": 6}

        # Title bar
        header = tk.Frame(self, bg=PALETTE["accent"], height=4)
        header.pack(fill="x")

        body = tk.Frame(self, bg=PALETTE["bg"], padx=30, pady=20)
        body.pack(fill="both", expand=True)

        def label(text):
            return tk.Label(
                body, text=text, bg=PALETTE["bg"],
                fg=PALETTE["text_dim"], font=("Georgia", 9),
                anchor="w"
            )

        def entry_widget(var, width=34):
            return tk.Entry(
                body, textvariable=var, width=width,
                bg=PALETTE["surface2"], fg=PALETTE["text"],
                insertbackground=PALETTE["accent"],
                relief="flat", font=("Courier New", 11),
                highlightthickness=1,
                highlightbackground=PALETTE["border"],
                highlightcolor=PALETTE["accent"],
            )

        # ── Fields ───────────────────────────────────────────────
        self._vars = {}
        fields = [
            ("Título",          "title",    "str"),
            ("Director",        "director", "str"),
            ("Año",             "year",     "str"),
            ("Puntuación (0-10)","score",   "str"),
            ("Notas",           "notes",    "str"),
        ]

        for display, key, _ in fields:
            label(display).pack(fill="x", pady=(8, 0))
            var = tk.StringVar(value=self._prefill.get(key, ""))
            self._vars[key] = var
            entry_widget(var).pack(fill="x", pady=(2, 0))

        # ── Genre combobox ────────────────────────────────────────
        label("Género").pack(fill="x", pady=(8, 0))
        self._vars["genre"] = tk.StringVar(
            value=self._prefill.get("genre", Movie.VALID_GENRES[0])
        )
        genre_cb = ttk.Combobox(
            body, textvariable=self._vars["genre"],
            values=Movie.VALID_GENRES, state="readonly", width=32
        )
        genre_cb.pack(fill="x", pady=(2, 0))

        # ── Rating combobox ───────────────────────────────────────
        label("Clasificación").pack(fill="x", pady=(8, 0))
        self._vars["rating"] = tk.StringVar(
            value=self._prefill.get("rating", Movie.VALID_RATINGS[0])
        )
        rating_cb = ttk.Combobox(
            body, textvariable=self._vars["rating"],
            values=Movie.VALID_RATINGS, state="readonly", width=32
        )
        rating_cb.pack(fill="x", pady=(2, 0))

        # ── Buttons ───────────────────────────────────────────────
        btn_frame = tk.Frame(body, bg=PALETTE["bg"])
        btn_frame.pack(fill="x", pady=(20, 0))

        tk.Button(
            btn_frame, text="✓  Guardar",
            command=self._on_save,
            bg=PALETTE["accent"], fg="#000000",
            font=("Georgia", 10, "bold"),
            relief="flat", cursor="hand2", padx=16, pady=8
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        tk.Button(
            btn_frame, text="✕  Cancelar",
            command=self.destroy,
            bg=PALETTE["surface2"], fg=PALETTE["text_dim"],
            font=("Georgia", 10),
            relief="flat", cursor="hand2", padx=16, pady=8
        ).pack(side="left", expand=True, fill="x")

    def _on_save(self):
        self.result = {k: v.get() for k, v in self._vars.items()}
        self.destroy()


class StatsPanel(tk.Toplevel):
    """Floating panel that shows collection statistics."""

    def __init__(self, parent, stats: dict):
        super().__init__(parent)
        self.title("Estadísticas de la Colección")
        self.configure(bg=PALETTE["bg"])
        self.resizable(False, False)
        self.grab_set()
        self._build(stats)
        self._center(parent)

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width() // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{pw - w//2}+{ph - h//2}")

    def _build(self, s: dict):
        tk.Frame(self, bg=PALETTE["accent"], height=4).pack(fill="x")
        body = tk.Frame(self, bg=PALETTE["bg"], padx=36, pady=24)
        body.pack()

        tk.Label(
            body, text="📊  Estadísticas",
            bg=PALETTE["bg"], fg=PALETTE["accent"],
            font=("Georgia", 16, "bold")
        ).pack(pady=(0, 16))

        if s.get("total", 0) == 0:
            tk.Label(
                body, text="No hay películas en la colección.",
                bg=PALETTE["bg"], fg=PALETTE["text_dim"],
                font=("Georgia", 11)
            ).pack()
        else:
            rows = [
                ("Total de películas",   str(s["total"])),
                ("Puntuación promedio",  str(s["avg_score"])),
                ("Puntuación máxima",    str(s["max_score"])),
                ("Puntuación mínima",    str(s["min_score"])),
                ("Género más frecuente", s["top_genre"]),
            ]
            for label_text, value in rows:
                row = tk.Frame(body, bg=PALETTE["surface"], pady=6, padx=12)
                row.pack(fill="x", pady=3)
                tk.Label(
                    row, text=label_text,
                    bg=PALETTE["surface"], fg=PALETTE["text_dim"],
                    font=("Georgia", 10), anchor="w", width=22
                ).pack(side="left")
                tk.Label(
                    row, text=value,
                    bg=PALETTE["surface"], fg=PALETTE["accent"],
                    font=("Courier New", 11, "bold"), anchor="e"
                ).pack(side="right", padx=8)

            # Genre bar chart (text-based)
            tk.Label(
                body, text="Distribución por Género",
                bg=PALETTE["bg"], fg=PALETTE["text_dim"],
                font=("Georgia", 10, "italic")
            ).pack(pady=(16, 4))

            for genre, count in sorted(s["genres"].items(), key=lambda x: -x[1]):
                bar_len = int((count / s["total"]) * 20)
                bar = "█" * bar_len + "░" * (20 - bar_len)
                row = tk.Frame(body, bg=PALETTE["bg"])
                row.pack(fill="x", pady=1)
                tk.Label(
                    row, text=f"{genre:<14}",
                    bg=PALETTE["bg"], fg=PALETTE["text_dim"],
                    font=("Courier New", 9), width=14, anchor="w"
                ).pack(side="left")
                tk.Label(
                    row, text=bar,
                    bg=PALETTE["bg"], fg=PALETTE["accent"],
                    font=("Courier New", 9)
                ).pack(side="left")
                tk.Label(
                    row, text=f" {count}",
                    bg=PALETTE["bg"], fg=PALETTE["text"],
                    font=("Courier New", 9)
                ).pack(side="left")

        tk.Button(
            body, text="Cerrar",
            command=self.destroy,
            bg=PALETTE["surface2"], fg=PALETTE["text_dim"],
            font=("Georgia", 10), relief="flat",
            cursor="hand2", padx=20, pady=6
        ).pack(pady=(20, 0))


class CineVaultApp:
    """
    Main Tkinter application — presentation layer only.
    All data operations are delegated to CatalogManager.
    """

    def __init__(self, root: tk.Tk):
        self._root = root
        self._manager = CatalogManager()
        self._search_var = tk.StringVar()
        self._sort_field = tk.StringVar(value="title")
        self._sort_reverse = tk.BooleanVar(value=False)

        self._setup_root()
        self._apply_styles()
        self._build_ui()
        self._load_demo_data()
        self._refresh_table()

    # ── Root window ───────────────────────────────────────────────

    def _setup_root(self):
        self._root.title("CineVault — Mi Colección de Películas")
        self._root.configure(bg=PALETTE["bg"])
        self._root.geometry("1060x680")
        self._root.minsize(860, 560)

    def _apply_styles(self):
        """Configure ttk widget styles for the dark theme."""
        style = ttk.Style()
        style.theme_use("clam")

        # Treeview (main table)
        style.configure(
            "Vault.Treeview",
            background=PALETTE["surface"],
            foreground=PALETTE["text"],
            fieldbackground=PALETTE["surface"],
            rowheight=30,
            font=("Courier New", 10),
            borderwidth=0,
        )
        style.configure(
            "Vault.Treeview.Heading",
            background=PALETTE["surface2"],
            foreground=PALETTE["accent"],
            font=("Georgia", 10, "bold"),
            borderwidth=0,
            relief="flat",
        )
        style.map(
            "Vault.Treeview",
            background=[("selected", PALETTE["accent2"])],
            foreground=[("selected", "#000000")],
        )

        # Comboboxes
        style.configure(
            "TCombobox",
            fieldbackground=PALETTE["surface2"],
            background=PALETTE["surface2"],
            foreground=PALETTE["text"],
            selectbackground=PALETTE["accent"],
            selectforeground="#000000",
        )

        # Scrollbar
        style.configure(
            "Vault.Vertical.TScrollbar",
            background=PALETTE["surface2"],
            troughcolor=PALETTE["bg"],
            arrowcolor=PALETTE["text_dim"],
        )

    # ── UI Construction ───────────────────────────────────────────

    def _build_ui(self):
        """Assemble all UI sections."""
        self._build_header()
        self._build_toolbar()
        self._build_table()
        self._build_statusbar()

    def _build_header(self):
        header = tk.Frame(self._root, bg=PALETTE["bg"], pady=0)
        header.pack(fill="x")

        # Golden top stripe
        tk.Frame(header, bg=PALETTE["accent"], height=3).pack(fill="x")

        inner = tk.Frame(header, bg=PALETTE["bg"], padx=24, pady=12)
        inner.pack(fill="x")

        tk.Label(
            inner,
            text="🎬  CineVault",
            bg=PALETTE["bg"], fg=PALETTE["accent"],
            font=("Georgia", 22, "bold")
        ).pack(side="left")

        tk.Label(
            inner,
            text="Mi Colección Personal de Cine",
            bg=PALETTE["bg"], fg=PALETTE["text_dim"],
            font=("Georgia", 11, "italic")
        ).pack(side="left", padx=(12, 0), pady=(6, 0))

    def _build_toolbar(self):
        bar = tk.Frame(self._root, bg=PALETTE["surface"], padx=16, pady=10)
        bar.pack(fill="x")

        # ── Action buttons ────────────────────────────────────────
        def btn(parent, text, cmd, color=PALETTE["surface2"], fg=PALETTE["text"]):
            return tk.Button(
                parent, text=text, command=cmd,
                bg=color, fg=fg,
                font=("Georgia", 10), relief="flat",
                cursor="hand2", padx=12, pady=6,
                activebackground=PALETTE["accent"],
                activeforeground="#000000",
            )

        btn(bar, "＋  Agregar",  self._on_add,
            PALETTE["accent"], "#000000").pack(side="left", padx=(0, 6))
        btn(bar, "✎  Editar",   self._on_edit).pack(side="left", padx=3)
        btn(bar, "✕  Eliminar", self._on_delete,
            PALETTE["surface2"], PALETTE["danger"]).pack(side="left", padx=3)
        btn(bar, "📊  Stats",   self._on_stats).pack(side="left", padx=3)

        # ── Sort controls ─────────────────────────────────────────
        tk.Label(
            bar, text="Ordenar:",
            bg=PALETTE["surface"], fg=PALETTE["text_dim"],
            font=("Georgia", 9)
        ).pack(side="left", padx=(20, 4))

        sort_opts = [("Título", "title"), ("Año", "year"),
                     ("Puntuación", "score"), ("Director", "director")]
        for label, field in sort_opts:
            rb = tk.Radiobutton(
                bar, text=label, value=field,
                variable=self._sort_field,
                command=self._refresh_table,
                bg=PALETTE["surface"], fg=PALETTE["text_dim"],
                selectcolor=PALETTE["surface2"],
                activebackground=PALETTE["surface"],
                font=("Georgia", 9),
            )
            rb.pack(side="left", padx=2)

        tk.Checkbutton(
            bar, text="↓ Desc",
            variable=self._sort_reverse,
            command=self._refresh_table,
            bg=PALETTE["surface"], fg=PALETTE["text_dim"],
            selectcolor=PALETTE["surface2"],
            activebackground=PALETTE["surface"],
            font=("Georgia", 9),
        ).pack(side="left", padx=(4, 0))

        # ── Search box ────────────────────────────────────────────
        search_frame = tk.Frame(bar, bg=PALETTE["surface"])
        search_frame.pack(side="right")

        tk.Label(
            search_frame, text="🔍",
            bg=PALETTE["surface"], fg=PALETTE["text_dim"],
            font=("Georgia", 12)
        ).pack(side="left", padx=(0, 4))

        search_entry = tk.Entry(
            search_frame, textvariable=self._search_var,
            width=22, bg=PALETTE["surface2"], fg=PALETTE["text"],
            insertbackground=PALETTE["accent"],
            relief="flat", font=("Courier New", 11),
            highlightthickness=1,
            highlightbackground=PALETTE["border"],
            highlightcolor=PALETTE["accent"],
        )
        search_entry.pack(side="left")
        self._search_var.trace_add("write", lambda *_: self._refresh_table())

    def _build_table(self):
        """Build the main Treeview table with scrollbar."""
        frame = tk.Frame(self._root, bg=PALETTE["bg"], padx=16, pady=8)
        frame.pack(fill="both", expand=True)

        columns = ("title", "director", "year", "genre", "rating", "score", "stars", "added")
        self._tree = ttk.Treeview(
            frame, columns=columns, show="headings",
            style="Vault.Treeview", selectmode="browse"
        )

        headers = {
            "title":    ("Título",           260),
            "director": ("Director",         160),
            "year":     ("Año",               55),
            "genre":    ("Género",           100),
            "rating":   ("Clasif.",           60),
            "score":    ("Punt.",             55),
            "stars":    ("Estrellas",        100),
            "added":    ("Agregada",          90),
        }
        for col, (heading, width) in headers.items():
            self._tree.heading(col, text=heading,
                               command=lambda c=col: self._on_column_sort(c))
            self._tree.column(col, width=width, minwidth=40, anchor="center"
                              if col not in ("title", "director") else "w")

        # Alternating row colors
        self._tree.tag_configure("even", background=PALETTE["row_even"])
        self._tree.tag_configure("odd",  background=PALETTE["row_odd"])

        scrollbar = ttk.Scrollbar(
            frame, orient="vertical",
            command=self._tree.yview,
            style="Vault.Vertical.TScrollbar"
        )
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Double-click to edit
        self._tree.bind("<Double-1>", lambda _: self._on_edit())

    def _build_statusbar(self):
        bar = tk.Frame(self._root, bg=PALETTE["surface2"], pady=4)
        bar.pack(fill="x", side="bottom")
        tk.Frame(bar, bg=PALETTE["accent"], height=2).pack(fill="x", side="top")
        self._status_var = tk.StringVar(value="Listo.")
        tk.Label(
            bar, textvariable=self._status_var,
            bg=PALETTE["surface2"], fg=PALETTE["text_dim"],
            font=("Georgia", 9), padx=16
        ).pack(side="left")

    # ── Table population ──────────────────────────────────────────

    def _refresh_table(self):
        """Re-populate table from manager (with current sort & filter)."""
        query = self._search_var.get()
        self._manager.sort(self._sort_field.get(), self._sort_reverse.get())
        movies = self._manager.search(query)

        for row in self._tree.get_children():
            self._tree.delete(row)

        for i, m in enumerate(movies):
            tag = "even" if i % 2 == 0 else "odd"
            self._tree.insert(
                "", "end", iid=m.title,
                values=(
                    m.title, m.director, m.year,
                    m.genre, m.rating,
                    f"{m.score:.1f}", m.score_stars(), m.added_on
                ),
                tags=(tag,)
            )

        count = len(movies)
        total = len(self._manager)
        self._status_var.set(
            f"{count} película(s) mostrada(s) de {total} en la colección."
        )

    def _selected_title(self) -> Optional[str]:
        sel = self._tree.selection()
        return sel[0] if sel else None

    # ── Event handlers ────────────────────────────────────────────

    def _on_add(self):
        dialog = FormDialog(self._root, "Agregar Película")
        if not dialog.result:
            return
        try:
            self._manager.add_movie(**dialog.result)
            self._refresh_table()
            self._status_var.set(f"✓ Película '{dialog.result['title']}' agregada.")
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e), parent=self._root)

    def _on_edit(self):
        title = self._selected_title()
        if not title:
            messagebox.showinfo("Sin selección",
                                "Selecciona una película para editar.",
                                parent=self._root)
            return
        movie = self._manager.get_movie(title)
        if not movie:
            return
        dialog = FormDialog(
            self._root,
            f"Editar — {movie.title}",
            prefill=movie.to_dict()
        )
        if not dialog.result:
            return
        try:
            # If title changed, we need to handle the reel reference carefully
            new_title = dialog.result.get("title", title)
            if new_title != title:
                # Easiest approach: delete & re-add (preserves validation)
                self._manager.delete_movie(title)
                self._manager.add_movie(**dialog.result)
            else:
                self._manager.edit_movie(title, **dialog.result)
            self._refresh_table()
            self._status_var.set(f"✓ Película '{new_title}' actualizada.")
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e), parent=self._root)

    def _on_delete(self):
        title = self._selected_title()
        if not title:
            messagebox.showinfo("Sin selección",
                                "Selecciona una película para eliminar.",
                                parent=self._root)
            return
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar '{title}' de la colección?",
            parent=self._root
        )
        if confirm:
            self._manager.delete_movie(title)
            self._refresh_table()
            self._status_var.set(f"✗ Película '{title}' eliminada.")

    def _on_stats(self):
        StatsPanel(self._root, self._manager.stats())

    def _on_column_sort(self, col: str):
        """Toggle sort direction when clicking a column header."""
        mapping = {
            "title": "title", "director": "director",
            "year": "year", "score": "score"
        }
        if col in mapping:
            if self._sort_field.get() == mapping[col]:
                self._sort_reverse.set(not self._sort_reverse.get())
            else:
                self._sort_field.set(mapping[col])
                self._sort_reverse.set(False)
            self._refresh_table()

    # ── Demo data ─────────────────────────────────────────────────

    def _load_demo_data(self):
        """Pre-load a handful of films to show the app is alive."""
        samples = [
            dict(title="El Padrino",          director="Francis Ford Coppola",
                 year=1972, genre="Crimen",    rating="R",    score=9.2, notes="Obra maestra del cine."),
            dict(title="Interestelar",         director="Christopher Nolan",
                 year=2014, genre="Sci-Fi",    rating="PG-13", score=8.6, notes="Banda sonora increíble."),
            dict(title="Parasite",             director="Bong Joon-ho",
                 year=2019, genre="Thriller",  rating="R",    score=8.5, notes="Palma de Oro y Óscar."),
            dict(title="Spirited Away",        director="Hayao Miyazaki",
                 year=2001, genre="Animación", rating="PG",   score=9.0, notes="Lo mejor de Ghibli."),
            dict(title="Pulp Fiction",         director="Quentin Tarantino",
                 year=1994, genre="Crimen",    rating="R",    score=8.9, notes="Narrativa no lineal genial."),
            dict(title="Amélie",               director="Jean-Pierre Jeunet",
                 year=2001, genre="Romance",   rating="R",    score=8.3, notes="Encantadora."),
            dict(title="Mad Max: Fury Road",   director="George Miller",
                 year=2015, genre="Acción",    rating="R",    score=8.1),
            dict(title="Coco",                 director="Lee Unkrich",
                 year=2017, genre="Animación", rating="PG",   score=8.4,
                 notes="Tributo precioso a la cultura mexicana."),
        ]
        for data in samples:
            try:
                self._manager.add_movie(**data)
            except ValueError:
                pass    # skip invalid demo data silently


# ─────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    app = CineVaultApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


# ═══════════════════════════════════════════════════════════════════
#  POSIBLES MEJORAS / EXTENSIONES
# ═══════════════════════════════════════════════════════════════════
#
#  1. PERSISTENCIA: Guardar/cargar la colección en JSON o SQLite.
#     La capa CatalogManager ya está aislada — solo añadir un
#     método save() / load() sin tocar la GUI.
#
#  2. IMPORTACIÓN / EXPORTACIÓN: CSV o PDF con reportlab.
#
#  3. PAGINACIÓN: Para colecciones > 500 películas, agregar un
#     mecanismo de "páginas" en la FilmReel (cursor + ventana).
#
#  4. COVERS / IMÁGENES: Integrar requests + Pillow para descargar
#     carteles desde TheMovieDB API.
#
#  5. PANEL DE DETALLE: Click en una fila despliega un panel lateral
#     con más información y la imagen del cartel.
#
#  6. FILTRO AVANZADO: Combinar género + rango de año + puntuación
#     mínima en una sola consulta sobre la FilmReel.
#
#  7. MÚLTIPLES COLECCIONES: Añadir un gestor de "listas" (Visto,
#     Pendiente, Favoritas) usando varias instancias de FilmReel.
#
#  8. TESTS UNITARIOS: pytest para Movie, FilmReel y CatalogManager
#     sin depender de Tkinter.
#
# ═══════════════════════════════════════════════════════════════════
