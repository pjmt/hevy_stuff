"""Data models (pure data + validation)."""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class Set(BaseModel):
    """A single set within an exercise."""
    model_config = {"frozen": True}

    index: int
    type: str
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[int] = None
    duration_seconds: Optional[int] = None
    rpe: Optional[float] = None
