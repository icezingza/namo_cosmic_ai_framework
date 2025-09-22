"""REST API for the Infinity AI framework."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from core import InfinityMemorySystem

app = FastAPI(title="Infinity AI Framework")
memory_system = InfinityMemorySystem()


class MemoryRequest(BaseModel):
    content: str
    emotional_context: Dict[str, float] | None = None


@app.post("/memory")
async def create_memory(request: MemoryRequest) -> Dict[str, Any]:
    return await memory_system.create_memory(request.content, emotional_context=request.emotional_context)


@app.get("/memory")
async def recall_memory(query: str) -> Dict[str, Any]:
    memories = await memory_system.recall_memories(query)
    if not memories:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"memories": [memory.to_dict() for memory in memories]}


@app.get("/system/health")
async def system_health() -> Dict[str, Any]:
    return {"status": "ok", "metrics": memory_system.get_system_metrics()}
