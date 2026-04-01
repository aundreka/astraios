"""Astrology-related business logic."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from typing import Optional


@dataclass
class AstrologyResult:
    zodiac_sign: str
    zodiac_description: str
    chinese_zodiac: str
    moon_sign: str
    rising_sign: str


class AstrologyService:
    """Compute simplified astrology results."""

    ZODIAC_RANGES = [
        ((1, 20), "Capricorn"),
        ((2, 19), "Aquarius"),
        ((3, 21), "Pisces"),
        ((4, 20), "Aries"),
        ((5, 21), "Taurus"),
        ((6, 21), "Gemini"),
        ((7, 23), "Cancer"),
        ((8, 23), "Leo"),
        ((9, 23), "Virgo"),
        ((10, 23), "Libra"),
        ((11, 22), "Scorpio"),
        ((12, 22), "Sagittarius"),
        ((12, 32), "Capricorn"),
    ]

    ZODIAC_DESCRIPTIONS = {
        "Aries": "Bold, energetic, and action-driven.",
        "Taurus": "Grounded, dependable, and comfort-loving.",
        "Gemini": "Curious, expressive, and mentally agile.",
        "Cancer": "Intuitive, caring, and emotionally deep.",
        "Leo": "Confident, creative, and warm-hearted.",
        "Virgo": "Analytical, practical, and detail-oriented.",
        "Libra": "Balanced, diplomatic, and relationship-focused.",
        "Scorpio": "Intense, passionate, and transformative.",
        "Sagittarius": "Adventurous, optimistic, and freedom-seeking.",
        "Capricorn": "Disciplined, ambitious, and resilient.",
        "Aquarius": "Innovative, independent, and visionary.",
        "Pisces": "Compassionate, imaginative, and reflective.",
    }

    CHINESE_ZODIAC = [
        "Monkey", "Rooster", "Dog", "Pig", "Rat", "Ox",
        "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat"
    ]

    RISING_SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    MOON_SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    def get_zodiac_sign(self, birthdate: date) -> str:
        for (month, day_limit), sign in self.ZODIAC_RANGES:
            if birthdate.month < month or (birthdate.month == month and birthdate.day < day_limit):
                return sign
        return "Capricorn"

    def get_chinese_zodiac(self, birthdate: date) -> str:
        return self.CHINESE_ZODIAC[birthdate.year % 12]

    def get_moon_sign(self, birthdate: date) -> str:
        """Approximate moon sign using day-of-year cycling.

        This is intentionally lightweight and does not require astronomy libraries.
        """
        doy = birthdate.timetuple().tm_yday
        index = ((doy - 1) // 3) % 12
        return self.MOON_SIGNS[index]

    def get_rising_sign(self, birth_time: Optional[time]) -> str:
        """Approximate rising sign from birth time in 2-hour blocks."""
        if birth_time is None:
            return "Unavailable (birth time not provided)"
        index = (birth_time.hour // 2) % 12
        return self.RISING_SIGNS[index]

    def create_profile(
        self,
        birthdate: date,
        birth_time: Optional[time] = None,
        birth_location: Optional[str] = None,
    ) -> AstrologyResult:
        zodiac = self.get_zodiac_sign(birthdate)
        chinese = self.get_chinese_zodiac(birthdate)
        moon = self.get_moon_sign(birthdate)
        rising = self.get_rising_sign(birth_time)

        if birth_location and "Unavailable" not in rising:
            rising = f"{rising} (approx., location-aware refinement not enabled)"

        return AstrologyResult(
            zodiac_sign=zodiac,
            zodiac_description=self.ZODIAC_DESCRIPTIONS[zodiac],
            chinese_zodiac=chinese,
            moon_sign=moon,
            rising_sign=rising,
        )
