"""Dashboard utilities for Infinity AI."""

from __future__ import annotations


class Dashboard:
    def __init__(self) -> None:
        self.widgets: dict[str, dict[str, str]] = {}

    def add_widget(self, name: str, config: dict[str, str]) -> None:
        self.widgets[name] = config

    def render(self) -> dict[str, dict[str, str]]:
        return self.widgets


__all__ = ["Dashboard"]
