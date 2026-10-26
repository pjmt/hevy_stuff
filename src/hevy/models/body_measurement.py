"""Data models (pure data + validation)."""

from __future__ import annotations

from pydantic import BaseModel


class BodyMeasurement(BaseModel):
    """Body measurement data."""
    model_config = {"frozen": True}

    date: str
    weight_kg: float
    lean_mass_kg: float
    fat_percentage: float
    neck_cm: float
    shoulder_cm: float
    chest_cm: float
    left_bicep_cm: float
    right_bicep_cm: float
    left_forearm_cm: float
    right_forearm_cm: float
    abdomen: float
    waist: float
    hips: float
    left_thigh: float
    right_thigh: float
    left_calf: float
    right_calf: float
