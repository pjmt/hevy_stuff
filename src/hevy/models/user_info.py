"""Data models (pure data + validation)."""

from __future__ import annotations

from pydantic import BaseModel


class UserInfo(BaseModel):
    """User information."""
    model_config = {"frozen": True}

    id: str
    name: str
    url: str
