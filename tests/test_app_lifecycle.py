import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Set a dummy GCP_PROJECT_ID before importing the app
import os
os.environ["GCP_PROJECT_ID"] = "test-project"

# Import the FastAPI app instance and dependency function
from crystal_api_main import app, get_memory_service


@pytest.fixture(scope="module")
def client_and_mock():
    """
    Pytest fixture to create a TestClient for the FastAPI app.
    It patches the FirestoreMemory class to avoid actual GCP calls and to allow
    for inspecting its usage (e.g., call count).
    """
    with patch("crystal_api_main.FirestoreMemory") as mock_firestore_constructor:
        # The mock constructor will now return a MagicMock instance by default
        mock_firestore_constructor.return_value = MagicMock()

        # The `with TestClient(app)` block triggers the application lifespan events
        with TestClient(app) as test_client:
            # Yield both the client and the mock constructor so tests can use them
            yield test_client, mock_firestore_constructor

def test_memory_service_is_initialized_only_once(client_and_mock):
    """
    Tests that the FirestoreMemory class is instantiated exactly once during the
    application's startup.
    """
    _, mock_firestore_constructor = client_and_mock

    # The TestClient context manager in the fixture has already triggered the
    # app's startup. We just need to assert that the mocked constructor was
    # called exactly one time.
    mock_firestore_constructor.assert_called_once()

def test_same_memory_instance_is_used_across_requests(client_and_mock):
    """
    Tests that the same singleton instance of the memory service is injected
    into multiple API requests.
    """
    client, _ = client_and_mock

    # Store the object ID of the injected dependency for each request
    instance_ids = set()

    # Define a dependency override to capture the ID of the injected service
    def capture_id_dependency():
        # Get the service using the original dependency logic, which now
        # retrieves the singleton instance from the app's state.
        service = get_memory_service()
        instance_ids.add(id(service))
        # Return the service so the endpoint can function
        return service

    # Replace the app's dependency with our capturing function
    app.dependency_overrides[get_memory_service] = capture_id_dependency

    try:
        # Make two separate requests to any endpoint that uses the dependency
        client.post("/sessions/test-session-1/messages", json={"role": "user", "content": "First call"})
        client.post("/sessions/test-session-2/messages", json={"role": "user", "content": "Second call"})

        # Assert that only one unique object ID was captured, proving it's a singleton
        assert len(instance_ids) == 1

    finally:
        # Clean up the dependency override after the test
        del app.dependency_overrides[get_memory_service]