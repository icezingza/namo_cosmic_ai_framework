"""Utility for generating capacity plans."""

from __future__ import annotations

import argparse

from monitoring.capacity_planner import CapacityPlanner


def parse_loads(load_values: str) -> list[int]:
    return [int(value) for value in load_values.split(",") if value]


def main() -> None:
    parser = argparse.ArgumentParser(description="Capacity planning tool")
    parser.add_argument("loads", help="Comma separated list of historical loads")
    args = parser.parse_args()

    planner = CapacityPlanner()
    plan = planner.plan(parse_loads(args.loads))
    print(f"Projected load: {plan.projected_load}")
    print(f"Recommended instances: {plan.recommended_instances}")
    print(f"Notes: {plan.notes}")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
