"""
StatsPanel - Statistics display window
"""
import tkinter as tk
from .config import PALETTE


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
