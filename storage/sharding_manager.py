"""Sharding utilities for the Infinity AI storage layer."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ShardPlan:
    shard_id: int
    capacity: int
    replicas: int


class ShardingManager:
    def __init__(self, max_shards: int = 10, shard_size: int = 100_000) -> None:
        self.max_shards = max_shards
        self.shard_size = shard_size

    def plan_shards(self, total_items: int, replication_factor: int = 1) -> list[ShardPlan]:
        shards_needed = min(self.max_shards, (total_items // self.shard_size) + 1)
        return [
            ShardPlan(shard_id=index, capacity=self.shard_size, replicas=replication_factor)
            for index in range(shards_needed)
        ]


__all__ = ["ShardingManager", "ShardPlan"]
