"""Infinity Memory implementation.

The previous prototype kept everything in process memory which meant data was
lost between runs and querying only relied on transient python objects.  To
support real usage scenarios we back the system with a lightweight SQLite
store, persist the emotional annotations and expose a practical recall method
based on simple term-frequency scoring.  The design intentionally avoids heavy
ML dependencies so it can run in constrained environments while still being
deterministic and easy to test.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

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
    embedding: list[float]
    memory_type: MemoryType
    tags: list[str]
    emotions: dict[str, float]
    timeline_id: str = "earth-616"
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    decay_t: int = 14
    conflict_group: str | None = None
    source: str = "event/chat/system"
    cosmic_signature: str | None = None
    importance: float = 0.5
    recall_count: int = 0
    last_recalled: datetime | None = None


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
    emotion_intensity: dict[str, float]
    emotion_tag: list[str]
    emotion_shift_trace: list[dict[str, Any]]
    cognitive_reflection: str = ""
    psyche_evolution: dict[str, Any] = field(
        default_factory=lambda: {"pre_state": "", "post_state": "", "growth_vector": []}
    )
    overlapping_memories: list[str] = field(default_factory=list)
    cosmic_signature: str = ""
    recall_count: int = 0
    importance: float = 0.5
    last_recalled: datetime | None = None


class InfinityMemorySystem:
    """Manage creation, storage, and recall of infinity memories."""

    def __init__(self, db_path: str | Path = "infinity_memory.db") -> None:
        self.db_path = str(db_path)
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._ensure_schema()
        self.memory_db: dict[str, InfinityMemory] = {}
        self.emotion_nexus = EmotionGraph()
        self.cognito_reflector = ReflectiveAI()
        self.quantum_tagger = QuantumEmotionTagger()
        self._load_from_storage()

    def create_memory(self, content: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        memory_id = str(uuid.uuid4())
        memory = InfinityMemory(
            id=memory_id,
            content=content,
            timestamp=datetime.now(UTC),
            emotional_spectrum=EmotionalSpectrum(),
            emotion_intensity={},
            emotion_tag=[],
            emotion_shift_trace=[],
        )
        memory = self.quantum_tagger.analyze_emotions(memory)
        self._update_emotional_spectrum(memory)
        memory.cosmic_signature = self._generate_cosmic_signature(memory, context)
        memory.psyche_evolution["growth_vector"] = self._calculate_growth_vector(memory)
        memory.cognitive_reflection = self.cognito_reflector.generate_reflection(
            memory.content, related_topics=memory.emotion_tag
        )
        self.memory_db[memory_id] = memory
        self._persist_memory(memory, context or {})
        self._update_overlapping_memories(memory_id, memory)
        return {
            "memory_id": memory_id,
            "cosmic_signature": memory.cosmic_signature,
            "emotional_profile": memory.emotion_intensity,
        }

    def recall_memory(
        self, query: str, emotion_filter: str | None = None, limit: int = 5
    ) -> list[InfinityMemory]:
        query_vector = self._convert_to_cosmic_vector(query)
        candidates: list[tuple[InfinityMemory, float]] = []
        for memory in self.memory_db.values():
            relevance = self._calculate_relevance(memory, query_vector)
            if emotion_filter and memory.emotion_intensity.get(emotion_filter, 0.0) < 0.5:
                continue
            candidates.append((memory, relevance))
        ranked = sorted(candidates, key=lambda item: item[1], reverse=True)[:limit]
        results: list[InfinityMemory] = []
        for memory, _ in ranked:
            memory.recall_count += 1
            memory.last_recalled = datetime.now(UTC)
            memory.psyche_evolution["growth_vector"] = self._calculate_growth_vector(memory)
            memory.importance = self._calculate_new_importance(memory)
            self._update_memory_stats(memory)
            results.append(memory)
        return results

    def _convert_to_cosmic_vector(self, text: str) -> dict[str, float]:
        tokens = [token for token in text.lower().split() if token]
        counts = Counter(tokens)
        total = float(sum(counts.values())) or 1.0
        return {token: freq / total for token, freq in counts.items()}

    def _calculate_relevance(self, memory: InfinityMemory, query_vector: dict[str, float]) -> float:
        content_vector = self._convert_to_cosmic_vector(memory.content)
        score = sum(
            content_vector.get(token, 0.0) * weight for token, weight in query_vector.items()
        )
        emotion_boost = sum(memory.emotion_intensity.values()) / max(
            len(memory.emotion_intensity) or 1, 1
        )
        return round(score + emotion_boost * 0.1, 3)

    def _generate_cosmic_signature(
        self, memory: InfinityMemory, context: dict[str, Any] | None
    ) -> str:
        context_seed = "|".join(f"{key}:{value}" for key, value in sorted((context or {}).items()))
        payload = (
            f"{memory.content}|{memory.emotion_tag}|{context_seed}|{memory.timestamp.isoformat()}"
        )
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
        return f"cosmic::{memory.timestamp.year}::{digest}"

    def _calculate_growth_vector(self, memory: InfinityMemory) -> list[float]:
        base = sum(memory.emotion_intensity.values())
        diversity = len(memory.emotion_intensity)
        return [round(base, 3), round(diversity / 10.0, 3), round(memory.recall_count / 5.0, 3)]

    def _update_overlapping_memories(self, memory_id: str, memory: InfinityMemory) -> None:
        overlaps = self.emotion_nexus.add_node(
            memory_id, memory.emotion_intensity, memory.timestamp
        )
        memory.overlapping_memories.extend(overlaps)
        self._update_overlap_field(memory)

    def _calculate_new_importance(self, memory: InfinityMemory) -> float:
        base = 0.5 + 0.05 * memory.recall_count
        freshness = max(0.0, 1.0 - (datetime.now(UTC) - memory.timestamp).total_seconds() / 86400.0)
        return round(min(1.0, base + freshness * 0.3), 3)

    def _update_emotional_spectrum(self, memory: InfinityMemory) -> None:
        spectrum_data = {
            field: memory.emotion_intensity.get(field, 0.0)
            for field in EmotionalSpectrum.__annotations__
        }
        memory.emotional_spectrum = EmotionalSpectrum(**spectrum_data)

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------
    def _ensure_schema(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS infinity_memory (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                tags TEXT NOT NULL,
                intensities TEXT NOT NULL,
                reflection TEXT,
                cosmic_signature TEXT,
                context TEXT,
                emotion_shift_trace TEXT,
                overlapping TEXT,
                recall_count INTEGER DEFAULT 0,
                importance REAL DEFAULT 0.5,
                last_recalled TEXT
            )
            """
        )
        self.connection.commit()

    def _persist_memory(self, memory: InfinityMemory, context: dict[str, Any]) -> None:
        payload = {
            "id": memory.id,
            "content": memory.content,
            "timestamp": memory.timestamp.isoformat(),
            "tags": json.dumps(memory.emotion_tag, ensure_ascii=False),
            "intensities": json.dumps(memory.emotion_intensity, ensure_ascii=False),
            "reflection": memory.cognitive_reflection,
            "cosmic_signature": memory.cosmic_signature,
            "context": json.dumps(context, ensure_ascii=False),
            "emotion_shift_trace": json.dumps(
                self._serialise_shift_trace(memory.emotion_shift_trace), ensure_ascii=False
            ),
            "overlapping": json.dumps(memory.overlapping_memories, ensure_ascii=False),
            "recall_count": memory.recall_count,
            "importance": memory.importance,
            "last_recalled": memory.last_recalled.isoformat() if memory.last_recalled else None,
        }
        self.connection.execute(
            """
            INSERT OR REPLACE INTO infinity_memory (
                id, content, timestamp, tags, intensities, reflection, cosmic_signature,
                context, emotion_shift_trace, overlapping, recall_count, importance, last_recalled
            ) VALUES (
                :id, :content, :timestamp, :tags, :intensities, :reflection, :cosmic_signature,
                :context, :emotion_shift_trace, :overlapping, :recall_count, :importance, :last_recalled
            )
            """,
            payload,
        )
        self.connection.commit()

    def _update_memory_stats(self, memory: InfinityMemory) -> None:
        self.connection.execute(
            """
            UPDATE infinity_memory
            SET recall_count = ?, importance = ?, last_recalled = ?, overlapping = ?
            WHERE id = ?
            """,
            (
                memory.recall_count,
                memory.importance,
                memory.last_recalled.isoformat() if memory.last_recalled else None,
                json.dumps(memory.overlapping_memories, ensure_ascii=False),
                memory.id,
            ),
        )
        self.connection.commit()

    def _update_overlap_field(self, memory: InfinityMemory) -> None:
        self.connection.execute(
            "UPDATE infinity_memory SET overlapping = ? WHERE id = ?",
            (json.dumps(memory.overlapping_memories, ensure_ascii=False), memory.id),
        )
        self.connection.commit()

    def _load_from_storage(self) -> None:
        cursor = self.connection.execute("SELECT * FROM infinity_memory")
        rows = cursor.fetchall()
        for row in rows:
            memory = self._row_to_memory(row)
            self.memory_db[memory.id] = memory
            # rebuild emotional graph for similarity tracking
            self.emotion_nexus.add_node(memory.id, memory.emotion_intensity, memory.timestamp)

    def _row_to_memory(self, row: sqlite3.Row) -> InfinityMemory:
        tags = json.loads(row["tags"])
        intensities = json.loads(row["intensities"])
        shift_trace = self._deserialise_shift_trace(json.loads(row["emotion_shift_trace"]))
        overlapping = json.loads(row["overlapping"])
        memory = InfinityMemory(
            id=row["id"],
            content=row["content"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            emotional_spectrum=EmotionalSpectrum(),
            emotion_intensity=intensities,
            emotion_tag=tags,
            emotion_shift_trace=shift_trace,
            cognitive_reflection=row["reflection"] or "",
            overlapping_memories=overlapping,
            cosmic_signature=row["cosmic_signature"] or "",
        )
        memory.recall_count = row["recall_count"]
        memory.importance = row["importance"]
        memory.last_recalled = (
            datetime.fromisoformat(row["last_recalled"]) if row["last_recalled"] else None
        )
        memory.psyche_evolution["growth_vector"] = self._calculate_growth_vector(memory)
        return memory

    def _serialise_shift_trace(self, trace: list[dict[str, Any]]) -> list[dict[str, Any]]:
        serialised: list[dict[str, Any]] = []
        for entry in trace:
            data = dict(entry)
            timestamp = data.get("timestamp")
            if isinstance(timestamp, datetime):
                data["timestamp"] = timestamp.isoformat()
            serialised.append(data)
        return serialised

    def _deserialise_shift_trace(self, trace: list[dict[str, Any]]) -> list[dict[str, Any]]:
        restored: list[dict[str, Any]] = []
        for entry in trace:
            data = dict(entry)
            timestamp = data.get("timestamp")
            if isinstance(timestamp, str):
                try:
                    data["timestamp"] = datetime.fromisoformat(timestamp)
                except ValueError:
                    data["timestamp"] = datetime.now(UTC)
            restored.append(data)
        return restored

    def close(self) -> None:
        self.connection.close()

    def __del__(self) -> None:  # pragma: no cover - defensive cleanup
        try:
            self.close()
        except Exception:
            pass

    def export_ledger(self) -> list[MemoryItem]:
        ledger: list[MemoryItem] = []
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

    def list_memories(self) -> list[InfinityMemory]:
        return list(self.memory_db.values())

    def __len__(self) -> int:  # pragma: no cover - trivial helper
        return len(self.memory_db)
