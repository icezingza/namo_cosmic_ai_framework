# api_integration/external_llm_api.py

from fastapi import APIRouter
from inter_llm.ollama_bridge import OllamaBridge

router = APIRouter()

@router.post("/ollama/sentiment")
def analyze_with_ollama(text: str):
    ollama = OllamaBridge(model="llama3")
    result = ollama.query(f"Analyze emotional sentiment: '{text}'")
    return {"ollama_sentiment": result}
