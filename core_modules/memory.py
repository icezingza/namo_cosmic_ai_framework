
import firebase_admin
from firebase_admin import firestore
from typing import List, Dict, Any

class FirestoreMemory:
    """
    A class to handle conversation memory using Google Firestore.
    Assumes firebase_admin has been initialized elsewhere.
    """
    def __init__(self):
        """
        Initializes the Firestore client.
        """
        self.db = firestore.client()

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """
        Adds a message to a conversation session in Firestore.

        Args:
            session_id (str): The unique identifier for the conversation session.
            role (str): The role of the message sender (e.g., 'user', 'ai', 'sender', 'receiver').
            content (str): The content of the message.
        """
        if not session_id or not role or not content:
            print("Error: session_id, role, and content cannot be empty.")
            return

        session_ref = self.db.collection('chat_sessions').document(session_id)
        messages_ref = session_ref.collection('messages')
        
        messages_ref.add({
            'role': role,
            'content': content,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

    def get_messages(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieves messages from a conversation session.

        Args:
            session_id (str): The unique identifier for the conversation session.
            limit (int): The maximum number of messages to retrieve, ordered by most recent.

        Returns:
            A list of message dictionaries.
        """
        if not session_id:
            return []
            
        messages_ref = self.db.collection('chat_sessions').document(session_id).collection('messages')
        
        # Order by timestamp descending to get the most recent messages
        query = messages_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
        
        docs = query.stream()
        
        # Reverse the order to return messages in chronological order (oldest first)
        messages = [doc.to_dict() for doc in docs]
        messages.reverse()
        
        return messages

# Example Usage (for testing)
if __name__ == '__main__':
    # To run this test, you need to have Application Default Credentials set up.
    # For local development, run: `gcloud auth application-default login`
    # And make sure your project is set: `gcloud config set project YOUR_PROJECT_ID`
    
    # You can also use a service account file:
    # SA_PATH = 'path/to/your/service-account.json'
    # memory = FirestoreMemory(service_account_path=SA_PATH)

    print("Connecting to Firestore...")
    # This will use Application Default Credentials if no path is provided
    memory = FirestoreMemory(project_id='namo-legacy-identity') 
    
    session_id = "test_session_001"
    
    print(f"Adding messages to session: {session_id}")
    memory.add_message(session_id, "user", "Hello, this is a test.")
    memory.add_message(session_id, "ai", "Hello, user! I am responding.")
    
    print("Retrieving messages...")
    history = memory.get_messages(session_id)
    
    if history:
        for msg in history:
            print(f"- [{msg.get('role')}] {msg.get('content')} (at {msg.get('timestamp')})")
    else:
        print("Could not retrieve messages. Make sure Firestore is set up correctly.")

