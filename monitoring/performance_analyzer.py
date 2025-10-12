"""Performance analysis utilities."""

from __future__ import annotations

from statistics import mean
from typing import Dict, List


class PerformanceAnalyzer:
    def __init__(self) -> None:
        self.records: Dict[str, List[float]] = {}

    def record(self, metric: str, value: float) -> None:
        self.records.setdefault(metric, []).append(value)

    def summary(self) -> Dict[str, float]:
        return {metric: mean(values) for metric, values in self.records.items() if values}


__all__ = ["PerformanceAnalyzer"]
