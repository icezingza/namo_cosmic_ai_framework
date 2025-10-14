import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

# Set the environment variable required by the app BEFORE importing the app
import os
os.environ["GCP_PROJECT_ID"] = "test-project"

# Import the app and the dependency function after setting the env var
from crystal_api_main import app, get_memory_service


@pytest.fixture
def client_with_mock_service():
    """
    Fixture to create a TestClient and a mock service.
    It patches FirestoreMemory to prevent real GCP calls during app startup.
    The mock service instance is yielded along with the client.
    """
    with patch("crystal_api_main.FirestoreMemory") as mock_firestore_constructor:
        mock_service_instance = MagicMock()
        mock_firestore_constructor.return_value = mock_service_instance

        with TestClient(app) as test_client:
            # Yield both the client and the mock service instance
            yield test_client, mock_service_instance

def test_health_check(client_with_mock_service):
    """Tests the health check endpoint."""
    client, _ = client_with_mock_service
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "project_id": "test-project"}


def test_get_messages_invalid_limit_negative(client_with_mock_service):
    """Tests that a negative limit returns a 400 Bad Request."""
    client, _ = client_with_mock_service
    response = client.get("/sessions/test-session/messages?limit=-1")
    assert response.status_code == 400
    assert "must be a positive integer" in response.json()["detail"]


def test_get_messages_invalid_limit_zero(client_with_mock_service):
    """Tests that a limit of zero returns a 400 Bad Request."""
    client, _ = client_with_mock_service
    response = client.get("/sessions/test-session/messages?limit=0")
    assert response.status_code == 400
    assert "must be a positive integer" in response.json()["detail"]


def test_get_messages_valid_limit(client_with_mock_service):
    """Tests retrieving messages with a valid limit."""
    client, mock_memory_service = client_with_mock_service
    mock_memory_service.get_messages.return_value = [{"role": "user", "content": "hello"}]

    response = client.get("/sessions/test-session/messages?limit=10")

    assert response.status_code == 200
    mock_memory_service.get_messages.assert_called_once_with("test-session", limit=10)
    assert response.json() == [{"role": "user", "content": "hello"}]


def test_add_message(client_with_mock_service):
    """Tests adding a message to a session."""
    client, mock_memory_service = client_with_mock_service
    message_data = {"role": "user", "content": "test message"}

    response = client.post("/sessions/test-session/messages", json=message_data)

    assert response.status_code == 201
    assert response.json() == {"status": "message added"}
    mock_memory_service.add_message.assert_called_once_with("test-session", "user", "test message")