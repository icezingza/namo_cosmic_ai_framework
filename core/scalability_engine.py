"""Scalability engine responsible for analysing resource usage and scaling."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import psutil

try:  # pragma: no cover - optional dependency
    import GPUtil  # type: ignore
except Exception:  # pragma: no cover - handled gracefully
    GPUtil = None


LOGGER = logging.getLogger(__name__)


@dataclass
class SystemResources:
    cpu_percent: float
    memory_percent: float
    disk_usage: float
    gpu_usage: float | None = None
    network_io: dict[str, float] = None  # type: ignore[assignment]


@dataclass
class ScalingDecision:
    action: str
    reason: str
    confidence: float
    recommended_instances: int
    estimated_cost: float
    timestamp: datetime = datetime.utcnow()


class ScalabilityEngine:
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}
        self.logger = LOGGER
        self.metrics_history: list[dict[str, Any]] = []

    async def monitor_system_health(self) -> SystemResources:
        resources = SystemResources(
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=psutil.virtual_memory().percent,
            disk_usage=psutil.disk_usage("/").percent,
            network_io=self._get_network_io(),
        )
        if GPUtil is not None:  # pragma: no branch - optional path
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    resources.gpu_usage = max(gpu.load * 100 for gpu in gpus)
            except Exception as exc:  # pragma: no cover - GPU environments vary
                self.logger.warning("Could not get GPU usage: %s", exc)
        return resources

    async def make_scaling_decision(
        self, current_resources: SystemResources, business_metrics: dict[str, Any]
    ) -> ScalingDecision:
        analysis = await self._analyze_scaling_needs(current_resources, business_metrics)
        if analysis["needs_scaling"]:
            return await self._calculate_scaling_plan(analysis)
        return ScalingDecision(
            action="maintain",
            reason="System resources within optimal range",
            confidence=0.9,
            recommended_instances=1,
            estimated_cost=0.0,
        )

    async def _analyze_scaling_needs(
        self, resources: SystemResources, business_metrics: dict[str, Any]
    ) -> dict[str, Any]:
        cpu_critical = resources.cpu_percent > 80
        memory_critical = resources.memory_percent > 85
        disk_critical = resources.disk_usage > 90
        high_traffic = business_metrics.get("requests_per_second", 0) > 1000
        slow_response = business_metrics.get("avg_response_time", 0) > 2.0
        needs_scaling = any(
            [cpu_critical, memory_critical, disk_critical, high_traffic, slow_response]
        )
        return {
            "needs_scaling": needs_scaling,
            "critical_metrics": {
                "cpu": cpu_critical,
                "memory": memory_critical,
                "disk": disk_critical,
                "traffic": high_traffic,
                "response_time": slow_response,
            },
            "current_resources": resources,
            "business_metrics": business_metrics,
        }

    async def _calculate_scaling_plan(self, analysis: dict[str, Any]) -> ScalingDecision:
        critical_count = sum(1 for value in analysis["critical_metrics"].values() if value)
        if critical_count >= 3:
            return ScalingDecision(
                action="scale_up",
                reason="Multiple critical resource thresholds exceeded",
                confidence=0.95,
                recommended_instances=3,
                estimated_cost=self._estimate_cost(3),
            )
        if critical_count >= 2:
            return ScalingDecision(
                action="scale_up",
                reason="Multiple resource thresholds exceeded",
                confidence=0.8,
                recommended_instances=2,
                estimated_cost=self._estimate_cost(2),
            )
        return ScalingDecision(
            action="scale_up",
            reason="Single resource threshold exceeded",
            confidence=0.7,
            recommended_instances=1,
            estimated_cost=self._estimate_cost(1),
        )

    def _estimate_cost(self, instances: int) -> float:
        base_cost = float(self.config.get("hourly_cost_per_instance", 0.10))
        return instances * base_cost * 720

    def _get_network_io(self) -> dict[str, float]:
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
        }


__all__ = [
    "ScalabilityEngine",
    "ScalingDecision",
    "SystemResources",
]
