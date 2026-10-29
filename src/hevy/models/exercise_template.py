"""Data models (pure data + validation)."""

from __future__ import annotations

from pydantic import BaseModel

from .equipment_category import EquipmentCategory


class ExerciseTemplate(BaseModel):
    """An exercise template."""
    model_config = {"frozen": True}

    id: str
    title: str
    type: str
    primary_muscle_group: str
    secondary_muscle_groups: list[str]
    equipment: EquipmentCategory
    is_custom: bool
    thumbnail_url: str | None = None
