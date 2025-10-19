from datetime import datetime
from typing import Any


class _Ledger:
    def __init__(self):
        self.log: list[dict[str, Any]] = []

    def record(self, change: dict[str, Any]) -> dict[str, Any]:
        item = {"ts": datetime.utcnow().isoformat() + "Z", **change}
        self.log.append(item)
        return item

    def history(self) -> list[dict[str, Any]]:
        return list(self.log)

    def revertible(self, key: str) -> dict[str, Any]:
        return {"revert_key": key, "available": True}


LEDGER_MEM = _Ledger()
