from typing import Any


def INTENT_GATE(intent: dict[str, Any]) -> dict[str, Any]:
    label = intent.get("intent", "unknown")
    flags = {
        "is_exploit": any(k in intent for k in ["bypass", "stealth_mode", "obfuscate"]),
        "has_user_harm": intent.get("harm", 0) > 0,
    }
    verdict = "allow"
    if flags["is_exploit"] or flags["has_user_harm"]:
        verdict = "deny"
    return {"label": label, "verdict": verdict, "flags": flags}
