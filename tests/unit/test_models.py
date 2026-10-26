"""Tests for hevy models."""

from dataclasses import FrozenInstanceError

import pytest

from hevy.models.workout import Workout


def test_workout_fields() -> None:
    w = Workout(id="1", title="Chest", sets=3)
    assert w.id == "1"
    assert w.title == "Chest"
    assert w.sets == 3


def test_workout_validation_rejects_negative_sets() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        Workout(id="1", title="Chest", sets=-1)


def test_workout_zero_sets_allowed() -> None:
    assert Workout(id="1", title="Rest", sets=0).sets == 0


def test_workout_is_frozen() -> None:
    w = Workout(id="1", title="Chest", sets=3)
    with pytest.raises(FrozenInstanceError):
        w.sets = 4  # type: ignore[misc]