from typing import Dict, Any, List
from datetime import datetime

class _Ledger:
    def __init__(self):
        self.log: List[Dict[str, Any]] = []

    def record(self, change: Dict[str, Any]) -> Dict[str, Any]:
        item = {"ts": datetime.utcnow().isoformat() + "Z", **change}
        self.log.append(item)
        return item

    def history(self) -> List[Dict[str, Any]]:
        return list(self.log)

    def revertible(self, key: str) -> Dict[str, Any]:
        return {"revert_key": key, "available": True}

LEDGER_MEM = _Ledger()
