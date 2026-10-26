"""Data models (pure data + validation)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Workout:
    """A Hevy workout summary."""

    id: str
    title: str
    sets: int

    def __post_init__(self) -> None:
        if self.sets < 0:
            raise ValueError("sets must be non-negative")