from fastapi import APIRouter, HTTPException
from core_modules.memory import FirestoreMemory
from typing import List, Dict, Any
import vertexai
from vertexai.generative_models import Content, GenerativeModel, Part
import os

# --- Vertex AI Configuration ---
# PROJECT_ID is now fetched from environment variables, not hardcoded.
LOCATION = "asia-southeast1"
MODEL_NAME = "gemini-1.5-pro-preview-0409"
# -----------------------------

router = APIRouter()

def format_history_for_gemini(history: List[Dict[str, Any]]) -> List[Content]:
    """
    Maps the role from our Firestore format ('user'/'ai') to the Gemini API format
    and converts each message into a ``Content`` instance.
    """

    formatted_messages: List[Content] = []
    for msg in history:
        role = msg.get("role")
        text = msg.get("content")

        if text is None:
            continue

        text = str(text).strip()
        if not text:
            continue

        if role == "ai":
            role = "model"
        elif role not in {"user", "model"}:
            # Skip messages that do not have a recognized role.
            continue

        formatted_messages.append(Content(role=role, parts=[Part.from_text(text)]))

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
        # 1. Get Project ID from environment
        project_id = os.getenv("GCP_PROJECT")
        if not project_id:
            raise HTTPException(status_code=500, detail="GCP_PROJECT environment variable not set.")

        # 2. Initialize Vertex AI and Memory inside the endpoint
        # This prevents crashes on startup.
        vertexai.init(project=project_id, location=LOCATION)
        memory = FirestoreMemory(project_id=project_id)

        # 3. Save the user's new message to Firestore
        memory.add_message(session_id=session_id, role="user", content=prompt)

        # 4. Retrieve the conversation history
        # We get the last 20 messages to keep the context window reasonable
        history = memory.get_messages(session_id=session_id, limit=20)
        
        # 5. Format history for the Gemini API
        # The history from Firestore already includes the new prompt we just added.
        messages_for_gemini = format_history_for_gemini(history)

        # 6. Call the Gemini API
        model = GenerativeModel(MODEL_NAME)
        # The Gemini API expects the history and the new prompt to be combined.
        # The last message in our list is the new user prompt.
        response = model.generate_content(messages_for_gemini)
        
        assistant_message = response.text

        # 7. Save the assistant's reply to Firestore
        memory.add_message(session_id=session_id, role="ai", content=assistant_message)

        # 8. Return the final response in a consistent format
        return {"response": assistant_message, "model_used": MODEL_NAME}

    except Exception as e:
        # Broad exception handling for any errors from Vertex AI or other issues.
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")