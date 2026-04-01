"""Astrology view."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from backend.astrology import AstrologyService
from database.models import AstrologyProfileModel
from utils.helpers import CARD_BG, FONT_BODY, FONT_H2, MUTED, TEXT, parse_date, parse_time, safe_show_error, safe_show_info


class AstrologyView(ttk.Frame):
    def __init__(self, parent, profile_model: AstrologyProfileModel):
        super().__init__(parent, padding=16)
        self.profile_model = profile_model
        self.service = AstrologyService()
        self.configure(style="Content.TFrame")
        self._build_ui()

    def _build_ui(self):
        title = ttk.Label(self, text="Astrology Profile", style="Title.TLabel")
        title.pack(anchor="w", pady=(0, 12))

        form = ttk.Frame(self, style="Card.TFrame", padding=16)
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)

        labels = ["Name", "Birthdate (YYYY-MM-DD)", "Birth time (HH:MM, optional)", "Birth location (optional)"]
        self.entries = {}
        keys = ["name", "birthdate", "birth_time", "birth_location"]

        for i, (label_text, key) in enumerate(zip(labels, keys)):
            ttk.Label(form, text=label_text, style="Body.TLabel").grid(row=i, column=0, sticky="w", padx=(0, 12), pady=6)
            entry = ttk.Entry(form)
            entry.grid(row=i, column=1, sticky="ew", pady=6)
            self.entries[key] = entry

        ttk.Button(form, text="Generate Profile", command=self.generate_profile, style="Accent.TButton").grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        self.output = tk.Text(self, height=10, bg=CARD_BG, fg=TEXT, insertbackground=TEXT, relief="flat", wrap="word", font=FONT_BODY)
        self.output.pack(fill="both", expand=True, pady=(16, 12))

        ttk.Button(self, text="Load Recent Profiles", command=self.load_recent).pack(anchor="e")

    def generate_profile(self):
        try:
            name = self.entries["name"].get().strip() or "Guest"
            birthdate_text = self.entries["birthdate"].get().strip()
            birthdate = parse_date(birthdate_text)
            birth_time_text = self.entries["birth_time"].get().strip()
            birth_time = parse_time(birth_time_text) if birth_time_text else None
            birth_location = self.entries["birth_location"].get().strip()

            result = self.service.create_profile(birthdate, birth_time, birth_location)
            self.profile_model.save(
                name,
                birthdate_text,
                birth_time_text,
                birth_location,
                result.zodiac_sign,
                result.moon_sign,
                result.rising_sign,
                result.chinese_zodiac,
            )

            text = (
                f"Name: {name}\n"
                f"Zodiac Sign: {result.zodiac_sign}\n"
                f"Description: {result.zodiac_description}\n"
                f"Moon Sign: {result.moon_sign}\n"
                f"Rising Sign: {result.rising_sign}\n"
                f"Chinese Zodiac: {result.chinese_zodiac}\n"
                f"\nNote: Moon and rising signs are simplified unless astronomy-grade calculations are added."
            )
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, text)
            safe_show_info("Saved", "Astrology profile saved successfully.")
        except ValueError:
            safe_show_error("Invalid Input", "Please use YYYY-MM-DD for birthdate and HH:MM for birth time.")
        except Exception as exc:
            safe_show_error("Error", str(exc))

    def load_recent(self):
        rows = self.profile_model.recent()
        if not rows:
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "No saved astrology profiles yet.")
            return

        lines = []
        for row in rows:
            lines.append(
                f"[{row['created_at']}] {row['name']} - {row['zodiac_sign']} | Moon: {row['moon_sign']} | Rising: {row['rising_sign']}"
            )
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "\n".join(lines))
