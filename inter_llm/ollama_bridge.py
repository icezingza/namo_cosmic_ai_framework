# inter_llm/ollama_bridge.py

import requests

class OllamaBridge:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def query(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
