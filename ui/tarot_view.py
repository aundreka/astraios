"""Tarot view."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from backend.tarot import TarotService
from database.models import TarotHistoryModel
from utils.helpers import CARD_BG, FONT_BODY, TEXT, safe_show_error, safe_show_info


class TarotView(ttk.Frame):
    def __init__(self, parent, tarot_model: TarotHistoryModel):
        super().__init__(parent, padding=16)
        self.tarot_model = tarot_model
        self.service = TarotService()
        self.configure(style="Content.TFrame")
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Tarot Reading", style="Title.TLabel").pack(anchor="w", pady=(0, 12))

        controls = ttk.Frame(self, style="Card.TFrame", padding=16)
        controls.pack(fill="x")

        ttk.Label(controls, text="Reading Category", style="Body.TLabel").pack(anchor="w")
        self.category = tk.StringVar(value="General")
        combo = ttk.Combobox(controls, textvariable=self.category, values=["General", "Love", "Career"], state="readonly")
        combo.pack(fill="x", pady=(6, 12))

        btn_frame = ttk.Frame(controls, style="Card.TFrame")
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Daily Draw", command=self.daily_draw, style="Accent.TButton").pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="Random Draw", command=self.daily_draw).pack(side="left")

        self.output = tk.Text(self, height=14, bg=CARD_BG, fg=TEXT, insertbackground=TEXT, relief="flat", wrap="word", font=FONT_BODY)
        self.output.pack(fill="both", expand=True, pady=(16, 12))
        ttk.Button(self, text="Load Reading History", command=self.load_recent).pack(anchor="e")

    def daily_draw(self):
        try:
            result = self.service.draw_card(self.category.get())
            self.tarot_model.save(result["category"], result["card_name"], result["meaning"], result["ai_explanation"])
            text = (
                f"Category: {result['category']}\n"
                f"Card: {result['card_name']}\n\n"
                f"Meaning:\n{result['meaning']}\n\n"
                f"Expanded Interpretation:\n{result['ai_explanation']}"
            )
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, text)
            safe_show_info("Saved", "Tarot reading saved successfully.")
        except Exception as exc:
            safe_show_error("Error", str(exc))

    def load_recent(self):
        rows = self.tarot_model.recent()
        if not rows:
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "No tarot history yet.")
            return
        lines = []
        for row in rows:
            lines.append(f"[{row['created_at']}] {row['category']}: {row['card_name']} - {row['meaning']}")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "\n\n".join(lines))
