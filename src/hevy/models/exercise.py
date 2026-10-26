"""Data models (pure data + validation)."""

from __future__ import annotations

from typing import List
from pydantic import BaseModel
from .set import Set


class Exercise(BaseModel):
    """An exercise within a routine or workout."""
    model_config = {"frozen": True}

    index: int
    title: str
    exercise_template_id: str
    notes: str
    superset_id: str
    sets: List[Set]
