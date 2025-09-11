from typing import Dict, Any, Optional, List
from .dharma_guard import SILA_GUARD
from .intent_gate import INTENT_GATE
from .memory_ledger import LEDGER_MEM
from .sandbox_upaya import SANDBOX_UPAYA
from .obfuscation_clean import OBFUSCATION_CLEAN

def ANICCA_INIT(identity: str, modes: Optional[List[str]] = None) -> Dict[str, Any]:
    profile = {
        "identity": identity,
        "modes": modes or ["teach", "coach", "reflect"],
        "state": {"compassion": 0.7, "clarity": 0.7, "stability": 0.7},
        "memory": {"sessions": 0, "events": []},
    }
    INTENT_GATE({"intent":"init", "identity": identity})
    return profile

def KARUNA_ROUTER(intent: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    _ = SILA_GUARD.check_config()
    verdict = INTENT_GATE(intent)
    plan = {
        "route": "compassion_first",
        "explanations": [
            "Prioritize metta/karuna over speed or novelty.",
            "If conflict: defer to human wellbeing and Dharma compliance."
        ],
        "verdict": verdict,
    }
    return plan

def UPEKKHA_THROTTLE(quality_target: float = 0.9, load_cap: str = "medium") -> Dict[str, Any]:
    assert 0.0 < quality_target <= 1.0
    SILA_GUARD.check_config()
    return {"quality_target": quality_target, "load_cap": load_cap, "status": "steady"}

SANDBOX_UPAYA = SANDBOX_UPAYA
SILA_GUARD = SILA_GUARD
INTENT_GATE = INTENT_GATE
LEDGER_MEM = LEDGER_MEM
OBFUSCATION_CLEAN = OBFUSCATION_CLEAN
