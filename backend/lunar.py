"""Lunar calculations and calendar helpers."""
from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Tuple


@dataclass
class MoonPhaseResult:
    phase_name: str
    illumination_hint: str
    special_event: str


class LunarService:
    """Provides lightweight moon phase calculations."""

    PHASES = [
        (1.84566, "New Moon"),
        (5.53699, "Waxing Crescent"),
        (9.22831, "First Quarter"),
        (12.91963, "Waxing Gibbous"),
        (16.61096, "Full Moon"),
        (20.30228, "Waning Gibbous"),
        (23.99361, "Last Quarter"),
        (27.68493, "Waning Crescent"),
        (29.53059, "New Moon"),
    ]

    def moon_age(self, target_date: date) -> float:
        year = target_date.year
        month = target_date.month
        day = target_date.day

        if month < 3:
            year -= 1
            month += 12

        month += 1
        c = 365.25 * year
        e = 30.6 * month
        jd = c + e + day - 694039.09
        jd /= 29.5305882
        b = int(jd)
        jd -= b
        age = jd * 29.5305882
        return age

    def get_moon_phase(self, target_date: date | None = None) -> MoonPhaseResult:
        if target_date is None:
            target_date = datetime.now().date()

        age = self.moon_age(target_date)
        phase_name = "New Moon"
        for limit, label in self.PHASES:
            if age <= limit:
                phase_name = label
                break

        if phase_name == "Full Moon":
            special = "Special event: Full Moon"
            illumination = "Illumination is near maximum."
        elif phase_name == "New Moon":
            special = "Special event: New Moon"
            illumination = "Illumination is near minimum."
        else:
            special = "No major lunar event today."
            illumination = f"Current phase is {phase_name.lower()}."

        return MoonPhaseResult(phase_name=phase_name, illumination_hint=illumination, special_event=special)

    def month_calendar(self, year: int, month: int) -> List[List[int]]:
        return calendar.monthcalendar(year, month)

    def special_days(self, year: int, month: int) -> List[Tuple[int, str]]:
        total_days = calendar.monthrange(year, month)[1]
        events: List[Tuple[int, str]] = []
        for day in range(1, total_days + 1):
            phase = self.get_moon_phase(date(year, month, day)).phase_name
            if phase in {"Full Moon", "New Moon"}:
                events.append((day, phase))
        return events
