"""Compatibility checker view."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from backend.compatibility import CompatibilityService
from database.models import CompatibilityLogModel
from utils.helpers import CARD_BG, FONT_BODY, TEXT, parse_date, safe_show_error, safe_show_info


class CompatibilityView(ttk.Frame):
    def __init__(self, parent, compatibility_model: CompatibilityLogModel):
        super().__init__(parent, padding=16)
        self.compatibility_model = compatibility_model
        self.service = CompatibilityService()
        self.configure(style="Content.TFrame")
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Compatibility Checker", style="Title.TLabel").pack(anchor="w", pady=(0, 12))

        form = ttk.Frame(self, style="Card.TFrame", padding=16)
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)

        self.date_one = ttk.Entry(form)
        self.date_two = ttk.Entry(form)

        ttk.Label(form, text="Birthdate 1 (YYYY-MM-DD)", style="Body.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=6)
        self.date_one.grid(row=0, column=1, sticky="ew", pady=6)
        ttk.Label(form, text="Birthdate 2 (YYYY-MM-DD)", style="Body.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 12), pady=6)
        self.date_two.grid(row=1, column=1, sticky="ew", pady=6)

        ttk.Button(form, text="Check Compatibility", command=self.check, style="Accent.TButton").grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        self.output = tk.Text(self, height=12, bg=CARD_BG, fg=TEXT, insertbackground=TEXT, relief="flat", wrap="word", font=FONT_BODY)
        self.output.pack(fill="both", expand=True, pady=(16, 12))

        ttk.Button(self, text="Load Recent Results", command=self.load_recent).pack(anchor="e")

    def check(self):
        try:
            bd1_text = self.date_one.get().strip()
            bd2_text = self.date_two.get().strip()
            result = self.service.check_compatibility(parse_date(bd1_text), parse_date(bd2_text))
            self.compatibility_model.save(
                bd1_text,
                bd2_text,
                result["sign_one"],
                result["sign_two"],
                result["score"],
                result["explanation"],
            )
            text = (
                f"Person A: {result['sign_one']}\n"
                f"Person B: {result['sign_two']}\n"
                f"Compatibility: {result['score']}\n\n"
                f"Explanation:\n{result['explanation']}"
            )
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, text)
            safe_show_info("Saved", "Compatibility result saved successfully.")
        except ValueError:
            safe_show_error("Invalid Input", "Please use YYYY-MM-DD for both birthdates.")
        except Exception as exc:
            safe_show_error("Error", str(exc))

    def load_recent(self):
        rows = self.compatibility_model.recent()
        if not rows:
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "No compatibility checks saved yet.")
            return
        lines = []
        for row in rows:
            lines.append(
                f"[{row['created_at']}] {row['sign_one']} + {row['sign_two']} -> {row['score']}\n{row['explanation']}"
            )
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "\n\n".join(lines))
