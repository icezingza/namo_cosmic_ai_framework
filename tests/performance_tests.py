import pytest

from monitoring.performance_analyzer import PerformanceAnalyzer


def test_performance_summary():
    analyzer = PerformanceAnalyzer()
    analyzer.record("latency", 0.5)
    analyzer.record("latency", 0.7)
    summary = analyzer.summary()
    assert summary["latency"] == pytest.approx(0.6, rel=1e-2)
