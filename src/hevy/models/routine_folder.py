"""Data models (pure data + validation)."""

from __future__ import annotations

from pydantic import BaseModel


class RoutineFolder(BaseModel):
    """A folder containing routines."""
    model_config = {"frozen": True}

    id: int
    index: int
    title: str
    updated_at: str
    created_at: str
