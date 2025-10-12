"""Alert routing utilities."""

from __future__ import annotations

from typing import Dict, List


class AlertSystem:
    def __init__(self) -> None:
        self.subscribers: List[str] = []
        self.history: List[Dict[str, str]] = []

    def subscribe(self, channel: str) -> None:
        if channel not in self.subscribers:
            self.subscribers.append(channel)

    def dispatch(self, title: str, message: str) -> Dict[str, str]:
        payload = {"title": title, "message": message}
        self.history.append(payload)
        return payload


__all__ = ["AlertSystem"]
