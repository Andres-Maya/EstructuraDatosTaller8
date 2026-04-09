"""
CineVaultApp - Main application window
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from services import CatalogManager
from .config import PALETTE
from .form_dialog import FormDialog
from .stats_panel import StatsPanel


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
