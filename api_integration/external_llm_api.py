from fastapi import APIRouter, HTTPException
from core_modules.memory import FirestoreMemory
from typing import List, Dict, Any
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# --- Vertex AI Configuration ---
PROJECT_ID = "arctic-signer-471822-i8"
LOCATION = "asia-southeast1"
MODEL_NAME = "gemini-1.5-pro-preview-0409"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)
# -----------------------------

router = APIRouter()

def format_history_for_gemini(history: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Maps the role from our Firestore format ('user'/'ai') 
    to what the Gemini API expects ('user'/'model').
    """
    formatted_messages = []
    for msg in history:
        role = msg.get("role")
        content = msg.get("content")
        if role == "ai":
            # Gemini expects the model's role to be 'model'
            formatted_messages.append({"role": "model", "content": content})
        elif role == "user":
            formatted_messages.append({"role": "user", "content": content})
    return formatted_messages

# NOTE: The path is kept as /ollama/chat to avoid breaking the existing Custom GPT Action.
# In the future, it would be good to rename this to /gemini/chat.
@router.post("/ollama/chat")
def chat_with_gemini_and_memory(prompt: str, session_id: str):
    """
    Handles a chat prompt using Gemini 1.5 Pro on Vertex AI,
    maintaining conversation history using Firestore.
    """
    try:
        # 1. Initialize memory
        memory = FirestoreMemory(project_id='namo-legacy-identity')

        # 2. Save the user's new message to Firestore
        memory.add_message(session_id=session_id, role="user", content=prompt)

        # 3. Retrieve the conversation history
        # We get the last 20 messages to keep the context window reasonable
        history = memory.get_messages(session_id=session_id, limit=20)
        
        # 4. Format history for the Gemini API
        # The history from Firestore already includes the new prompt we just added.
        messages_for_gemini = format_history_for_gemini(history)

        # 5. Call the Gemini API
        model = GenerativeModel(MODEL_NAME)
        # The Gemini API expects the history and the new prompt to be combined.
        # The last message in our list is the new user prompt.
        response = model.generate_content(messages_for_gemini)
        
        assistant_message = response.text

        # 6. Save the assistant's reply to Firestore
        memory.add_message(session_id=session_id, role="ai", content=assistant_message)

        # 7. Return the final response in a consistent format
        return {"response": assistant_message, "model_used": MODEL_NAME}

    except Exception as e:
        # Broad exception handling for any errors from Vertex AI or other issues.
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
