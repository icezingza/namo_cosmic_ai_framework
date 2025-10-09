"""Capacity planning helper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class CapacityPlan:
    projected_load: int
    recommended_instances: int
    notes: str


class CapacityPlanner:
    def plan(self, historical_load: List[int]) -> CapacityPlan:
        if not historical_load:
            return CapacityPlan(0, 1, "No data; default plan")
        peak = max(historical_load)
        recommended = max(2, peak // 100 + 1)
        notes = f"Peak load {peak} handled with {recommended} instances"
        return CapacityPlan(peak, recommended, notes)


__all__ = ["CapacityPlanner", "CapacityPlan"]
