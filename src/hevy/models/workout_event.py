"""Data models (pure data + validation)."""

from __future__ import annotations

from pydantic import BaseModel
from .workout import Workout


class WorkoutEvent(BaseModel):
    """An event related to a workout."""
    model_config = {"frozen": True}

    id: str
    type: str
    workout: Workout
