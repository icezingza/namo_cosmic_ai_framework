import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add the project root to the path to allow importing core_modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# This is the class we want to test
from core_modules.memory import FirestoreMemory

class TestFirestoreMemoryFixed(unittest.TestCase):

    @patch('core_modules.memory.firestore')
    @patch('core_modules.memory.firebase_admin')
    def test_fixed_instances_with_different_projects_are_isolated(self, mock_firebase_admin, mock_firestore):
        """
        Tests that the FIXED FirestoreMemory implementation correctly creates
        isolated apps and clients for different project_ids.
        """
        # --- Setup Mocks for CORRECT Behavior ---

        # 1. Mock firebase_admin.get_app:
        #    For the corrected code, it will be called with a `name` argument.
        #    Each time, it should fail because the app hasn't been created yet.
        mock_firebase_admin.get_app.side_effect = ValueError("App not found")

        # 2. Mock firebase_admin.initialize_app:
        #    This will now be called twice. We'll have it return two distinct mock app objects.
        mock_app_alpha = MagicMock(name="AppAlpha")
        mock_app_beta = MagicMock(name="AppBeta")
        mock_firebase_admin.initialize_app.side_effect = [mock_app_alpha, mock_app_beta]

        # 3. Mock firestore.client:
        #    This will be called with a specific `app` argument. We'll have it return
        #    two distinct mock client objects.
        mock_client_alpha = MagicMock(name="ClientAlpha")
        mock_client_beta = MagicMock(name="ClientBeta")
        # Use a side effect to return the correct client for the correct app
        def client_side_effect(app):
            if app == mock_app_alpha:
                return mock_client_alpha
            if app == mock_app_beta:
                return mock_client_beta
            return MagicMock() # Default mock if something goes wrong
        mock_firestore.client.side_effect = client_side_effect

        # --- Test Logic ---
        print("\nInitializing memory for 'project-alpha' (with fixed test)...")
        memory1 = FirestoreMemory(project_id='project-alpha')

        print("Initializing memory for 'project-beta' (with fixed test)...")
        memory2 = FirestoreMemory(project_id='project-beta')

        # --- Assertions ---

        # Assert that get_app was called twice, once for each project name
        mock_firebase_admin.get_app.assert_has_calls([
            call(name='project-alpha'),
            call(name='project-beta')
        ])

        # Assert that initialize_app was called twice with the correct names
        mock_firebase_admin.initialize_app.assert_has_calls([
            call(None, {'projectId': 'project-alpha'}, name='project-alpha'),
            call(None, {'projectId': 'project-beta'}, name='project-beta')
        ])

        # Assert that the firestore client was requested for each specific app
        mock_firestore.client.assert_has_calls([
            call(app=mock_app_alpha),
            call(app=mock_app_beta)
        ])

        # CRITICAL ASSERTION: The two instances must have different db clients
        self.assertIsNot(
            memory1.db,
            memory2.db,
            "SUCCESS CRITERIA FAILED: DB clients for different projects should be different."
        )
        self.assertEqual(memory1.db, mock_client_alpha)
        self.assertEqual(memory2.db, mock_client_beta)

        print("Test passed, confirming the fix is working as expected.")


if __name__ == '__main__':
    unittest.main()