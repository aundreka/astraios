"""Tarot reading logic."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class TarotCard:
    name: str
    general: str
    love: str
    career: str


class TarotService:
    """Provides tarot card draws and interpretations."""

    def __init__(self) -> None:
        self.cards: List[TarotCard] = [
            TarotCard("The Fool", "A new beginning is unfolding.", "Take a chance in love with an open heart.", "An exciting opportunity may reward courage."),
            TarotCard("The Magician", "You have the tools to shape your path.", "Clear communication can strengthen connection.", "Your skills are ready to be used with confidence."),
            TarotCard("The High Priestess", "Trust your intuition and inner knowing.", "Emotional truth matters more than surface signals.", "Pause and observe before making a work decision."),
            TarotCard("The Empress", "Growth, abundance, and nurturing surround you.", "Love deepens through care and patience.", "A creative or fruitful phase is beginning."),
            TarotCard("The Emperor", "Structure and discipline are needed.", "Healthy boundaries improve relationships.", "Leadership and organization bring progress."),
            TarotCard("The Lovers", "A heartfelt choice stands before you.", "Alignment and intimacy are highlighted.", "Partnerships and values-based decisions matter now."),
            TarotCard("The Chariot", "Momentum builds when focus is steady.", "Move forward with emotional clarity.", "Determination can drive a major win."),
            TarotCard("Strength", "Gentle courage will carry you through.", "Compassion and patience heal tension.", "Resilience matters more than force."),
            TarotCard("The Hermit", "Reflection will reveal the next step.", "Time alone can clarify your feelings.", "A thoughtful pause can improve long-term results."),
            TarotCard("Wheel of Fortune", "Change is turning in your favor.", "A relationship dynamic may shift unexpectedly.", "Timing and adaptability are especially important."),
            TarotCard("Justice", "Truth, fairness, and accountability are central.", "Honesty creates balance in love.", "Make careful and ethical decisions at work."),
            TarotCard("The Star", "Hope and renewal are returning.", "Healing energy surrounds the heart.", "Long-term goals are worth believing in again."),
            TarotCard("The Moon", "Not everything is fully visible yet.", "Avoid assumptions and listen deeply.", "Uncertainty calls for careful judgment."),
            TarotCard("The Sun", "Joy, clarity, and confidence shine strongly.", "Warmth and openness strengthen romance.", "Recognition and success are close."),
            TarotCard("Judgement", "A calling or awakening is emerging.", "Past lessons can reshape present love.", "A major evaluation or pivot is near."),
            TarotCard("The World", "Completion and fulfillment are within reach.", "A relationship enters a more whole phase.", "A project cycle may conclude successfully."),
        ]

    def draw_card(self, category: str = "general") -> Dict[str, str]:
        card = random.choice(self.cards)
        category = category.lower().strip()
        if category not in {"general", "love", "career"}:
            category = "general"

        meaning = {
            "general": card.general,
            "love": card.love,
            "career": card.career,
        }[category]
        return {
            "card_name": card.name,
            "category": category.title(),
            "meaning": meaning,
            "ai_explanation": self.generate_ai_explanation(card.name, meaning, category),
        }

    def generate_ai_explanation(self, card_name: str, meaning: str, category: str) -> str:
        """Fallback local explanation when no external AI service is configured."""
        return (
            f"{card_name} in a {category} reading suggests that you should focus on the core message: "
            f"{meaning.lower()} Reflect on how this theme connects with your present choices and emotions."
        )
