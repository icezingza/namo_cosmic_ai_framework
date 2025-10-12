import asyncio

from core.memory_system import InfinityMemorySystem


def test_create_memory_event_loop():
    memory_system = InfinityMemorySystem()
    result = asyncio.run(memory_system.create_memory("Test memory", emotional_context={"joy": 0.8}))
    assert "memory_id" in result
    assert result["reliability_score"] <= 1.0
