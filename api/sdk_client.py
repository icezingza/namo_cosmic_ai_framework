"""SDK client for programmatic access."""

from __future__ import annotations

from typing import Any

from core import InfinityMemorySystem


class InfinityAIFramework:
    def __init__(self, config_path: str | None = None, api_key: str | None = None) -> None:
        self.config_path = config_path
        self.api_key = api_key
        self._memory_system = InfinityMemorySystem()

    @property
    def memory(self) -> MemoryClient:
        return MemoryClient(self._memory_system)


class MemoryClient:
    def __init__(self, memory_system: InfinityMemorySystem) -> None:
        self._memory_system = memory_system

    async def create(
        self,
        content: str,
        emotional_context: dict[str, float] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self._memory_system.create_memory(content, emotional_context=emotional_context)

    async def recall(
        self,
        query: str,
        filters: dict[str, Any] | None = None,
        limit: int = 5,
    ) -> list[Any]:
        return await self._memory_system.recall_memories(query, filters=filters, limit=limit)


__all__ = ["InfinityAIFramework", "MemoryClient"]
