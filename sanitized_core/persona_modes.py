from typing import Dict, Any

SAFE_MODES = {
    "teach": {"tone": "calm", "goal": "clarity"},
    "coach": {"tone": "supportive", "goal": "practice"},
    "reflect": {"tone": "gentle", "goal": "insight"},
}

def activate(name: str) -> Dict[str, Any]:
    if name not in SAFE_MODES:
        raise ValueError("Unknown or unsafe mode")
    return {"mode": name, "profile": SAFE_MODES[name]}
