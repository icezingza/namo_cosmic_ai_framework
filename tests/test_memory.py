import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add the project root to the path to allow importing core_modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_modules.memory import FirestoreMemory

class TestFirestoreMemory(unittest.TestCase):

    @patch('core_modules.memory.firestore')
    @patch('core_modules.memory.firebase_admin')
    def test_initialization_with_project_id(self, mock_firebase_admin, mock_firestore):
        """
        Tests that FirestoreMemory initializes correctly using a project_id,
        relying on Application Default Credentials.
        """
        # --- Setup Mocks ---
        mock_firebase_admin.get_app.side_effect = ValueError("App not found")
        mock_app = MagicMock(name="MockApp")
        mock_firebase_admin.initialize_app.return_value = mock_app
        mock_client = MagicMock(name="MockClient")
        mock_firestore.client.return_value = mock_client

        # --- Test Logic ---
        project_id = "test-project-adc"
        memory = FirestoreMemory(project_id=project_id)

        # --- Assertions ---
        # 1. Check that get_app was called to see if the app already exists
        mock_firebase_admin.get_app.assert_called_once_with(name=project_id)

        # 2. Check that initialize_app was called correctly for ADC
        #    (None for credentials)
        mock_firebase_admin.initialize_app.assert_called_once_with(
            None, {'projectId': project_id}, name=project_id
        )

        # 3. Check that the client was requested for the correct app
        mock_firestore.client.assert_called_once_with(app=mock_app)

        # 4. Check that the db attribute is set correctly
        self.assertEqual(memory.db, mock_client)

    def test_initialization_requires_project_id(self):
        """
        Tests that a ValueError is raised if no project_id is provided.
        """
        with self.assertRaisesRegex(ValueError, "A project_id is required"):
            FirestoreMemory(project_id=None)

        with self.assertRaisesRegex(ValueError, "A project_id is required"):
            FirestoreMemory(project_id="")

    @patch('core_modules.memory.firestore')
    @patch('core_modules.memory.firebase_admin')
    def test_add_message_requires_parameters(self, mock_firebase_admin, mock_firestore):
        """
        Tests that add_message raises ValueError for empty inputs.
        """
        memory = FirestoreMemory(project_id="test-project")

        with self.assertRaisesRegex(ValueError, "session_id, role, and content cannot be empty"):
            memory.add_message(session_id="", role="user", content="Hello")

        with self.assertRaisesRegex(ValueError, "session_id, role, and content cannot be empty"):
            memory.add_message(session_id="test", role="", content="Hello")

        with self.assertRaisesRegex(ValueError, "session_id, role, and content cannot be empty"):
            memory.add_message(session_id="test", role="user", content="")


if __name__ == '__main__':
    unittest.main()