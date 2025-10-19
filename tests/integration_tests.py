import asyncio

from core.memory_system import InfinityMemorySystem


def test_recall_after_create():
    memory_system = InfinityMemorySystem()
    asyncio.run(
        memory_system.create_memory(
            "Cross cultural collaboration story", emotional_context={"joy": 0.7}
        )
    )
    memories = asyncio.run(memory_system.recall_memories("collaboration"))
    assert memories
    assert any("collaboration" in memory.content for memory in memories)
