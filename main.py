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

Entry point for the CineVault application.
Run with: python main.py
"""
import tkinter as tk
from ui import CineVaultApp


def main():
    root = tk.Tk()
    app = CineVaultApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
