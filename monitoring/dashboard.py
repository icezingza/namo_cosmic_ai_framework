"""Dashboard utilities for Infinity AI."""

from __future__ import annotations

from typing import Dict


class Dashboard:
    def __init__(self) -> None:
        self.widgets: Dict[str, Dict[str, str]] = {}

    def add_widget(self, name: str, config: Dict[str, str]) -> None:
        self.widgets[name] = config

    def render(self) -> Dict[str, Dict[str, str]]:
        return self.widgets


__all__ = ["Dashboard"]
