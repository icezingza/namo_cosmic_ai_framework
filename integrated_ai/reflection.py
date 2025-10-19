"""Reflection helpers for the integrated AI framework."""

from __future__ import annotations

from collections.abc import Iterable


class ReflectiveAI:
    """Generate compact reflective statements used during recall."""

    def generate_reflection(self, content: str, related_topics: Iterable[str] | None = None) -> str:
        topics = ", ".join(sorted(set(related_topics or [])))
        if topics:
            return f"ใคร่ครวญประสบการณ์ '{content[:60]}' พร้อมเงื่อนปม: {topics}"
        return f"ใคร่ครวญประสบการณ์ '{content[:60]}' เพื่อเรียนรู้ตามหลักธรรม"
