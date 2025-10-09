import pytest
from unittest.mock import AsyncMock, patch
import numpy as np
from datetime import datetime

from core.memory_system import (
    InfinityMemorySystem,
    InfinityMemory,
    MemoryType,
    EmotionalSpectrum,
    MemoryMetadata,
)


def test_infinity_memory_system_initialization():
    """
    Tests that the InfinityMemorySystem can be initialized.
    """
    try:
        memory_system = InfinityMemorySystem()
        assert memory_system is not None
        assert memory_system.storage is not None
        assert memory_system.emotion_tagger is not None
        assert memory_system.conflict_resolver is not None
        assert memory_system.reliability_engine is not None
    except Exception as e:
        pytest.fail(f"InfinityMemorySystem initialization failed: {e}")


def test_emotional_spectrum():
    """Tests the EmotionalSpectrum dataclass."""
    spectrum = EmotionalSpectrum(joy=0.9, sorrow=0.1, rage=0.0)

    # Test to_dict
    spectrum_dict = spectrum.to_dict()
    assert "joy" in spectrum_dict
    assert "sorrow" in spectrum_dict
    assert "rage" not in spectrum_dict

    # Test get_dominant_emotion
    dominant_emotion, intensity = spectrum.get_dominant_emotion()
    assert dominant_emotion == "joy"
    assert intensity == 0.9

    empty_spectrum = EmotionalSpectrum()
    dominant_emotion, intensity = empty_spectrum.get_dominant_emotion()
    assert dominant_emotion == "neutral"
    assert intensity == 0.0


def test_infinity_memory_to_from_dict():
    """Tests serialization and deserialization of InfinityMemory."""
    mem = InfinityMemory(
        content="Test content",
        memory_type=MemoryType.EPISODIC,
        emotional_spectrum=EmotionalSpectrum(joy=0.8),
        metadata=MemoryMetadata(importance=90.0),
    )
    mem.embedding = np.array([0.1, 0.2, 0.3])

    mem_dict = mem.to_dict()

    assert mem_dict["content"] == "Test content"
    assert mem_dict["memory_type"] == "episodic"
    assert mem_dict["emotional_spectrum"]["joy"] == 0.8
    assert mem_dict["metadata"]["importance"] == 90.0
    assert np.array_equal(np.array(mem_dict["embedding"]), mem.embedding)

    new_mem = InfinityMemory.from_dict(mem_dict)

    assert new_mem.id == mem.id
    assert new_mem.content == mem.content
    assert new_mem.memory_type == mem.memory_type
    assert new_mem.emotional_spectrum.joy == 0.8
    assert new_mem.metadata.importance == 90.0
    assert np.array_equal(new_mem.embedding, mem.embedding)


@pytest.fixture
def memory_system():
    """Fixture for an InfinityMemorySystem with mocked dependencies."""
    with patch("core.memory_system.InMemoryStorageBackend", new_callable=AsyncMock) as mock_storage:
        system = InfinityMemorySystem(storage_backend=mock_storage)

        # Mock dependencies
        system.emotion_tagger = AsyncMock()
        system.conflict_resolver = AsyncMock()
        system.reliability_engine = AsyncMock()
        system.scaling_manager = AsyncMock()

        # Configure mock returns for async methods
        system.emotion_tagger.analyze_emotions_async = AsyncMock(return_value=InfinityMemory("test"))
        system.reliability_engine.calculate_reliability_score_async = AsyncMock(return_value=0.9)
        system._compute_embedding_async = AsyncMock(return_value=np.array([0.1, 0.2, 0.3]))
        system._update_overlapping_memories_async = AsyncMock()

        # Mock storage methods
        system.storage.store_memory_async = AsyncMock()
        system.storage.update_memory_async = AsyncMock()
        system.storage.get_memory_async = AsyncMock()
        system.storage.search_memories_async = AsyncMock(return_value=[])
        system.storage.all_memories_async = AsyncMock(return_value=[])

        yield system


@pytest.mark.asyncio
async def test_create_memory(memory_system):
    """Tests the successful creation of a memory."""
    content = "A new memory about a sunset."
    emotional_context = {"joy": 0.7, "awe": 0.9}

    embedding_val = np.random.rand(384)
    memory_system._compute_embedding_async.return_value = embedding_val

    # Mock emotion tagger to return a memory with the right content
    mock_memory = InfinityMemory(content)
    memory_system.emotion_tagger.analyze_emotions_async.return_value = mock_memory

    result = await memory_system.create_memory(content=content, emotional_context=emotional_context)

    assert "memory_id" in result
    assert result["reliability_score"] == 0.9
    assert "emotional_profile" in result
    assert "cosmic_signature" in result

    memory_system.emotion_tagger.analyze_emotions_async.assert_called_once()
    memory_system.reliability_engine.calculate_reliability_score_async.assert_called_once()
    memory_system.storage.store_memory_async.assert_called_once()

    stored_data = memory_system.storage.store_memory_async.call_args[0][0]
    assert stored_data["content"] == content
    assert np.array_equal(np.array(stored_data["embedding"]), embedding_val)


@pytest.mark.asyncio
async def test_recall_memories_no_results(memory_system):
    """Tests recall when no memories are found."""
    memory_system.storage.search_memories_async.return_value = []

    results = await memory_system.recall_memories("non-existent")

    assert results == []
    memory_system.storage.search_memories_async.assert_called_once()


@pytest.mark.asyncio
async def test_recall_memories_with_results(memory_system):
    """Tests recall with a single matching memory."""
    query = "found"
    mem = InfinityMemory("This should be found.")

    memory_system.storage.search_memories_async.return_value = [mem.to_dict()]

    results = await memory_system.recall_memories(query)

    assert len(results) == 1
    assert results[0].id == mem.id
    memory_system.storage.update_memory_async.assert_called_once()


@pytest.mark.asyncio
async def test_recall_memories_caching(memory_system):
    """Tests that recall results are cached."""
    query = "cached query"
    mem = InfinityMemory("This will be cached.")

    memory_system.storage.search_memories_async.return_value = [mem.to_dict()]

    # First call, should query storage
    await memory_system.recall_memories(query)
    assert memory_system.storage.search_memories_async.call_count == 1

    # Second call, should use cache
    await memory_system.recall_memories(query)
    assert memory_system.storage.search_memories_async.call_count == 1


@pytest.mark.asyncio
async def test_recall_memories_advanced_filter(memory_system):
    """Tests recall with advanced filtering logic."""
    query = "test"
    mem1 = InfinityMemory("Reliable and joyful")
    mem1.metadata.reliability_score = 0.95
    mem1.emotion_tags = ["joy"]

    mem2 = InfinityMemory("Unreliable and joyful")
    mem2.metadata.reliability_score = 0.3
    mem2.emotion_tags = ["joy"]

    mem3 = InfinityMemory("Reliable and sad")
    mem3.metadata.reliability_score = 0.90
    mem3.emotion_tags = ["sorrow"]

    memory_system.storage.search_memories_async.return_value = [
        mem1.to_dict(),
        mem2.to_dict(),
        mem3.to_dict(),
    ]

    # Filter by reliability
    filters = {"min_reliability": 0.8}
    results = await memory_system.recall_memories(query, filters=filters)
    assert len(results) == 2
    assert {m.id for m in results} == {mem1.id, mem3.id}

    # Filter by emotion
    filters = {"emotions": ["joy"]}
    results = await memory_system.recall_memories(query, filters=filters)
    assert len(results) == 2
    assert {m.id for m in results} == {mem1.id, mem2.id}


def test_get_system_metrics(memory_system):
    """Tests the retrieval of system metrics."""
    memory_system.metrics = {"active_memories": 5, "cache_hit_rate": 0.5}
    memory_system.cache = {"a": 1, "b": 2}

    metrics = memory_system.get_system_metrics()

    assert metrics["active_memories"] == 5
    assert metrics["cache_hit_rate"] == 0.5
    assert metrics["cache_size"] == 2
    assert "timestamp" in metrics