import os

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

# Import the refactored FirestoreMemory class
from core_modules.memory import FirestoreMemory

# --- Configuration ---
# Get the GCP Project ID from environment variables.
# This is crucial for Application Default Credentials (ADC) to work correctly.
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")

if not GCP_PROJECT_ID:
    raise RuntimeError(
        "GCP_PROJECT_ID environment variable not set. This is required to run the API."
    )


# --- Pydantic Models for API Data Validation ---
class Message(BaseModel):
    """
    Represents a single message in a conversation.
    The role can be 'user' or 'ai'.
    """

    role: str
    content: str


class HealthCheckResponse(BaseModel):
    """
    Response model for the health check endpoint.
    """

    status: str
    project_id: str


# --- FastAPI Application Setup ---
app = FastAPI(
    title="Namo Cosmic AI Memory Service",
    description="An API service providing memory capabilities for AI agents, powered by Google Firestore.",
    version="1.0.0",
)


# --- Global Service Initialization ---
# This function will act as a dependency to provide the memory service.
def get_memory_service():
    try:
        # This part will be executed once per request that depends on it.
        # For a more complex setup, you might initialize this once at startup.
        yield FirestoreMemory(project_id=GCP_PROJECT_ID)
    except Exception as e:
        # If initialization fails, raise an HTTPException to be handled by FastAPI.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to initialize FirestoreMemory: {e}",
        ) from e


# --- API Endpoints ---


@app.get(
    "/health", tags=["Health"], summary="Perform a health check", response_model=HealthCheckResponse
)
def health_check():
    """
    Checks if the API is running and connected to the correct GCP project.
    """
    return {"status": "ok", "project_id": GCP_PROJECT_ID}


@app.post(
    "/sessions/{session_id}/messages",
    tags=["Memory"],
    summary="Add a message to a session",
    status_code=status.HTTP_201_CREATED,
)
def add_message_to_session(
    session_id: str, message: Message, memory_service: FirestoreMemory = Depends(get_memory_service)
):
    """
    Adds a new message to the specified conversation session.

    - **session_id**: The unique identifier for the conversation.
    - **message**: A JSON object with 'role' and 'content'.
    """
    try:
        memory_service.add_message(session_id, message.role, message.content)
        return {"status": "message added"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add message to Firestore: {e}",
        ) from e


@app.get(
    "/sessions/{session_id}/messages",
    tags=["Memory"],
    summary="Retrieve messages from a session",
    response_model=list[Message],
)
def get_messages_from_session(
    session_id: str, limit: int = 50, memory_service: FirestoreMemory = Depends(get_memory_service)
):
    """
    Retrieves the most recent messages from the specified conversation session.

    - **session_id**: The unique identifier for the conversation.
    - **limit**: The maximum number of messages to retrieve (defaults to 50).
    """
    if limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'limit' parameter must be a positive integer.",
        )
    try:
        messages = memory_service.get_messages(session_id, limit=limit)
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve messages from Firestore: {e}",
        ) from e
