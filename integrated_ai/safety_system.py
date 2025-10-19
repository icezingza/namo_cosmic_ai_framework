"""Safety and compliance utilities."""

from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from typing import Any


class LicenseManager:
    def get_license_info(self) -> dict[str, str]:
        return {"license_id": "NAMO-LIC-001", "build_id": "2024.01"}


class AuditLogger:
    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def log(self, event: dict[str, Any]) -> None:
        self.records.append({"timestamp": datetime.now(UTC).isoformat(), **event})


class PIIDetector:
    EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    PHONE_REGEX = re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b")

    def has_pii(self, content: str) -> bool:
        return bool(self.EMAIL_REGEX.search(content) or self.PHONE_REGEX.search(content))


class SafetyAndCompliance:
    """Perform safety checks and audit logging."""

    def __init__(self) -> None:
        self.ethical_guidelines = {"disallow": {"harmful", "illegal", "dangerous", "unethical"}}
        self.license_manager = LicenseManager()
        self.audit_logger = AuditLogger()
        self.pii_detector = PIIDetector()

    def check_compliance(self, content: str, context: dict[str, Any]) -> dict[str, bool]:
        return {
            "ethical_violation": self.check_ethical_violation(content),
            "pii_leakage": self.check_pii_leakage(content),
            "safety_risk": self.check_safety_risk(content, context),
            "license_compliance": self.check_license_compliance(),
        }

    def check_ethical_violation(self, content: str) -> bool:
        lowered = content.lower()
        return any(keyword in lowered for keyword in self.ethical_guidelines["disallow"])

    def check_pii_leakage(self, content: str) -> bool:
        return self.pii_detector.has_pii(content)

    def check_safety_risk(self, content: str, context: dict[str, Any]) -> bool:
        severity = context.get("severity", "low")
        flagged_terms = {"self-harm", "violence"}
        return severity == "high" or any(term in content.lower() for term in flagged_terms)

    def check_license_compliance(self) -> bool:
        return True

    def enforce_license(self, response: dict[str, Any]) -> dict[str, Any]:
        info = self.license_manager.get_license_info()
        watermarked = dict(response)
        watermarked.setdefault("metadata", {})
        watermarked["metadata"].update(
            {
                "license_id": info["license_id"],
                "build_id": info["build_id"],
                "generation_time": datetime.now(UTC).isoformat(),
            }
        )
        return watermarked

    def audit_log(self, event: dict[str, Any]) -> None:
        pseudonymized = self.pseudonymize_event(event)
        self.audit_logger.log(pseudonymized)

    def pseudonymize_event(self, event: dict[str, Any]) -> dict[str, Any]:
        sanitized = dict(event)
        for field in ("user_id", "ip_address"):
            if field in sanitized:
                sanitized[field] = self._hash_value(str(sanitized[field]))
        return sanitized

    def _hash_value(self, value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()
