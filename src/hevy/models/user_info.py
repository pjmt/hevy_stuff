"""Data models (pure data + validation)."""

from __future__ import annotations

from pydantic import BaseModel


class UserInfo(BaseModel):
    """User information."""
    model_config = {"frozen": True}

    id: str
    username: str
    name: str
    url: str
    weight_unit: str
    distance_unit: str
    is_pro: bool
