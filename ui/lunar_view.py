"""Lunar calendar view."""
from __future__ import annotations

from datetime import datetime, date
import tkinter as tk
from tkinter import ttk

from backend.lunar import LunarService
from database.models import LunarLogModel
from utils.helpers import CARD_BG, FONT_BODY, TEXT, days_in_month, safe_show_error


class LunarView(ttk.Frame):
    def __init__(self, parent, lunar_model: LunarLogModel):
        super().__init__(parent, padding=16)
        self.lunar_model = lunar_model
        self.service = LunarService()
        self.configure(style="Content.TFrame")
        self._build_ui()
        self.refresh_calendar()

    def _build_ui(self):
        ttk.Label(self, text="Lunar Calendar", style="Title.TLabel").pack(anchor="w", pady=(0, 12))

        top = ttk.Frame(self, style="Card.TFrame", padding=16)
        top.pack(fill="x")

        now = datetime.now()
        self.year_var = tk.IntVar(value=now.year)
        self.month_var = tk.IntVar(value=now.month)

        row = ttk.Frame(top, style="Card.TFrame")
        row.pack(fill="x")

        ttk.Label(row, text="Year", style="Body.TLabel").pack(side="left")
        ttk.Spinbox(row, from_=1900, to=2100, textvariable=self.year_var, width=8).pack(side="left", padx=(6, 12))
        ttk.Label(row, text="Month", style="Body.TLabel").pack(side="left")
        ttk.Spinbox(row, from_=1, to=12, textvariable=self.month_var, width=5).pack(side="left", padx=(6, 12))
        ttk.Button(row, text="Refresh", command=self.refresh_calendar, style="Accent.TButton").pack(side="left")

        self.phase_label = ttk.Label(top, text="", style="Body.TLabel")
        self.phase_label.pack(anchor="w", pady=(12, 0))
        self.special_label = ttk.Label(top, text="", style="Muted.TLabel")
        self.special_label.pack(anchor="w")

        self.calendar_text = tk.Text(self, height=16, bg=CARD_BG, fg=TEXT, insertbackground=TEXT, relief="flat", wrap="none", font=("Consolas", 10))
        self.calendar_text.pack(fill="both", expand=True, pady=(16, 12))

    def refresh_calendar(self):
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            if month < 1 or month > 12:
                raise ValueError("Month out of range")

            today_phase = self.service.get_moon_phase()
            self.phase_label.config(text=f"Today: {today_phase.phase_name} — {today_phase.illumination_hint}")
            self.special_label.config(text=today_phase.special_event)

            self.lunar_model.save(str(date.today()), today_phase.phase_name, today_phase.special_event)

            weeks = self.service.month_calendar(year, month)
            specials = dict(self.service.special_days(year, month))
            header = "Mo Tu We Th Fr Sa Su\n"
            body_lines = []
            for week in weeks:
                cells = []
                for day in week:
                    if day == 0:
                        cells.append("  ")
                    elif day in specials:
                        marker = "F" if specials[day] == "Full Moon" else "N"
                        cells.append(f"{day:>2}{marker}")
                    else:
                        cells.append(f"{day:>2} ")
                body_lines.append(" ".join(cells))

            legend = "\n\nLegend: F = Full Moon, N = New Moon"
            self.calendar_text.delete("1.0", tk.END)
            self.calendar_text.insert(tk.END, header + "\n".join(body_lines) + legend)
        except Exception as exc:
            safe_show_error("Error", str(exc))
