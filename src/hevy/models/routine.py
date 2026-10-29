"""Data models (pure data + validation)."""

from __future__ import annotations

from pydantic import BaseModel

from .exercise import Exercise


class Routine(BaseModel):
    """A routine consisting of several exercises."""
    model_config = {"frozen": True}

    id: str
    folder_id: int | None = None
    title: str
    updated_at: str
    created_at: str
    exercises: list[Exercise]
