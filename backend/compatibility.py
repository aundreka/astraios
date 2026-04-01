"""Zodiac compatibility logic."""
from __future__ import annotations

from datetime import date

from backend.astrology import AstrologyService


class CompatibilityService:
    """Provides simple zodiac compatibility results."""

    def __init__(self) -> None:
        self.astrology_service = AstrologyService()
        self.compatibility_map = {
            "Aries": {"best": ["Leo", "Sagittarius", "Gemini"], "challenging": ["Cancer", "Capricorn"]},
            "Taurus": {"best": ["Virgo", "Capricorn", "Cancer"], "challenging": ["Leo", "Aquarius"]},
            "Gemini": {"best": ["Libra", "Aquarius", "Aries"], "challenging": ["Virgo", "Pisces"]},
            "Cancer": {"best": ["Scorpio", "Pisces", "Taurus"], "challenging": ["Aries", "Libra"]},
            "Leo": {"best": ["Aries", "Sagittarius", "Libra"], "challenging": ["Taurus", "Scorpio"]},
            "Virgo": {"best": ["Taurus", "Capricorn", "Cancer"], "challenging": ["Gemini", "Sagittarius"]},
            "Libra": {"best": ["Gemini", "Aquarius", "Leo"], "challenging": ["Cancer", "Capricorn"]},
            "Scorpio": {"best": ["Cancer", "Pisces", "Virgo"], "challenging": ["Leo", "Aquarius"]},
            "Sagittarius": {"best": ["Aries", "Leo", "Aquarius"], "challenging": ["Virgo", "Pisces"]},
            "Capricorn": {"best": ["Taurus", "Virgo", "Scorpio"], "challenging": ["Aries", "Libra"]},
            "Aquarius": {"best": ["Gemini", "Libra", "Sagittarius"], "challenging": ["Taurus", "Scorpio"]},
            "Pisces": {"best": ["Cancer", "Scorpio", "Capricorn"], "challenging": ["Gemini", "Sagittarius"]},
        }

    def check_compatibility(self, birthdate_one: date, birthdate_two: date) -> dict:
        sign_one = self.astrology_service.get_zodiac_sign(birthdate_one)
        sign_two = self.astrology_service.get_zodiac_sign(birthdate_two)
        best = self.compatibility_map[sign_one]["best"]
        challenging = self.compatibility_map[sign_one]["challenging"]

        if sign_two in best:
            score = "High"
            explanation = f"{sign_one} and {sign_two} often connect through complementary energy, flow, and mutual encouragement."
        elif sign_two in challenging:
            score = "Moderate to Challenging"
            explanation = f"{sign_one} and {sign_two} may need extra patience because their instincts and priorities can differ."
        elif sign_one == sign_two:
            score = "Balanced"
            explanation = f"Two {sign_one} signs usually understand each other well, though similar habits can amplify strengths and weaknesses."
        else:
            score = "Moderate"
            explanation = f"{sign_one} and {sign_two} have a mixed but workable dynamic that can thrive with communication and effort."

        return {
            "sign_one": sign_one,
            "sign_two": sign_two,
            "score": score,
            "explanation": explanation,
        }
