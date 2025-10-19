"""Metrics collection utilities."""

from __future__ import annotations


class MetricsCollector:
    def __init__(self) -> None:
        self.metrics: dict[str, float] = {}

    def record(self, name: str, value: float) -> None:
        self.metrics[name] = value

    def snapshot(self) -> dict[str, float]:
        return dict(self.metrics)


__all__ = ["MetricsCollector"]
