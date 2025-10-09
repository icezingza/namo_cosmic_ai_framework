"""Command line interface for interacting with the Infinity AI framework."""

from __future__ import annotations

import argparse
import asyncio
from typing import Any

from core import InfinityMemorySystem


async def create_and_recall(memory_system: InfinityMemorySystem, content: str, query: str) -> None:
    await memory_system.create_memory(content)
    memories = await memory_system.recall_memories(query)
    for memory in memories:
        print(memory.content)


def main(argv: Any | None = None) -> None:
    parser = argparse.ArgumentParser(description="Infinity AI CLI")
    parser.add_argument("content", help="Content to store as a memory")
    parser.add_argument("query", help="Query string for recall")
    args = parser.parse_args(argv)

    memory_system = InfinityMemorySystem()
    asyncio.run(create_and_recall(memory_system, args.content, args.query))


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
