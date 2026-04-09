"""
FormDialog - Modal dialog for adding/editing movies
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional
from models import Movie
from .config import PALETTE


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
