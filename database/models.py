"""High-level data access methods."""
from __future__ import annotations

from database.db import DatabaseManager
from utils.helpers import now_str


class AstrologyProfileModel:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def save(self, name: str, birthdate: str, birth_time: str, birth_location: str, zodiac_sign: str, moon_sign: str, rising_sign: str, chinese_zodiac: str) -> None:
        self.db.execute(
            """
            INSERT INTO astrology_profiles
            (name, birthdate, birth_time, birth_location, zodiac_sign, moon_sign, rising_sign, chinese_zodiac, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (name, birthdate, birth_time, birth_location, zodiac_sign, moon_sign, rising_sign, chinese_zodiac, now_str()),
        )

    def recent(self) -> list:
        return self.db.fetch_all("SELECT * FROM astrology_profiles ORDER BY id DESC LIMIT 10")


class TarotHistoryModel:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def save(self, category: str, card_name: str, meaning: str, ai_explanation: str) -> None:
        self.db.execute(
            "INSERT INTO tarot_history (category, card_name, meaning, ai_explanation, created_at) VALUES (?, ?, ?, ?, ?)",
            (category, card_name, meaning, ai_explanation, now_str()),
        )

    def recent(self) -> list:
        return self.db.fetch_all("SELECT * FROM tarot_history ORDER BY id DESC LIMIT 10")


class CompatibilityLogModel:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def save(self, birthdate_one: str, birthdate_two: str, sign_one: str, sign_two: str, score: str, explanation: str) -> None:
        self.db.execute(
            """
            INSERT INTO compatibility_logs
            (birthdate_one, birthdate_two, sign_one, sign_two, score, explanation, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (birthdate_one, birthdate_two, sign_one, sign_two, score, explanation, now_str()),
        )

    def recent(self) -> list:
        return self.db.fetch_all("SELECT * FROM compatibility_logs ORDER BY id DESC LIMIT 10")


class LunarLogModel:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def save(self, target_date: str, phase_name: str, special_event: str) -> None:
        self.db.execute(
            "INSERT INTO lunar_logs (target_date, phase_name, special_event, created_at) VALUES (?, ?, ?, ?)",
            (target_date, phase_name, special_event, now_str()),
        )

    def recent(self) -> list:
        return self.db.fetch_all("SELECT * FROM lunar_logs ORDER BY id DESC LIMIT 10")
