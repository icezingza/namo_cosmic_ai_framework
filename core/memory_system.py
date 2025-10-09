"""Advanced asynchronous memory system for the Infinity AI framework."""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from prometheus_client import Counter, Gauge, Histogram


LOGGER = logging.getLogger(__name__)


MEMORY_CREATED = Counter(
    "infinity_memory_created_total", "Total memories created",
)
MEMORY_RECALLED = Counter(
    "infinity_memory_recalled_total", "Total memory recalls",
)
MEMORY_OPERATION_DURATION = Histogram(
    "infinity_memory_operation_duration_seconds", "Memory operation duration",
)
ACTIVE_MEMORIES = Gauge(
    "infinity_active_memories", "Number of active memories",
)


class MemoryType(Enum):
    """Enumeration of memory types supported by the system."""

    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    EMOTIONAL = "emotional"
    TEMPORAL = "temporal"
    COSMIC = "cosmic"
    PROCEDURAL = "procedural"


@dataclass
class EmotionalSpectrum:
    """Representation of emotional intensity across a spectrum."""

    joy: float = 0.0
    sorrow: float = 0.0
    rage: float = 0.0
    serenity: float = 0.0
    longing: float = 0.0
    betrayal: float = 0.0
    hope: float = 0.0
    nostalgia: float = 0.0
    curiosity: float = 0.0
    awe: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        """Return a dictionary with only active emotions."""

        return {k: v for k, v in asdict(self).items() if v > 0.0}

    def get_dominant_emotion(self) -> Tuple[str, float]:
        """Return the dominant emotion and its intensity."""

        emotions = asdict(self)
        if not emotions:
            return "neutral", 0.0
        dominant = max(emotions.items(), key=lambda item: item[1])
        return dominant[0], dominant[1]


@dataclass
class MemoryMetadata:
    """Metadata associated with an :class:`InfinityMemory`."""

    timeline_id: str = "earth-616"
    importance: float = 50.0
    recall_count: int = 0
    last_recalled: Optional[datetime] = None
    cosmic_signature: str = ""
    conflict_group: Optional[str] = None
    source: str = "user_input"
    reliability_score: float = 0.8
    access_frequency: float = 1.0
    last_updated: datetime = field(default_factory=datetime.now)


class InfinityMemory:
    """Rich representation of a single memory entity."""

    def __init__(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.SEMANTIC,
        emotional_spectrum: Optional[EmotionalSpectrum] = None,
        metadata: Optional[MemoryMetadata] = None,
        embedding: Optional[np.ndarray] = None,
    ) -> None:
        self.id = str(uuid.uuid4())
        self.content = content
        self.memory_type = memory_type
        self.timestamp = datetime.now()
        self.emotional_spectrum = emotional_spectrum or EmotionalSpectrum()
        self.metadata = metadata or MemoryMetadata()
        self.embedding = embedding

        self.emotion_intensity: Dict[str, float] = {}
        self.emotion_tags: List[str] = []
        self.emotion_shift_trace: List[Dict[str, Any]] = []
        self.overlapping_memories: List[str] = []
        self.cognitive_reflection = ""
        self.related_concepts: List[str] = []
        self.psyche_evolution = {
            "pre_state": "",
            "post_state": "",
            "growth_vector": [],
            "learning_points": [],
        }

        self._cached_embedding: Optional[np.ndarray] = None
        self._last_accessed: datetime = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the memory to a JSON-compatible dictionary."""

        data = {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "timestamp": self.timestamp.isoformat(),
            "emotional_spectrum": self.emotional_spectrum.to_dict(),
            "metadata": asdict(self.metadata),
            "emotion_intensity": self.emotion_intensity,
            "emotion_tags": self.emotion_tags,
            "psyche_evolution": self.psyche_evolution,
            "cognitive_reflection": self.cognitive_reflection,
            "related_concepts": self.related_concepts,
            "embedding": self.embedding.tolist() if self.embedding is not None else None,
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InfinityMemory":
        """Construct an :class:`InfinityMemory` from a dictionary."""

        memory = cls(
            content=data["content"],
            memory_type=MemoryType(data["memory_type"]),
        )
        memory.id = data["id"]
        memory.timestamp = datetime.fromisoformat(data["timestamp"])
        emotional_data = data.get("emotional_spectrum", {})
        memory.emotional_spectrum = EmotionalSpectrum(**emotional_data)
        metadata_data = data.get("metadata", {})
        metadata_data.setdefault("last_updated", datetime.now().isoformat())
        if isinstance(metadata_data.get("last_updated"), str):
            metadata_data["last_updated"] = datetime.fromisoformat(metadata_data["last_updated"])
        memory.metadata = MemoryMetadata(**metadata_data)
        memory.emotion_intensity = data.get("emotion_intensity", {})
        memory.emotion_tags = data.get("emotion_tags", [])
        memory.psyche_evolution = data.get("psyche_evolution", {})
        memory.cognitive_reflection = data.get("cognitive_reflection", "")
        memory.related_concepts = data.get("related_concepts", [])
        embedding_data = data.get("embedding")
        if embedding_data is not None:
            memory.embedding = np.array(embedding_data)
        return memory

    def update_access_time(self) -> None:
        """Update access metadata when the memory is recalled."""

        self._last_accessed = datetime.now()
        self.metadata.last_recalled = self._last_accessed
        self.metadata.recall_count += 1
        self.metadata.last_updated = datetime.now()


class QuantumEmotionTagger:
    """Toy emotion analysis engine supporting asynchronous execution."""

    async def analyze_emotions_async(
        self, memory: InfinityMemory, emotional_context: Optional[Dict[str, float]]
    ) -> InfinityMemory:
        context = emotional_context or {}
        intensities = {k: float(v) for k, v in context.items() if isinstance(v, (int, float))}
        dominant = max(intensities.items(), key=lambda item: item[1], default=("neutral", 0.0))
        memory.emotion_intensity = intensities
        memory.emotion_tags = [emotion for emotion, value in intensities.items() if value > 0.5]
        memory.emotional_spectrum = EmotionalSpectrum(**{
            key: intensities.get(key, 0.0)
            for key in EmotionalSpectrum().__dict__.keys()
        })
        memory.cognitive_reflection = f"Dominant emotion detected: {dominant[0]} ({dominant[1]:.2f})"
        return memory


class MemoryConflictResolver:
    """Simplified resolver that aggregates conflicting memories."""

    async def resolve_conflicts_async(self, memories: List[InfinityMemory]) -> Dict[str, Any]:
        if not memories:
            return {"status": "no_conflicts", "details": []}
        sorted_memories = sorted(
            memories,
            key=lambda mem: mem.metadata.reliability_score,
            reverse=True,
        )
        champion = sorted_memories[0]
        conflicts = [mem.id for mem in sorted_memories[1:]]
        return {
            "status": "resolved",
            "champion_memory": champion.id,
            "conflicts": conflicts,
            "confidence": champion.metadata.reliability_score,
        }


class MemoryReliabilityEngine:
    """Compute reliability scores for memories."""

    async def calculate_reliability_score_async(self, memory: InfinityMemory) -> float:
        base = 0.5 + min(len(memory.content) / 500.0, 0.4)
        emotion_bonus = sum(memory.emotion_intensity.values()) / 10.0
        return min(base + emotion_bonus, 1.0)


class InMemoryStorageBackend:
    """Default asynchronous storage backend based on an in-memory dictionary."""

    def __init__(self) -> None:
        self._memories: Dict[str, Dict[str, Any]] = {}

    async def store_memory_async(self, memory: Dict[str, Any]) -> None:
        self._memories[memory["id"]] = memory

    async def update_memory_async(self, memory: Dict[str, Any]) -> None:
        self._memories[memory["id"]] = memory

    async def get_memory_async(self, memory_id: str) -> Optional[Dict[str, Any]]:
        return self._memories.get(memory_id)

    async def search_memories_async(
        self,
        query: str,
        filters: Dict[str, Any],
        limit: int,
    ) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        lowered = query.lower()
        for memory in self._memories.values():
            if lowered in memory["content"].lower():
                results.append(memory)
        return results[:limit]

    async def all_memories_async(self) -> List[Dict[str, Any]]:
        return list(self._memories.values())


class InfinityMemorySystem:
    """Coordinates memory creation, storage, and recall."""

    def __init__(self, storage_backend: Any = None, config: Optional[Dict[str, Any]] = None) -> None:
        self.storage = storage_backend or self._create_default_storage()
        self.emotion_tagger = QuantumEmotionTagger()
        self.conflict_resolver = MemoryConflictResolver()
        self.reliability_engine = MemoryReliabilityEngine()
        self.scaling_manager = MemoryScalingManager()
        self.config = config or {}
        self.cache: Dict[str, Any] = {}
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.logger = LOGGER
        self.metrics = {
            "active_memories": 0,
            "cache_hit_rate": 0.0,
            "avg_processing_time": 0.0,
        }
        logging.basicConfig(level=logging.INFO)

    def _create_default_storage(self) -> InMemoryStorageBackend:
        return InMemoryStorageBackend()

    async def create_memory(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None,
        emotional_context: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        start_time = datetime.now()
        ACTIVE_MEMORIES.inc()
        try:
            memory = InfinityMemory(content=content)
            memory = await self.emotion_tagger.analyze_emotions_async(memory, emotional_context)
            reliability_score = await self.reliability_engine.calculate_reliability_score_async(memory)
            memory.metadata.reliability_score = reliability_score
            memory.metadata.importance = reliability_score * 100
            memory.metadata.cosmic_signature = self._generate_cosmic_signature(memory)
            memory.embedding = await self._compute_embedding_async(memory.content)
            memory_data = memory.to_dict()
            await self.storage.store_memory_async(memory_data)
            self.cache[memory.id] = memory
            self.metrics["active_memories"] = len(self.cache)
            await self._update_overlapping_memories_async(memory)
            MEMORY_CREATED.inc()
            processing_time = (datetime.now() - start_time).total_seconds()
            MEMORY_OPERATION_DURATION.observe(processing_time)
            return {
                "memory_id": memory.id,
                "reliability_score": reliability_score,
                "emotional_profile": memory.emotion_intensity,
                "cosmic_signature": memory.metadata.cosmic_signature,
                "processing_time": processing_time,
            }
        except Exception as exc:  # pragma: no cover - defensive logging
            self.logger.error("Error creating memory: %s", exc)
            raise
        finally:
            ACTIVE_MEMORIES.dec()

    async def recall_memories(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        use_cache: bool = True,
    ) -> List[InfinityMemory]:
        start_time = datetime.now()
        filters = filters or {}
        try:
            cache_key = json.dumps({"query": query, "filters": filters}, sort_keys=True)
            if use_cache and cache_key in self.cache:
                cached_result = self.cache[cache_key]
                if datetime.now() - cached_result["timestamp"] < timedelta(minutes=5):
                    self.metrics["cache_hit_rate"] = (
                        self.metrics.get("cache_hit_rate", 0.0) * 0.9 + 0.1
                    )
                    return cached_result["memories"]

            raw_results = await self.storage.search_memories_async(query=query, filters=filters, limit=limit * 3)
            memories = await self._convert_to_memory_objects_async(raw_results)
            filtered_memories = await self._apply_advanced_filters_async(memories, filters)
            for memory in filtered_memories[:limit]:
                memory.update_access_time()
                await self._update_memory_in_storage_async(memory)
            if use_cache:
                self.cache[cache_key] = {
                    "memories": filtered_memories[:limit],
                    "timestamp": datetime.now(),
                }
            MEMORY_RECALLED.inc()
            processing_time = (datetime.now() - start_time).total_seconds()
            MEMORY_OPERATION_DURATION.observe(processing_time)
            self.metrics["avg_processing_time"] = (
                self.metrics.get("avg_processing_time", 0.0) * 0.9 + processing_time * 0.1
            )
            return filtered_memories[:limit]
        except Exception as exc:  # pragma: no cover - defensive logging
            self.logger.error("Error recalling memories: %s", exc)
            raise

    async def resolve_memory_conflicts(self, memory_ids: List[str]) -> Dict[str, Any]:
        memories_data = await asyncio.gather(
            *[self.storage.get_memory_async(memory_id) for memory_id in memory_ids]
        )
        memory_objects = [InfinityMemory.from_dict(data) for data in memories_data if data]
        return await self.conflict_resolver.resolve_conflicts_async(memory_objects)

    async def scale_system(self, target_capacity: int) -> Dict[str, Any]:
        return await self.scaling_manager.scale_memory_system(
            current_load=self.metrics["active_memories"],
            target_capacity=target_capacity,
            system_metrics=self.metrics,
        )

    def get_system_metrics(self) -> Dict[str, Any]:
        return {
            **self.metrics,
            "cache_size": len(self.cache),
            "timestamp": datetime.now().isoformat(),
        }

    async def _compute_embedding_async(self, content: str) -> np.ndarray:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._compute_embedding_sync, content)

    def _compute_embedding_sync(self, content: str) -> np.ndarray:
        words = content.split()
        embedding = np.zeros(384)
        for word in words:
            word_hash = hash(word) % 1000
            embedding[word_hash % 384] += 1
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        self._cached_embedding = embedding
        return embedding

    async def _convert_to_memory_objects_async(self, results: List[Dict[str, Any]]) -> List[InfinityMemory]:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(self.executor, InfinityMemory.from_dict, result)
            for result in results
        ]
        return await asyncio.gather(*tasks)

    async def _apply_advanced_filters_async(
        self, memories: List[InfinityMemory], filters: Dict[str, Any]
    ) -> List[InfinityMemory]:
        min_reliability = float(filters.get("min_reliability", 0))
        required_emotions = set(filters.get("emotions", []))
        time_range = filters.get("time_range")
        now = datetime.now()
        filtered: List[InfinityMemory] = []
        for memory in memories:
            if memory.metadata.reliability_score < min_reliability:
                continue
            if required_emotions and not required_emotions.intersection(memory.emotion_tags):
                continue
            if time_range == "last_30_days" and (now - memory.timestamp).days > 30:
                continue
            filtered.append(memory)
        return filtered

    async def _update_memory_in_storage_async(self, memory: InfinityMemory) -> None:
        await self.storage.update_memory_async(memory.to_dict())

    async def _update_overlapping_memories_async(self, memory: InfinityMemory) -> None:
        stored_memories = await self.storage.all_memories_async()
        overlaps: List[str] = []
        for stored in stored_memories:
            if stored["id"] == memory.id:
                continue
            if stored.get("memory_type") == memory.memory_type.value:
                overlaps.append(stored["id"])
        memory.overlapping_memories = overlaps

    def _generate_cosmic_signature(self, memory: InfinityMemory) -> str:
        timestamp = int(memory.timestamp.timestamp())
        return f"COSMIC-{memory.memory_type.value.upper()}-{timestamp}-{memory.id[:8]}"


class MemoryScalingManager:
    """Decide how to scale the memory system."""

    def __init__(self) -> None:
        self.scaling_strategies = {
            "horizontal": self._scale_horizontally,
            "vertical": self._scale_vertically,
            "sharding": self._scale_with_sharding,
        }

    async def scale_memory_system(
        self,
        current_load: int,
        target_capacity: int,
        system_metrics: Dict[str, Any],
    ) -> Dict[str, Any]:
        decision = self._analyze_scaling_needs(current_load, target_capacity, system_metrics)
        if not decision["needs_scaling"]:
            return {"status": "no_scaling_needed", "message": "System capacity is sufficient"}
        strategy = decision["recommended_strategy"]
        return await self.scaling_strategies[strategy](decision)

    def _analyze_scaling_needs(
        self, current_load: int, target_capacity: int, metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        capacity_ratio = current_load / target_capacity if target_capacity else 0
        performance_degradation = metrics.get("avg_processing_time", 0) > 1.0
        needs_scaling = capacity_ratio > 0.8 or performance_degradation
        return {
            "needs_scaling": needs_scaling,
            "current_load": current_load,
            "target_capacity": target_capacity,
            "capacity_ratio": capacity_ratio,
            "performance_issue": performance_degradation,
            "recommended_strategy": self._select_scaling_strategy(capacity_ratio, performance_degradation),
        }

    def _select_scaling_strategy(self, capacity_ratio: float, performance_issue: bool) -> str:
        if capacity_ratio > 0.9 or performance_issue:
            return "sharding"
        if capacity_ratio > 0.7:
            return "horizontal"
        return "vertical"

    async def _scale_horizontally(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        return {"strategy": "horizontal", "status": "implemented", "details": decision}

    async def _scale_vertically(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        return {"strategy": "vertical", "status": "implemented", "details": decision}

    async def _scale_with_sharding(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        return {"strategy": "sharding", "status": "implemented", "details": decision}


__all__ = [
    "InfinityMemory",
    "InfinityMemorySystem",
    "MemoryType",
    "MemoryMetadata",
    "EmotionalSpectrum",
    "MemoryScalingManager",
]
