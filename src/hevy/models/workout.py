"""Data models (pure data + validation)."""

from __future__ import annotations

from typing import List
from pydantic import BaseModel
from .exercise import Exercise


class Workout(BaseModel):
    """A workout."""
    model_config = {"frozen": True}

    id: str
    title: str
    sets: int = 0
    routine_id: str | None = None
    description: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    updated_at: str | None = None
    created_at: str | None = None
    exercises: List[Exercise] = []
