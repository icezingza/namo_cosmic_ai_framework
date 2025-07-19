from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, Any

# Universal schema (auto accept all fields)
class UniversalInput(BaseModel):
    data: Optional[Any] = None

app = FastAPI(title="NaMo Cosmic AI Framework")

@app.post("/universal-endpoint")
async def universal_api(input: UniversalInput):
    return {"status": "ok", "data_received": input.dict()}

# รวม routers เดิมทั้งหมด
from api_integration.ai_communication_api import router as ai_router
from api_integration.multiverse_sync_api import router as multiverse_router
from api_integration.github_mcp_api import router as github_mcp_router
from api_integration.external_llm_api import router as llm_router

app.include_router(ai_router, prefix="/ai")
app.include_router(multiverse_router, prefix="/multiverse")
app.include_router(github_mcp_router, prefix="/github")
app.include_router(llm_router, prefix="/llm")
