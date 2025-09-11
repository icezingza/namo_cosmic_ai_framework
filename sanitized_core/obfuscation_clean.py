import re
from typing import Dict, Any

ZERO_WIDTH = re.compile(r"[\u200B-\u200F\uFEFF]")

def OBFUSCATION_CLEAN(signal: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = {}
    for k, v in signal.items():
        if isinstance(v, str):
            v = ZERO_WIDTH.sub("", v)
            if "stealth" in k:
                v = v.replace("sx","sex")
        cleaned[k] = v
    return {"cleaned": cleaned, "status": "normalized"}
