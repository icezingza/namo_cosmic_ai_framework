"""Vector database abstraction for Infinity AI."""

from __future__ import annotations

from typing import Dict, List

import numpy as np


class VectorDatabase:
    def __init__(self, dimensions: int = 384) -> None:
        self.dimensions = dimensions
        self._vectors: Dict[str, np.ndarray] = {}

    def upsert(self, key: str, vector: np.ndarray) -> None:
        if vector.shape[0] != self.dimensions:
            raise ValueError("Vector dimensionality mismatch")
        self._vectors[key] = vector

    def search(self, vector: np.ndarray, top_k: int = 5) -> List[str]:
        if not self._vectors:
            return []
        scores: List[tuple[str, float]] = []
        for key, stored in self._vectors.items():
            similarity = float(np.dot(vector, stored))
            scores.append((key, similarity))
        scores.sort(key=lambda item: item[1], reverse=True)
        return [key for key, _ in scores[:top_k]]


__all__ = ["VectorDatabase"]
