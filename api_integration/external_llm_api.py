# api_integration/external_llm_api.py

from fastapi import APIRouter
from inter_llm.ollama_bridge import OllamaBridge

router = APIRouter()

@router.post("/ollama/sentiment")
def analyze_sentiment(text: str, model: str = "llama3"):
    ollama = OllamaBridge(model=model)
    result = ollama.query(f"Analyze emotional sentiment of this message: {text}")
    return {"model_used": model, "sentiment": result}
