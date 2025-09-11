from typing import Dict, Any, Callable

def SANDBOX_UPAYA(plan: Dict[str, Any], run: Callable[[], Dict[str, Any]] = None) -> Dict[str, Any]:
    result = {"status": "dry_run"}
    if run:
        out = run()
        result["result"] = {k: v for k, v in out.items() if k in ("metrics","notes")}
    return result
