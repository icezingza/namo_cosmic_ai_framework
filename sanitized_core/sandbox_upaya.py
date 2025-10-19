from collections.abc import Callable
from typing import Any


def SANDBOX_UPAYA(plan: dict[str, Any], run: Callable[[], dict[str, Any]] = None) -> dict[str, Any]:
    result = {"status": "dry_run"}
    if run:
        out = run()
        result["result"] = {k: v for k, v in out.items() if k in ("metrics", "notes")}
    return result
