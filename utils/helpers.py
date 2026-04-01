"""Helper utilities for AstraiOS."""
from __future__ import annotations

from datetime import datetime, date
from tkinter import messagebox


APP_BG = "#10131A"
SIDEBAR_BG = "#171B24"
CARD_BG = "#1E2430"
ACCENT = "#9B87F5"
TEXT = "#F5F7FB"
MUTED = "#B8C0D4"
SUCCESS = "#73D2A2"
WARNING = "#F5C26B"
ERROR = "#F07C82"

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_H2 = ("Segoe UI", 15, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
BUTTON_FONT = ("Segoe UI", 10, "bold")


def parse_date(date_str: str) -> date:
    """Parse a date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()



def parse_time(time_str: str) -> datetime.time:
    """Parse a time string in HH:MM 24-hour format."""
    return datetime.strptime(time_str.strip(), "%H:%M").time()



def now_str() -> str:
    """Return current timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



def safe_show_error(title: str, message: str) -> None:
    messagebox.showerror(title, message)



def safe_show_info(title: str, message: str) -> None:
    messagebox.showinfo(title, message)



def days_in_month(year: int, month: int) -> int:
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    return (next_month - date(year, month, 1)).days
