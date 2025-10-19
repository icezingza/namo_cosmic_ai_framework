"""Self-improvement and evolution engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EvolutionEvent:
    timestamp: datetime
    description: str
    metrics: dict[str, float] = field(default_factory=dict)


class EvolutionEngine:
    def __init__(self) -> None:
        self.history: list[EvolutionEvent] = []

    def record_event(
        self, description: str, metrics: dict[str, float] | None = None
    ) -> EvolutionEvent:
        event = EvolutionEvent(
            timestamp=datetime.utcnow(), description=description, metrics=metrics or {}
        )
        self.history.append(event)
        return event

    def latest_events(self, limit: int = 5) -> list[EvolutionEvent]:
        return list(self.history[-limit:])


__all__ = ["EvolutionEngine", "EvolutionEvent"]
