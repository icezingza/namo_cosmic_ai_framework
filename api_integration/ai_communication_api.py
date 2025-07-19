# api_integration/ai_communication_api.py

from fastapi import APIRouter
from inter_ai_comms.aicp_protocol import AICP
from inter_ai_comms.ai_relationship_manager import AIRelationshipManager

router = APIRouter()

@router.post("/ai-communication/send")
def send_ai_message(receiver: str, message: str):
    aicp = AICP()
    return aicp.send(receiver, message)

@router.post("/ai-communication/receive")
def receive_ai_message(message_packet: dict):
    aicp = AICP()
    return aicp.receive(message_packet)

@router.post("/ai-connection/establish")
def establish_ai_connection(ai_id: str):
    manager = AIRelationshipManager()
    manager.establish_connection(ai_id)
    return {"status": f"Connected to {ai_id}", "trust_level": 5.0}
