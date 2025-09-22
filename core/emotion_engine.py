"""Emotion processing utilities for the Infinity AI framework."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class EmotionAnalysis:
    dominant_emotion: str
    intensity: float
    tags: List[str]
    spectrum: Dict[str, float]


class EmotionEngine:
    """High level interface for emotion detection and enrichment."""

    def analyze(self, text: str, context: Dict[str, float] | None = None) -> EmotionAnalysis:
        context = context or {}
        if not context:
            return EmotionAnalysis("neutral", 0.0, [], {})
        dominant = max(context.items(), key=lambda item: item[1])
        tags = [emotion for emotion, value in context.items() if value > 0.5]
        return EmotionAnalysis(dominant[0], float(dominant[1]), tags, context)


__all__ = ["EmotionEngine", "EmotionAnalysis"]
