"""JSON file persistence for workouts."""

from __future__ import annotations

import json
from pathlib import Path

from hevy.models.workout import Workout


class WorkoutRepository:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    def save(self, workouts: list[Workout]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = [{"id": w.id, "title": w.title, "sets": w.sets} for w in workouts]
        self.path.write_text(json.dumps(data, indent=2))

    def load(self) -> list[Workout]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text())
        return [Workout(id=item["id"], title=item["title"], sets=item["sets"]) for item in data]