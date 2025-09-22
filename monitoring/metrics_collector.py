"""Metrics collection utilities."""

from __future__ import annotations

from typing import Dict


class MetricsCollector:
    def __init__(self) -> None:
        self.metrics: Dict[str, float] = {}

    def record(self, name: str, value: float) -> None:
        self.metrics[name] = value

    def snapshot(self) -> Dict[str, float]:
        return dict(self.metrics)


__all__ = ["MetricsCollector"]
