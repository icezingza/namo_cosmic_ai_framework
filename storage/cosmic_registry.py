"""Registry for cross-dimensional data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class CosmicRecord:
    identifier: str
    payload: Dict[str, str]
    signature: str


class CosmicRegistry:
    def __init__(self) -> None:
        self._records: Dict[str, CosmicRecord] = {}

    def register(self, identifier: str, payload: Dict[str, str], signature: str) -> CosmicRecord:
        record = CosmicRecord(identifier, payload, signature)
        self._records[identifier] = record
        return record

    def get(self, identifier: str) -> Optional[CosmicRecord]:
        return self._records.get(identifier)


__all__ = ["CosmicRegistry", "CosmicRecord"]
