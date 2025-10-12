"""Safety guardrails for Infinity AI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SafetyIncident:
    category: str
    message: str
    severity: str


class SafetySystem:
    PROHIBITED_KEYWORDS = {"malware", "harm", "exploit"}

    def __init__(self) -> None:
        self.incidents: List[SafetyIncident] = []

    def validate(self, text: str) -> bool:
        lowered = text.lower()
        if any(keyword in lowered for keyword in self.PROHIBITED_KEYWORDS):
            self.incidents.append(SafetyIncident("content", text, "high"))
            return False
        return True

    def report(self) -> Dict[str, int]:
        summary: Dict[str, int] = {}
        for incident in self.incidents:
            summary[incident.category] = summary.get(incident.category, 0) + 1
        return summary


__all__ = ["SafetySystem", "SafetyIncident"]
