"""Emotion processing components for the integrated AI framework."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from math import sqrt
from typing import Dict, Iterable, List, Tuple

# Core lexicon that anchors the hybrid emotion model. The list is intentionally
# lightweight so it can run in restricted environments while still producing
# consistent, interpretable signals for downstream components.
EMOTION_KEYWORDS: Dict[str, Tuple[str, ...]] = {
    "joy": ("happy", "joy", "excited", "pleased", "delighted"),
    "sorrow": ("sad", "sorrow", "unhappy", "cry", "เศร้า"),
    "rage": ("angry", "rage", "furious", "mad", "โกรธ"),
    "serenity": ("calm", "peaceful", "serene", "tranquil", "สงบ"),
    "longing": ("miss", "longing", "yearn", "desire", "โหยหา"),
    "betrayal": ("betray", "treachery", "deceive", "trust", "หักหลัง"),
    "hope": ("hope", "optimistic", "expect", "wish", "หวัง"),
    "nostalgia": ("nostalgia", "remember", "memory", "past", "คิดถึง"),
}


@dataclass(frozen=True)
class EmotionShift:
    """Represents a timestamped snapshot of an emotional state."""

    timestamp: datetime
    emotions: Dict[str, float]
    trigger: str


class QuantumEmotionTagger:
    """Hybrid lexicon and heuristic based emotion annotator."""

    def __init__(self, emotion_lexicon: Dict[str, Tuple[str, ...]] | None = None) -> None:
        self.emotion_lexicon = emotion_lexicon or EMOTION_KEYWORDS

    def analyze_emotions(self, memory: "InfinityMemory") -> "InfinityMemory":
        """Annotate a memory with tags, intensities, and the first shift trace."""

        tags = self._extract_emotion_tags(memory.content)
        intensities = self._calculate_emotion_intensity(memory.content, tags)
        memory.emotion_tag = tags
        memory.emotion_intensity = intensities
        memory.emotion_shift_trace.append(
            EmotionShift(timestamp=datetime.now(UTC), emotions=dict(intensities), trigger="initial_analysis").__dict__
        )
        return memory

    def _extract_emotion_tags(self, content: str) -> List[str]:
        content_lower = content.lower()
        tags: List[str] = []
        for emotion, keywords in self.emotion_lexicon.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(emotion)
        if not tags:
            tags.append("serenity")
        return tags

    def _calculate_emotion_intensity(self, content: str, tags: Iterable[str]) -> Dict[str, float]:
        base = max(len(content) / 120.0, 0.1)
        intensities: Dict[str, float] = {}
        for emotion in tags:
            multiplier = 1.0 + 0.1 * len(emotion)
            intensity = min(1.0, base * multiplier)
            intensities[emotion] = round(intensity, 3)
        return intensities


class EmotionGraph:
    """Track emotional similarity across stored memories."""

    def __init__(self) -> None:
        self.nodes: Dict[str, Dict[str, object]] = {}
        self.edges: Dict[Tuple[str, str], Dict[str, float | datetime]] = {}

    def add_node(self, memory_id: str, emotions: Dict[str, float], timestamp: datetime) -> List[str]:
        connections = self._find_emotional_connections(memory_id, emotions)
        self.nodes[memory_id] = {
            "emotions": emotions,
            "timestamp": timestamp,
            "connections": connections,
        }
        return connections

    def _find_emotional_connections(self, memory_id: str, emotions: Dict[str, float]) -> List[str]:
        connections: List[str] = []
        for other_id, other_data in self.nodes.items():
            if other_id == memory_id:
                continue
            similarity = self._calculate_emotional_similarity(emotions, other_data["emotions"])
            if similarity >= 0.7:
                self.edges[(memory_id, other_id)] = {"similarity": similarity, "created": datetime.now(UTC)}
                connections.append(other_id)
        return connections

    def _calculate_emotional_similarity(self, emotions1: Dict[str, float], emotions2: Dict[str, float]) -> float:
        all_emotions = set(emotions1) | set(emotions2)
        if not all_emotions:
            return 0.0
        vector1 = [emotions1.get(emotion, 0.0) for emotion in all_emotions]
        vector2 = [emotions2.get(emotion, 0.0) for emotion in all_emotions]
        dot_product = sum(a * b for a, b in zip(vector1, vector2))
        magnitude1 = sqrt(sum(a * a for a in vector1))
        magnitude2 = sqrt(sum(b * b for b in vector2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        return round(dot_product / (magnitude1 * magnitude2), 3)
