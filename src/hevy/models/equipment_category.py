"""Data models (pure data + validation)."""

from __future__ import annotations

from enum import Enum


class EquipmentCategory(str, Enum):
    """Equipment categories."""
    NONE = "none"
    BARBELL = "barbell"
    DUMBBELL = "dumbbell"
    KETTLEBELL = "kettlebell"
    MACHINE = "machine"
    PLATE = "plate"
    RESISTANCE_BAND = "resistance_band"
    SUSPENSION = "suspension"
    OTHER = "other"
