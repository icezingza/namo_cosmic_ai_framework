"""Infinity Memory implementation."""

from __future__ import annotations

import hashlib
import uuid
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional

from .emotion_engine import EmotionGraph, QuantumEmotionTagger
from .reflection import ReflectiveAI


class MemoryType(Enum):
    """Types of memories supported by the infinity system."""

    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    EMOTIONAL = "emotional"
    TEMPORAL = "temporal"
    COSMIC = "cosmic"


@dataclass
class MemoryItem:
    """Lightweight item for basic ledger functionality."""

    id: str
    content: str
    embedding: List[float]
    memory_type: MemoryType
    tags: List[str]
    emotions: Dict[str, float]
    timeline_id: str = "earth-616"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    decay_t: int = 14
    conflict_group: Optional[str] = None
    source: str = "event/chat/system"
    cosmic_signature: Optional[str] = None
    importance: float = 0.5
    recall_count: int = 0
    last_recalled: Optional[datetime] = None


@dataclass
class EmotionalSpectrum:
    joy: float = 0.0
    sorrow: float = 0.0
    rage: float = 0.0
    serenity: float = 0.0
    longing: float = 0.0
    betrayal: float = 0.0
    hope: float = 0.0
    nostalgia: float = 0.0


@dataclass
class InfinityMemory:
    id: str
    content: str
    timestamp: datetime
    emotional_spectrum: EmotionalSpectrum
    emotion_intensity: Dict[str, float]
    emotion_tag: List[str]
    emotion_shift_trace: List[Dict[str, Any]]
    cognitive_reflection: str = ""
    psyche_evolution: Dict[str, Any] = field(
        default_factory=lambda: {"pre_state": "", "post_state": "", "growth_vector": []}
    )
    overlapping_memories: List[str] = field(default_factory=list)
    cosmic_signature: str = ""


class InfinityMemorySystem:
    """Manage creation, storage, and recall of infinity memories."""

    def __init__(self) -> None:
        self.memory_db: Dict[str, InfinityMemory] = {}
        self.emotion_nexus = EmotionGraph()
        self.cognito_reflector = ReflectiveAI()
        self.quantum_tagger = QuantumEmotionTagger()

    def create_memory(self, content: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        memory_id = str(uuid.uuid4())
        memory = InfinityMemory(
            id=memory_id,
            content=content,
            timestamp=datetime.utcnow(),
            emotional_spectrum=EmotionalSpectrum(),
            emotion_intensity={},
            emotion_tag=[],
            emotion_shift_trace=[],
        )
        memory = self.quantum_tagger.analyze_emotions(memory)
        memory.cosmic_signature = self._generate_cosmic_signature(memory, context)
        memory.psyche_evolution["growth_vector"] = self._calculate_growth_vector(memory)
        memory.cognitive_reflection = self.cognito_reflector.generate_reflection(
            memory.content, related_topics=memory.emotion_tag
        )
        self.memory_db[memory_id] = memory
        self._update_overlapping_memories(memory_id, memory)
        return {
            "memory_id": memory_id,
            "cosmic_signature": memory.cosmic_signature,
            "emotional_profile": memory.emotion_intensity,
        }

    def recall_memory(self, query: str, emotion_filter: Optional[str] = None, limit: int = 5) -> List[InfinityMemory]:
        query_vector = self._convert_to_cosmic_vector(query)
        candidates: List[tuple[InfinityMemory, float]] = []
        for memory in self.memory_db.values():
            relevance = self._calculate_relevance(memory, query_vector)
            if emotion_filter and memory.emotion_intensity.get(emotion_filter, 0.0) < 0.5:
                continue
            candidates.append((memory, relevance))
        ranked = sorted(candidates, key=lambda item: item[1], reverse=True)[:limit]
        results: List[InfinityMemory] = []
        for memory, _ in ranked:
            memory.recall_count += 1
            memory.last_recalled = datetime.utcnow()
            memory.psyche_evolution["growth_vector"] = self._calculate_growth_vector(memory)
            memory.importance = self._calculate_new_importance(memory)
            results.append(memory)
        return results

    def _convert_to_cosmic_vector(self, text: str) -> Dict[str, float]:
        tokens = [token for token in text.lower().split() if token]
        counts = Counter(tokens)
        total = float(sum(counts.values())) or 1.0
        return {token: freq / total for token, freq in counts.items()}

    def _calculate_relevance(self, memory: InfinityMemory, query_vector: Dict[str, float]) -> float:
        content_vector = self._convert_to_cosmic_vector(memory.content)
        score = sum(content_vector.get(token, 0.0) * weight for token, weight in query_vector.items())
        emotion_boost = sum(memory.emotion_intensity.values()) / max(len(memory.emotion_intensity) or 1, 1)
        return round(score + emotion_boost * 0.1, 3)

    def _generate_cosmic_signature(self, memory: InfinityMemory, context: Optional[Dict[str, Any]]) -> str:
        context_seed = "|".join(f"{key}:{value}" for key, value in sorted((context or {}).items()))
        payload = f"{memory.content}|{memory.emotion_tag}|{context_seed}|{memory.timestamp.isoformat()}"
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
        return f"cosmic::{memory.timestamp.year}::{digest}"

    def _calculate_growth_vector(self, memory: InfinityMemory) -> List[float]:
        base = sum(memory.emotion_intensity.values())
        diversity = len(memory.emotion_intensity)
        return [round(base, 3), round(diversity / 10.0, 3), round(memory.recall_count / 5.0, 3)]

    def _update_overlapping_memories(self, memory_id: str, memory: InfinityMemory) -> None:
        overlaps = self.emotion_nexus.add_node(memory_id, memory.emotion_intensity, memory.timestamp)
        memory.overlapping_memories.extend(overlaps)

    def _calculate_new_importance(self, memory: InfinityMemory) -> float:
        base = 0.5 + 0.05 * memory.recall_count
        freshness = max(0.0, 1.0 - (datetime.utcnow() - memory.timestamp).total_seconds() / 86400.0)
        return round(min(1.0, base + freshness * 0.3), 3)

    def export_ledger(self) -> List[MemoryItem]:
        ledger: List[MemoryItem] = []
        for memory in self.memory_db.values():
            ledger.append(
                MemoryItem(
                    id=memory.id,
                    content=memory.content,
                    embedding=list(memory.emotion_intensity.values()),
                    memory_type=MemoryType.EMOTIONAL,
                    tags=memory.emotion_tag,
                    emotions=memory.emotion_intensity,
                    cosmic_signature=memory.cosmic_signature,
                    importance=memory.importance,
                    recall_count=memory.recall_count,
                    last_recalled=memory.last_recalled,
                )
            )
        return ledger

    def list_memories(self) -> List[InfinityMemory]:
        return list(self.memory_db.values())

    def __len__(self) -> int:  # pragma: no cover - trivial helper
        return len(self.memory_db)
