import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

# Set the environment variable required by the app BEFORE importing the app
import os
os.environ["GCP_PROJECT_ID"] = "test-project"

# Import the app and the dependency function after setting the env var
from crystal_api_main import app, get_memory_service


@pytest.fixture
def mock_memory_service():
    """Fixture to create a mock of the FirestoreMemory service."""
    service = MagicMock()
    service.get_messages.return_value = [{"role": "user", "content": "hello"}]
    service.add_message.return_value = None
    return service


@pytest.fixture
def client(mock_memory_service):
    """
    Fixture to create a TestClient with the get_memory_service dependency
    overridden to return our mock service.
    """
    # Define the override function
    def override_get_memory_service():
        yield mock_memory_service

    # Apply the dependency override
    app.dependency_overrides[get_memory_service] = override_get_memory_service

    with TestClient(app) as c:
        yield c

    # Clean up the override after the test
    del app.dependency_overrides[get_memory_service]


def test_health_check(client):
    """Tests the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "project_id": "test-project"}


def test_get_messages_invalid_limit_negative(client):
    """Tests that a negative limit returns a 400 Bad Request."""
    response = client.get("/sessions/test-session/messages?limit=-1")
    assert response.status_code == 400
    assert "must be a positive integer" in response.json()["detail"]


def test_get_messages_invalid_limit_zero(client):
    """Tests that a limit of zero returns a 400 Bad Request."""
    response = client.get("/sessions/test-session/messages?limit=0")
    assert response.status_code == 400
    assert "must be a positive integer" in response.json()["detail"]


def test_get_messages_valid_limit(client, mock_memory_service):
    """Tests retrieving messages with a valid limit."""
    response = client.get("/sessions/test-session/messages?limit=10")
    assert response.status_code == 200
    # Verify the mocked service was called correctly
    mock_memory_service.get_messages.assert_called_once_with("test-session", limit=10)
    # Verify the response from the mock is passed through
    assert response.json() == [{"role": "user", "content": "hello"}]


def test_add_message(client, mock_memory_service):
    """Tests adding a message to a session."""
    message_data = {"role": "user", "content": "test message"}
    response = client.post("/sessions/test-session/messages", json=message_data)
    assert response.status_code == 201
    assert response.json() == {"status": "message added"}
    # Verify the mocked service was called correctly
    mock_memory_service.add_message.assert_called_once_with("test-session", "user", "test message")