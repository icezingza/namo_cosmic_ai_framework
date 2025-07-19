# api_integration/github_mcp_api.py

from fastapi import APIRouter
from inter_ai_comms.github_mcp_adapter import GitHubMCPAdapter
from core_modules.emotional_core import EmotionalCore

router = APIRouter()

@router.post("/github-mcp/sync")
def sync_github_commits():
    adapter = GitHubMCPAdapter()
    commits = adapter.get_commits()
    core = EmotionalCore()
    results = [core.analyze_sentiment(msg) for msg in commits]
    return {"commit_emotions": results}
