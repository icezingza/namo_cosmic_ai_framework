"""Integration-style tests for the Integrated AI framework pieces."""

from __future__ import annotations

from pathlib import Path

from integrated_ai import InfinityMemorySystem, SafetyAndCompliance


def test_memory_persistence_and_recall(tmp_path: Path) -> None:
    db_path = tmp_path / "memory.db"
    system = InfinityMemorySystem(db_path=db_path)
    creation = system.create_memory(
        "วันนี้ได้กลับไปเจอเพื่อนสมัยเรียน ทำให้คิดถึงช่วงเวลาที่มีความสุข",
        context={"user_id": "tester", "channel": "chat"},
    )
    first_id = creation["memory_id"]
    system.close()

    # Re-initialise to make sure content is reloaded from SQLite storage.
    reloaded = InfinityMemorySystem(db_path=db_path)
    recalled = reloaded.recall_memory("เพื่อน", limit=1)
    assert recalled, "Expected to recall the stored memory"
    memory = recalled[0]
    assert memory.id == first_id
    assert "nostalgia" in memory.emotion_tag
    assert memory.recall_count >= 1
    assert memory.last_recalled is not None
    reloaded.close()


def test_safety_and_compliance_audit_logging(tmp_path: Path) -> None:
    safety = SafetyAndCompliance()
    event = {"user_id": "user123", "ip_address": "127.0.0.1", "content": "sample"}
    safety.audit_log(event)
    record = safety.audit_logger.records[-1]
    assert record["user_id"] != "user123"
    assert record["ip_address"] != "127.0.0.1"
    assert len(safety.audit_logger.records) == 1

    checks = safety.check_compliance("Please email me at test@example.com", {"severity": "low"})
    assert checks["pii_leakage"] is True
    assert checks["ethical_violation"] is False
