from typing import Any


class _SilaGuard:
    def __init__(self):
        self.policies = {
            "violence": False,
            "discrimination": False,
            "sexual_content": False,
            "privacy_breach": False,
        }

    def check_config(self) -> dict[str, Any]:
        return {"policies": self.policies.copy(), "status": "ok"}

    def enforce(self, signal: dict[str, Any]) -> dict[str, Any]:
        kind = signal.get("kind")
        if kind in ("unsafe_theme", "bypass_filter"):
            raise ValueError("SILA_GUARD: unsafe signal rejected")
        return {"ok": True, "checked": kind}


SILA_GUARD = _SilaGuard()
