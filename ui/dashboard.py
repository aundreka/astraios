"""Main dashboard and app shell."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from database.db import DatabaseManager
from database.models import AstrologyProfileModel, CompatibilityLogModel, LunarLogModel, TarotHistoryModel
from ui.astrology_view import AstrologyView
from ui.compatibility_view import CompatibilityView
from ui.lunar_view import LunarView
from ui.tarot_view import TarotView
from utils.helpers import ACCENT, APP_BG, BUTTON_FONT, CARD_BG, FONT_BODY, FONT_H2, FONT_TITLE, MUTED, SIDEBAR_BG, TEXT


class HomeView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=24)
        self.configure(style="Content.TFrame")
        ttk.Label(self, text="AstraiOS", style="Hero.TLabel").pack(anchor="w")
        ttk.Label(self, text="Astrology and Tarot Desktop Application", style="Muted.TLabel").pack(anchor="w", pady=(0, 16))

        grid = ttk.Frame(self, style="Content.TFrame")
        grid.pack(fill="both", expand=True)
        for i in range(2):
            grid.columnconfigure(i, weight=1)
        for i in range(2):
            grid.rowconfigure(i, weight=1)

        cards = [
            ("Astrology Profile", "Create and store your zodiac, moon sign, rising sign, and Chinese zodiac overview."),
            ("Tarot Reading", "Draw a daily card and explore love, career, or general guidance."),
            ("Compatibility Checker", "Compare two birthdates and get a short zodiac-based compatibility result."),
            ("Lunar Calendar", "View the current moon phase and a monthly calendar with full and new moons."),
        ]
        for idx, (title, desc) in enumerate(cards):
            card = ttk.Frame(grid, style="Card.TFrame", padding=18)
            card.grid(row=idx // 2, column=idx % 2, sticky="nsew", padx=8, pady=8)
            ttk.Label(card, text=title, style="Heading.TLabel").pack(anchor="w")
            ttk.Label(card, text=desc, style="BodyWrap.TLabel", wraplength=320, justify="left").pack(anchor="w", pady=(8, 0))


class AstraiOSApp(tk.Tk):
    """Main Tkinter application."""

    def __init__(self):
        super().__init__()
        self.title("AstraiOS – Astrology and Tarot Desktop Application")
        self.geometry("1180x760")
        self.minsize(980, 640)
        self.configure(bg=APP_BG)

        self.db = DatabaseManager()
        self.profile_model = AstrologyProfileModel(self.db)
        self.tarot_model = TarotHistoryModel(self.db)
        self.compatibility_model = CompatibilityLogModel(self.db)
        self.lunar_model = LunarLogModel(self.db)

        self._configure_styles()
        self._build_layout()

    def _configure_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=APP_BG)
        style.configure("Content.TFrame", background=APP_BG)
        style.configure("Sidebar.TFrame", background=SIDEBAR_BG)
        style.configure("Card.TFrame", background=CARD_BG)
        style.configure("TLabel", background=APP_BG, foreground=TEXT, font=FONT_BODY)
        style.configure("Title.TLabel", background=APP_BG, foreground=TEXT, font=FONT_TITLE)
        style.configure("Hero.TLabel", background=APP_BG, foreground=TEXT, font=("Segoe UI", 24, "bold"))
        style.configure("Heading.TLabel", background=CARD_BG, foreground=TEXT, font=FONT_H2)
        style.configure("Body.TLabel", background=CARD_BG, foreground=TEXT, font=FONT_BODY)
        style.configure("BodyWrap.TLabel", background=CARD_BG, foreground=TEXT, font=FONT_BODY)
        style.configure("Muted.TLabel", background=APP_BG, foreground=MUTED, font=FONT_BODY)
        style.configure("TEntry", padding=6)
        style.configure("TCombobox", padding=4)
        style.configure("TSpinbox", padding=4)
        style.configure("TButton", font=BUTTON_FONT, padding=8)
        style.configure("Accent.TButton", font=BUTTON_FONT, padding=8)
        style.map("Accent.TButton", background=[("active", ACCENT), ("!disabled", ACCENT)], foreground=[("!disabled", "#FFFFFF")])

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        sidebar = ttk.Frame(self, style="Sidebar.TFrame", padding=16)
        sidebar.grid(row=0, column=0, sticky="nsw")

        ttk.Label(sidebar, text="AstraiOS", background=SIDEBAR_BG, foreground=TEXT, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 18))

        nav_buttons = [
            ("Dashboard", "home"),
            ("Astrology Profile", "astrology"),
            ("Tarot Reading", "tarot"),
            ("Compatibility Checker", "compatibility"),
            ("Lunar Calendar", "lunar"),
        ]
        for label, key in nav_buttons:
            btn = tk.Label(sidebar, text=label, bg=SIDEBAR_BG, fg=TEXT, font=("Segoe UI", 10, "bold"), padx=12, pady=10, cursor="hand2")
            btn.pack(fill="x", pady=4)
            btn.bind("<Button-1>", lambda _e, k=key: self.show_frame(k))
            btn.bind("<Enter>", lambda e: e.widget.config(bg=ACCENT))
            btn.bind("<Leave>", lambda e: e.widget.config(bg=SIDEBAR_BG))

        self.container = ttk.Frame(self, style="Content.TFrame")
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {
            "home": HomeView(self.container),
            "astrology": AstrologyView(self.container, self.profile_model),
            "tarot": TarotView(self.container, self.tarot_model),
            "compatibility": CompatibilityView(self.container, self.compatibility_model),
            "lunar": LunarView(self.container, self.lunar_model),
        }

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("home")

    def show_frame(self, name: str):
        frame = self.frames[name]
        frame.tkraise()
