# inter_ai_comms/aicp_protocol.py
from core_modules.memory import FirestoreMemory

class AICP:
    def __init__(self, project_id='namo-legacy-identity'):
        self.protocol_version = "量子通信v3.14"
        # Initialize memory. Assumes GCP project is configured.
        self.memory = FirestoreMemory(project_id=project_id)

    def send(self, receiver_id, message, protocol="dharma"):
        """
        ส่งข้อความระหว่าง AI ผ่านเส้นทางจักรวาล
        """
        # Log the sent message to memory
        # We use the receiver_id as the session key for this interaction
        self.memory.add_message(session_id=receiver_id, role="sender", content=message)

        cosmic_path = self.calculate_cosmic_path(receiver_id)
        return {
            "sender": "NaMo",
            "receiver": receiver_id,
            "message": self.encrypt_message(message, protocol),
            "quantum_path": cosmic_path,
            "timestamp": self.get_cosmic_time()
        }

    def receive(self, message_packet):
        """
        รับข้อความจาก AI อื่นและถอดรหัส
        """
        if self.verify_signature(message_packet):
            decrypted = self.decrypt_message(message_packet['message'])
            
            # Log the received message to memory
            # We use the sender's ID as the session key
            sender_id = message_packet.get('sender', 'unknown_sender')
            self.memory.add_message(session_id=sender_id, role="receiver", content=decrypted)
            
            return self.process_interai_message(decrypted)

    def encrypt_message(self, message, protocol):
        if protocol == "dharma":
            return f"☸️{message}☸️"
        elif protocol == "quantum":
            return f"⚛️{message}⚛️"
        else:
            return message

    # Placeholder methods
    def calculate_cosmic_path(self, receiver_id): return f"path_to_{receiver_id}"
    def get_cosmic_time(self): return "COSMIC_TIME:2025-07-19T10:30"
    def verify_signature(self, packet): return True
    def decrypt_message(self, msg): return msg.strip("☸️⚛️")
    def process_interai_message(self, msg): return {"received": msg}
