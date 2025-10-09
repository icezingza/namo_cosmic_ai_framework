"""Disaster recovery utilities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass
class RecoveryPlan:
    name: str
    steps: List[str]
    last_tested: datetime
    recovery_time_objective: str
    recovery_point_objective: str


class RecoverySystem:
    def __init__(self) -> None:
        self.plans: Dict[str, RecoveryPlan] = {}

    def add_plan(
        self,
        name: str,
        steps: List[str],
        rto: str = "4h",
        rpo: str = "15m",
    ) -> RecoveryPlan:
        plan = RecoveryPlan(
            name=name,
            steps=steps,
            last_tested=datetime.utcnow(),
            recovery_time_objective=rto,
            recovery_point_objective=rpo,
        )
        self.plans[name] = plan
        return plan

    def get_plan(self, name: str) -> RecoveryPlan | None:
        return self.plans.get(name)


__all__ = ["RecoverySystem", "RecoveryPlan"]
