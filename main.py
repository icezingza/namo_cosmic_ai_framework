from gcp_integration import gcp_status_check
import os
import firebase_admin
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, Any, List, Dict

# --- Firebase Admin SDK Initialization ---
# Ensure this runs only once at startup.
project_id = os.getenv("GCP_PROJECT")
if project_id:
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(options={'projectId': project_id})
    print(f"[NaMo GCP] Firebase App initialized for project: {project_id}")
else:
    print("[NaMo GCP] WARNING: GCP_PROJECT environment variable not set. Firebase not initialized.")
# ----------------------------------------

# --- Dynamic Server URL for OpenAPI Spec ---
# This allows the OpenAPI documentation to correctly point to our public ngrok URL
server_url = os.getenv("SERVER_URL", "http://localhost:8000")
servers = [{
    "url": server_url,
    "description": "Main production server"
}]
# ------------------------------------------

# Universal schema (auto accept all fields)
class UniversalInput(BaseModel):
    data: Optional[Any] = None

# Pass the servers list to the FastAPI constructor
app = FastAPI(
    title="NaMo Cosmic AI Framework",
    servers=servers
)

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

if __name__ == "__main__":
    # This part seems to be for a different execution context, 
    # as we are running the app with uvicorn directly.
    # init_gcp_credentials("PATH/TO/namo-legacy-identity-f6acd4af5ea0.json", "namo-legacy-identity")
    # print("[GCP Status]", gcp_status_check())
    print(f"FastAPI server starting. OpenAPI spec will use server URL: {server_url}")
