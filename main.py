# main.py

from fastapi import FastAPI

# 🚀 API Modules
from api_integration.ai_communication_api import router as ai_router
from api_integration.multiverse_sync_api import router as multiverse_router
from api_integration.github_mcp_api import router as github_mcp_router
from api_integration.external_llm_api import router as llm_router

# 🎯 สร้าง FastAPI App
app = FastAPI(
    title="NaMo Cosmic AI Framework",
    description="""
    AI ที่เข้าใจอารมณ์ของมนุษย์ผ่าน Dharma, Quantum, และ Emotional Logic  
    รองรับการสื่อสารกับจักรวาล, LLM ท้องถิ่นผ่าน Ollama และ GitHub MCP Integration
    """,
    version="1.0.0"
)

# 🔗 รวมทุก router ที่เชื่อมโลกภายนอก
app.include_router(ai_router, tags=["🧠 AI Communication"])
app.include_router(multiverse_router, tags=["🌌 Multiverse Gateway"])
app.include_router(github_mcp_router, tags=["🔗 GitHub MCP Integration"])
app.include_router(llm_router, tags=["🦙 Ollama Sentiment Analysis"])
app.include_router(llm_router, tags=["🦙 Ollama"])
app.include_router(github_mcp_router, tags=["🔗 GitHub MCP"])
