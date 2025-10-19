"""Registry for cross-dimensional data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CosmicRecord:
    identifier: str
    payload: dict[str, str]
    signature: str


class CosmicRegistry:
    def __init__(self) -> None:
        self._records: dict[str, CosmicRecord] = {}

    def register(self, identifier: str, payload: dict[str, str], signature: str) -> CosmicRecord:
        record = CosmicRecord(identifier, payload, signature)
        self._records[identifier] = record
        return record

    def get(self, identifier: str) -> CosmicRecord | None:
        return self._records.get(identifier)


__all__ = ["CosmicRegistry", "CosmicRecord"]
