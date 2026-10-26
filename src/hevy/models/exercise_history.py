"""Data models (pure data + validation)."""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel
from .set import Set


class ExerciseHistoryEntry(BaseModel):
    """An entry in the exercise history."""
    model_config = {"frozen": True}

    workout_id: str
    workout_title: str
    workout_start_time: str
    workout_end_time: str
    exercise_template_id: str
    weight_kg: Optional[int] = None
    reps: Optional[int] = None
    distance_meters: Optional[int] = None
    duration_seconds: Optional[int] = None
    rpe: Optional[float] = None
    set_type: str
    sets: List[Set]
