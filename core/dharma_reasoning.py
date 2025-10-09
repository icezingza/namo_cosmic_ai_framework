"""Reasoning helpers inspired by dharma principles."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DharmaDecision:
    principle: str
    rationale: str
    confidence: float


class DharmaReasoningEngine:
    PRINCIPLES = {
        "ahimsa": "Minimise harm in all outcomes",
        "satya": "Prioritise truthfulness and transparency",
        "dharma": "Act in alignment with duty and ethics",
    }

    def evaluate(self, situation: Dict[str, str]) -> DharmaDecision:
        context = situation.get("context", "")
        if "risk" in context.lower():
            principle = "ahimsa"
        elif "uncertain" in context.lower():
            principle = "satya"
        else:
            principle = "dharma"
        rationale = self.PRINCIPLES[principle]
        confidence = 0.8 if principle != "dharma" else 0.7
        return DharmaDecision(principle, rationale, confidence)


__all__ = ["DharmaReasoningEngine", "DharmaDecision"]
