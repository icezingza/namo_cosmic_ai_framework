"""Dharma reasoning helpers for the integrated AI framework."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Sequence

from .memory_core import InfinityMemory


@dataclass
class TurningPoint:
    timestamp: datetime
    shift_magnitude: float
    from_memory: str
    to_memory: str
    description: str


class DharmaReasoningModule:
    """Provide Dharma-grounded insights for a collection of memories."""

    def generate_reflection(self, memory: InfinityMemory, related_memories: Sequence[InfinityMemory]) -> str:
        emotional_patterns = self._analyze_emotional_patterns([memory, *related_memories])
        turning_points = self._identify_turning_points([memory, *related_memories])
        insight = self._apply_dharma_principles(memory, emotional_patterns, turning_points)
        return insight

    def _analyze_emotional_patterns(self, memories: Iterable[InfinityMemory]) -> Dict[str, Any]:
        aggregate: Dict[str, float] = {}
        for memory in memories:
            for emotion, intensity in memory.emotion_intensity.items():
                aggregate[emotion] = aggregate.get(emotion, 0.0) + intensity
        dominant = dict(sorted(aggregate.items(), key=lambda item: item[1], reverse=True)[:3])
        return {"dominant_emotions": dominant}

    def _identify_turning_points(self, memories: Iterable[InfinityMemory]) -> List[TurningPoint]:
        ordered = sorted(memories, key=lambda mem: mem.timestamp)
        points: List[TurningPoint] = []
        for previous, current in zip(ordered, ordered[1:]):
            shift = self._calculate_emotional_shift(previous, current)
            if shift > 0.5:
                points.append(
                    TurningPoint(
                        timestamp=current.timestamp,
                        shift_magnitude=shift,
                        from_memory=previous.id,
                        to_memory=current.id,
                        description=f"เปลี่ยนจาก {previous.emotion_tag} เป็น {current.emotion_tag}",
                    )
                )
        return points

    def _calculate_emotional_shift(self, previous: InfinityMemory, current: InfinityMemory) -> float:
        previous_emotions = previous.emotion_intensity
        current_emotions = current.emotion_intensity
        total_shift = 0.0
        keys = set(previous_emotions) | set(current_emotions)
        for key in keys:
            total_shift += abs(current_emotions.get(key, 0.0) - previous_emotions.get(key, 0.0))
        return round(total_shift / max(len(keys) or 1, 1), 3)

    def _apply_dharma_principles(
        self, memory: InfinityMemory, patterns: Dict[str, Any], turning_points: Sequence[TurningPoint]
    ) -> str:
        dominant = patterns.get("dominant_emotions", {})
        summary_lines = [f"การวิเคราะห์ความทรงจำ {memory.id} ผ่านหลักธรรม:"]
        if dominant:
            joined = ", ".join(f"{emotion}:{intensity:.2f}" for emotion, intensity in dominant.items())
            summary_lines.append(f"- อารมณ์เด่น: {joined}")
        if any(emotion in ("sorrow", "rage") for emotion in dominant):
            summary_lines.append("- ตามหลักอนิจจัง ทุกอารมณ์ล้วนผันแปร จงรู้เท่าทัน")
        if any(emotion in ("hope", "serenity") for emotion in dominant):
            summary_lines.append("- หลักอริยสัจ: ความหวังและความสงบช่วยให้เห็นหนทางออกจากทุกข์")
        if turning_points:
            summary_lines.append(f"- พบจุดเปลี่ยนสำคัญ {len(turning_points)} ช่วง")
        summary_lines.append("- ข้อแนะนำ: เจริญสติรับรู้อารมณ์ก่อนตอบสนอง")
        return "\n".join(summary_lines)
