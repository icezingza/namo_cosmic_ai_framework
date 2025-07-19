from fastapi import APIRouter
import requests

router = APIRouter()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # หรือ lfm2-1.2b ที่พี่ติดตั้ง

@router.post("/ollama/chat")
def ollama_chat(prompt: str):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()
