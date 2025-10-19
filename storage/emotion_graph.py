"""Graph representation of emotional relationships."""

from __future__ import annotations

from collections import defaultdict


class EmotionGraph:
    def __init__(self) -> None:
        self._graph: dict[str, dict[str, float]] = defaultdict(dict)

    def connect(self, emotion_a: str, emotion_b: str, weight: float) -> None:
        self._graph[emotion_a][emotion_b] = weight
        self._graph[emotion_b][emotion_a] = weight

    def related_emotions(self, emotion: str, threshold: float = 0.5) -> list[str]:
        neighbours = self._graph.get(emotion, {})
        return [name for name, weight in neighbours.items() if weight >= threshold]


__all__ = ["EmotionGraph"]
