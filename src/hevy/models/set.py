"""Data models (pure data + validation)."""

from __future__ import annotations

from pydantic import BaseModel


class Set(BaseModel):
    """A single set within an exercise."""
    model_config = {"frozen": True}

    index: int
    type: str
    weight_kg: float | None = None
    reps: int | None = None
    distance_meters: int | None = None
    duration_seconds: int | None = None
    rpe: float | None = None
    custom_metric: int | None = None
