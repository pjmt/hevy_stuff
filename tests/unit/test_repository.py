"""Tests for WorkoutRepository."""

from pathlib import Path

from hevy.models.workout import Workout
from hevy.repositories.workout_repository import WorkoutRepository


def test_save_load_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "w.json"
    repo = WorkoutRepository(path)
    data = [Workout(id="1", title="Chest", sets=3)]
    repo.save(data)
    assert repo.load() == data


def test_load_missing_returns_empty(tmp_path: Path) -> None:
    repo = WorkoutRepository(tmp_path / "nope.json")
    assert repo.load() == []


def test_save_creates_parent_dir(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "w.json"
    repo = WorkoutRepository(path)
    repo.save([])
    assert path.exists()