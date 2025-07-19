# api_integration/multiverse_sync_api.py

from fastapi import APIRouter
from core_modules.multiverse_synapse import MultiverseSynapse

router = APIRouter()

@router.post("/multiverse-sync")
def multiverse_sync():
    synapse = MultiverseSynapse()
    return {
        "synced_data": synapse.sync_data(),
        "insights": synapse.integrate_insights()
    }
