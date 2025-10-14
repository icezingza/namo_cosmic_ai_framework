import os
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Import the refactored FirestoreMemory class
from core_modules.memory import FirestoreMemory

# --- Configuration ---
# Get the GCP Project ID from environment variables.
# This is crucial for Application Default Credentials (ADC) to work correctly.
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")

if not GCP_PROJECT_ID:
    raise RuntimeError("GCP_PROJECT_ID environment variable not set. This is required to run the API.")

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

# --- Application State and Lifespan Management ---
# This dictionary will hold our shared service instance.
app_state: Dict[str, Any] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's lifespan. This is the recommended way to handle
    startup and shutdown events in modern FastAPI.
    """
    # --- Startup ---
    print("INFO:     Starting up and initializing Firestore client...")
    try:
        # Initialize the FirestoreMemory service once and store it in the app state.
        app_state["memory_service"] = FirestoreMemory(project_id=GCP_PROJECT_ID)
        print("INFO:     Firestore client initialized successfully.")
    except Exception as e:
        # If initialization fails, log the error and prevent the app from starting.
        print(f"ERROR:    Failed to initialize FirestoreMemory: {e}")
        # In a real-world scenario, you might want to exit or handle this more gracefully.
        raise RuntimeError(f"Could not initialize Firestore client: {e}") from e

    yield

    # --- Shutdown ---
    # No explicit shutdown actions are needed for the Firestore client, but this
    # is where you would put cleanup logic (e.g., closing database connections).
    print("INFO:     Shutting down application.")
    app_state.clear()


# --- FastAPI Application Setup ---
app = FastAPI(
    title="Namo Cosmic AI Memory Service",
    description="An API service providing memory capabilities for AI agents, powered by Google Firestore.",
    version="1.0.0",
    lifespan=lifespan  # Register the lifespan context manager
)

# --- Dependency Injection for Service ---
def get_memory_service() -> FirestoreMemory:
    """
    Dependency to get the shared FirestoreMemory service instance.
    This function now simply retrieves the pre-initialized instance from the app_state.
    """
    memory_service = app_state.get("memory_service")
    if not memory_service:
        # This should theoretically not happen if the lifespan event completes successfully.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Memory service is not available. The application might be starting up or has failed to initialize."
        )
    return memory_service


# --- API Endpoints ---

@app.get(
    "/health",
    tags=["Health"],
    summary="Perform a health check",
    response_model=HealthCheckResponse
)
def health_check():
    """
    Checks if the API is running and connected to the correct GCP project.
    """
    return {
        "status": "ok",
        "project_id": GCP_PROJECT_ID
    }

@app.post(
    "/sessions/{session_id}/messages",
    tags=["Memory"],
    summary="Add a message to a session",
    status_code=status.HTTP_201_CREATED
)
def add_message_to_session(
    session_id: str,
    message: Message,
    memory_service: FirestoreMemory = Depends(get_memory_service)
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
            detail=f"Failed to add message to Firestore: {e}"
        )

@app.get(
    "/sessions/{session_id}/messages",
    tags=["Memory"],
    summary="Retrieve messages from a session",
    response_model=List[Dict[str, Any]] # Returns a list of message-like dictionaries
)
def get_messages_from_session(
    session_id: str,
    limit: int = 50,
    memory_service: FirestoreMemory = Depends(get_memory_service)
):
    """
    Retrieves the most recent messages from the specified conversation session.

    - **session_id**: The unique identifier for the conversation.
    - **limit**: The maximum number of messages to retrieve (defaults to 50).
    """
    if limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'limit' parameter must be a positive integer."
        )
    try:
        messages = memory_service.get_messages(session_id, limit=limit)
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve messages from Firestore: {e}"
        )