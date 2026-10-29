"""Tests for Hevy domain models."""

import pytest
from pydantic import ValidationError

from hevy.models import (
    BodyMeasurement,
    EquipmentCategory,
    Exercise,
    ExerciseHistoryEntry,
    ExerciseTemplate,
    Routine,
    RoutineFolder,
    Set,
    UserInfo,
    Workout,
    WorkoutEvent,
)


def test_user_info_valid():
    u = UserInfo(
        id="u1",
        username="testuser",
        name="Test User",
        url="http://example.com",
        weight_unit="kg",
        distance_unit="km",
        is_pro=False,
    )
    assert u.name == "Test User"

def test_exercise_valid():
    s = Set(index=1, type="working")
    e = Exercise(
        index=1, 
        title="Bench Press", 
        exercise_template_id="et1", 
        notes="", 
        superset_id=None, 
        sets=[s]
    )
    assert e.title == "Bench Press"

def test_set_valid():
    s = Set(index=1, type="working", weight_kg=100.0, reps=10)
    assert s.weight_kg == 100.0
    assert s.reps == 10

def test_routine_valid():
    s = Set(index=1, type="working")
    e = Exercise(
        index=1, 
        title="Bench Press", 
        exercise_template_id="et1", 
        notes="", 
        superset_id=None, 
        sets=[s]
    )
    r = Routine(
        id="r1", 
        folder_id=1, 
        title="Push Day", 
        updated_at="2026-01-01", 
        created_at="2026-01-01", 
        exercises=[e]
    )
    assert r.title == "Push Day"

def test_routine_folder_valid():
    rf = RoutineFolder(
        id=1, 
        index=1, 
        title="Workouts", 
        updated_at="2026-01-01", 
        created_at="2026-01-01"
    )
    assert rf.title == "Workouts"

def test_exercise_template_valid():
    et = ExerciseTemplate(
        id="et1", 
        title="Squat", 
        type="compound", 
        primary_muscle_group="Legs", 
        secondary_muscle_groups=[], 
        equipment=EquipmentCategory.DUMBBELL, 
        is_custom=False
    )
    assert et.title == "Squat"

def test_body_measurement_valid():
    bm = BodyMeasurement(
        date="2026-01-01",
        weight_kg=80.5,
        lean_mass_kg=60.0,
        fat_percentage=25.0,
        neck_cm=38.0,
        shoulder_cm=110.0,
        chest_cm=100.0,
        left_bicep_cm=35.0,
        right_bicep_cm=35.0,
        left_forearm_cm=30.0,
        right_forearm_cm=30.0,
        abdomen=85.0,
        waist=80.0,
        hips=95.0,
        left_thigh=55.0,
        right_thigh=55.0,
        left_calf=38.0,
        right_calf=38.0
    )
    assert bm.weight_kg == 80.5

def test_workout_event_valid():
    w = Workout(id="w1", title="Chest", sets=10)
    we = WorkoutEvent(id="we1", type="start", workout=w)
    assert we.type == "start"

def test_exercise_history_valid():
    s = Set(index=1, type="working")
    eh = ExerciseHistoryEntry(
        workout_id="w1",
        workout_title="T",
        workout_start_time="S",
        workout_end_time="E",
        exercise_template_id="et1",
        set_type="type",
        sets=[s]
    )
    assert eh.exercise_template_id == "et1"

def test_equipment_category_valid():
    ec = EquipmentCategory.DUMBBELL
    assert ec.name == "DUMBBELL"

def test_models_are_frozen():
    m = Workout(id="1", title="t", sets=10)
    with pytest.raises(ValidationError):
        m.id = "2" # type: ignore

def test_workout_validation_rejects_negative_sets():
    with pytest.raises(ValidationError):
        Workout(id="1", title="Chest", sets=-1)

def test_workout_zero_sets_allowed():
    assert Workout(id="1", title="Rest", sets=0).sets == 0

def test_workout_fields():
    w = Workout(id="1", title="Chest", sets=3)
    assert w.id == "1"
    assert w.title == "Chest"
    assert w.sets == 3
