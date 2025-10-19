"""Alert routing utilities."""

from __future__ import annotations


class AlertSystem:
    def __init__(self) -> None:
        self.subscribers: list[str] = []
        self.history: list[dict[str, str]] = []

    def subscribe(self, channel: str) -> None:
        if channel not in self.subscribers:
            self.subscribers.append(channel)

    def dispatch(self, title: str, message: str) -> dict[str, str]:
        payload = {"title": title, "message": message}
        self.history.append(payload)
        return payload


__all__ = ["AlertSystem"]
