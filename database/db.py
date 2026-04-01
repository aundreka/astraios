"""SQLite database helper."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable


DB_PATH = Path(__file__).resolve().parent / "astraios.db"


class DatabaseManager:
    """Simple SQLite wrapper for AstraiOS."""

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or str(DB_PATH)
        self._initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.executescript(
                """
                CREATE TABLE IF NOT EXISTS astrology_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    birthdate TEXT NOT NULL,
                    birth_time TEXT,
                    birth_location TEXT,
                    zodiac_sign TEXT NOT NULL,
                    moon_sign TEXT,
                    rising_sign TEXT,
                    chinese_zodiac TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS tarot_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    card_name TEXT NOT NULL,
                    meaning TEXT NOT NULL,
                    ai_explanation TEXT,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS compatibility_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    birthdate_one TEXT NOT NULL,
                    birthdate_two TEXT NOT NULL,
                    sign_one TEXT NOT NULL,
                    sign_two TEXT NOT NULL,
                    score TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS lunar_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_date TEXT NOT NULL,
                    phase_name TEXT NOT NULL,
                    special_event TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )
            conn.commit()

    def execute(self, query: str, params: Iterable[Any] = ()) -> None:
        with self.connect() as conn:
            conn.execute(query, tuple(params))
            conn.commit()

    def fetch_all(self, query: str, params: Iterable[Any] = ()) -> list[sqlite3.Row]:
        with self.connect() as conn:
            rows = conn.execute(query, tuple(params)).fetchall()
        return rows
