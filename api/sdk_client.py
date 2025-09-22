"""SDK client for programmatic access."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List

from core import InfinityMemorySystem


class InfinityAIFramework:
    def __init__(self, config_path: str | None = None, api_key: str | None = None) -> None:
        self.config_path = config_path
        self.api_key = api_key
        self._memory_system = InfinityMemorySystem()

    @property
    def memory(self) -> "MemoryClient":
        return MemoryClient(self._memory_system)


class MemoryClient:
    def __init__(self, memory_system: InfinityMemorySystem) -> None:
        self._memory_system = memory_system

    async def create(
        self,
        content: str,
        emotional_context: Dict[str, float] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        return await self._memory_system.create_memory(content, emotional_context=emotional_context)

    async def recall(
        self,
        query: str,
        filters: Dict[str, Any] | None = None,
        limit: int = 5,
    ) -> List[Any]:
        return await self._memory_system.recall_memories(query, filters=filters, limit=limit)


__all__ = ["InfinityAIFramework", "MemoryClient"]
