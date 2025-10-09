"""Self-evolution orchestration for the integrated AI framework."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional

from .memory_core import InfinityMemorySystem


@dataclass
class EvolutionRecord:
    event: Dict[str, Any]
    plan: Dict[str, Any]
    context: List[Dict[str, Any]]
    response: Dict[str, Any]
    score: Dict[str, float]
    timestamp: datetime


class DecisionEngine:
    def decide(self, goals: Dict[str, Any], constraints: Dict[str, Any], context: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "strategy": goals.get("focus", "empathy"),
            "constraints": constraints,
            "context_summary": [item.get("memory_id") for item in context],
        }


class LLMGenerator:
    def generate(self, plan: Dict[str, Any], style: str) -> Dict[str, Any]:
        message = f"ตอบสนองด้วยสไตล์ {style} โดยคำนึงถึง {plan['strategy']}"
        return {"message": message, "style": style}


class Evaluator:
    def evaluate(self, response: Dict[str, Any], metrics: List[str]) -> Dict[str, float]:
        return {metric: 0.9 for metric in metrics}


class EvolutionAnalyzer:
    def analyze(self, records: List[EvolutionRecord]) -> Dict[str, Any]:
        return {"avg_score": sum(record.score.get("tone", 0.0) for record in records) / max(len(records), 1)}


class PolicySynthesizer:
    def synthesize(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        return {"focus": "empathy" if insights.get("avg_score", 0.0) < 0.95 else "wisdom"}


class ABTester:
    def test_improvement(self, new_policy: Dict[str, Any]) -> float:
        return 0.1 if new_policy.get("focus") == "wisdom" else 0.08


class MetricsTracker:
    def current_metrics(self) -> Dict[str, float]:
        return {"latency_ms": 120.0, "satisfaction": 0.88}

    def measure_impact(self) -> Dict[str, float]:
        return {"latency_delta": -5.0, "satisfaction_delta": 0.03}


class InfinityEvolutionEngine:
    """Coordinate adaptive evolution cycles."""

    def __init__(
        self,
        memory_system: Optional[InfinityMemorySystem] = None,
        decision_engine: Optional[DecisionEngine] = None,
        llm_generator: Optional[LLMGenerator] = None,
        evaluator: Optional[Evaluator] = None,
        analyzer: Optional[EvolutionAnalyzer] = None,
        policy_synthesizer: Optional[PolicySynthesizer] = None,
        ab_tester: Optional[ABTester] = None,
        metrics_tracker: Optional[MetricsTracker] = None,
    ) -> None:
        self.memory_system = memory_system or InfinityMemorySystem()
        self.decision_engine = decision_engine or DecisionEngine()
        self.llm_generator = llm_generator or LLMGenerator()
        self.evaluator = evaluator or Evaluator()
        self.analyzer = analyzer or EvolutionAnalyzer()
        self.policy_synthesizer = policy_synthesizer or PolicySynthesizer()
        self.ab_tester = ab_tester or ABTester()
        self.metrics_tracker = metrics_tracker or MetricsTracker()
        self.emotion_engine_style = "compassion"
        self.current_goals = {"focus": "empathy"}
        self.current_constraints = {"safety": "strict"}
        self.evolution_buffer: List[EvolutionRecord] = []
        self.current_policy_version = "1.0"
        self.policy_history: List[Dict[str, Any]] = []
        self.evolution_logs: List[Dict[str, Any]] = []
        self.improvement_threshold = 0.09

    def on_interaction(self, event: Dict[str, Any]) -> Dict[str, Any]:
        features = self._extract_features(event)
        memory_result = self.memory_system.create_memory(features["content"], context=features["context"])
        context = self.memory_system.recall_memory(event.get("query", ""), limit=3)
        context_payload = [
            {"memory_id": item.id, "emotions": item.emotion_intensity}
            for item in context
        ]
        action_plan = self.decision_engine.decide(self.current_goals, self.current_constraints, context_payload)
        response = self.llm_generator.generate(action_plan, style=self.emotion_engine_style)
        score = self.evaluator.evaluate(response, metrics=["tone", "task_completion", "latency", "goal_conflict"])
        record = EvolutionRecord(
            event=event,
            plan=action_plan,
            context=context_payload,
            response=response,
            score=score,
            timestamp=datetime.now(UTC),
        )
        self.evolution_buffer.append(record)
        return {"response": response, "memory_id": memory_result["memory_id"]}

    def periodic_evolution(self) -> Optional[Dict[str, Any]]:
        if not self.evolution_buffer:
            return None
        insights = self.analyzer.analyze(self.evolution_buffer)
        new_policy = self.policy_synthesizer.synthesize(insights)
        improvement = self.ab_tester.test_improvement(new_policy)
        if improvement >= self.improvement_threshold:
            self.deploy_policy(new_policy)
            self.log_evolution(insights, new_policy)
            self.evolution_buffer.clear()
            return new_policy
        self.evolution_buffer.clear()
        return None

    def deploy_policy(self, new_policy: Dict[str, Any]) -> None:
        version = f"{float(self.current_policy_version) + 0.1:.1f}"
        self.policy_history.append(
            {
                "version": version,
                "policy": new_policy,
                "timestamp": datetime.now(UTC),
                "metrics_before": self.metrics_tracker.current_metrics(),
            }
        )
        self.current_policy_version = version
        self.current_goals.update(new_policy)

    def log_evolution(self, insights: Dict[str, Any], policy: Dict[str, Any]) -> None:
        self.evolution_logs.append(
            {
                "timestamp": datetime.now(UTC),
                "policy_version": self.current_policy_version,
                "insights": insights,
                "policy_changes": policy,
                "metrics_impact": self.metrics_tracker.measure_impact(),
            }
        )

    def _extract_features(self, event: Dict[str, Any]) -> Dict[str, Any]:
        content = event.get("content") or event.get("message") or ""
        context = {key: value for key, value in event.items() if key not in {"content", "message"}}
        return {"content": content, "context": context}
