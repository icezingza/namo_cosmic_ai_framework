# main.py

from fastapi import FastAPI

# 🚀 API Modules
from api_integration.ai_communication_api import router as ai_router
from api_integration.multiverse_sync_api import router as multiverse_router
from api_integration.github_mcp_api import router as github_mcp_router
from api_integration.external_llm_api import router as llm_router  # NEW

app = FastAPI(
    title="NaMo Cosmic AI Framework",
    description="AI ที่เข้าใจอารมณ์และเชื่อมโยงกับจักรวาลผ่าน Dharma และ Emotional Analysis",
    version="1.0.0"
)

# 🔗 Register API routers
app.include_router(ai_router)
app.include_router(multiverse_router)
app.include_router(github_mcp_router)
app.include_router(llm_router)  # NEW: เชื่อมกับ Ollama LLM ในเครื่อง
