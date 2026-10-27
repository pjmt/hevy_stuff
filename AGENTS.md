# Repository Guidelines

## Project Overview

`hevy` is a Python application for experimenting with Hevy fitness/workout-tracking data. It is a synchronous, layered application: `CLI` → `Service` → `Model`, with optional JSON persistence through `Repository`.

- Package: `hevy` (`src/hevy`)
- Version: `0.1.0` (`src/hevy/__init__.py`)
- Python: `>=3.11`
- Package manager / build: `uv` + `hatchling`
- CLI entry point: `hevy = "hevy.cli.main:app"` (`pyproject.toml`)
- CLI commands: `version`, `workouts`

## Architecture & Data Flow

### Layers

| Layer | Path | Purpose |
|---|---|---|
| CLI | `src/hevy/cli/` | Typer commands, user I/O, orchestration |
| Service | `src/hevy/services/` | Hevy API integration via `HevyClient` |
| Repository | `src/hevy/repositories/` | JSON persistence via `WorkoutRepository` |
| Model | `src/hevy/models/` | Immutable Pydantic domain objects |
| Config | `src/hevy/config.py` | Pydantic-Settings from `.env`/environment |

### Data flow

`CLI` → `HevyClient` → `httpx` → Hevy API → parsed `Workout` models → CLI output

Optional persistence:

`CLI/Service` → `WorkoutRepository.save()` → JSON file on disk  
`WorkoutRepository.load()` → `list[Workout]`

### Key modules

- `src/hevy/config.py`: `Settings` with `api_key`, `base_url`; module-global `settings`.
- `src/hevy/services/hevy_client.py`: `HevyClient` with constructor DI (`api_key`, `base_url`, `timeout`, `transport`, `client`), `list_workouts()`, and context-manager lifecycle.
- `src/hevy/repositories/workout_repository.py`: `WorkoutRepository.save()` / `load()`; serializes `id`, `title`, `sets` only.
- `src/hevy/models/`: frozen Pydantic v2 models; `Workout` validates `sets: int = Field(ge=0)`.

### Key patterns

- Constructor dependency injection for clients and transport.
- Frozen Pydantic `BaseModel`s for domain objects.
- Context managers for HTTP client closure.
- Boundary validation at service/model layer.
- Synchronous I/O only; no `asyncio`.

## Key Directories

| Directory | Purpose |
|---|---|
| `src/hevy/` | Application package |
| `src/hevy/cli/` | CLI entry points |
| `src/hevy/services/` | API integration |
| `src/hevy/repositories/` | JSON persistence |
| `src/hevy/models/` | Domain models |
| `tests/unit/` | Deterministic unit tests |

## Development Commands

```bash
# Setup
uv sync --extra dev

# Run CLI
uv run hevy version
uv run hevy workouts

# Quality
uv run pytest
uv run ruff check . --fix
uv run ruff format
uv run mypy .
uv build
```

Configuration comes from `.env` or environment with the `HEVY_` prefix (`HEVY_API_KEY`, `HEVY_BASE_URL`); no `.env.example` is committed.

## Code Conventions & Common Patterns

- Formatting/lint: Ruff, line length 100, target `py311`.
- Ruff rules: `E`, `F`, `I`, `UP`, `B`, `SIM`.
- Type checking: mypy strict, packages `hevy`, `mypy_path = src`.
- Modules `snake_case.py`; classes `PascalCase`; functions/variables `snake_case`; constants `UPPER_SNAKE`.
- Use modern union syntax (`X | None`) and built-in generics (`list[T]`).
- Services validate external data at boundaries; use `response.raise_for_status()` for API failures.
- Keep I/O synchronous; do not mix sync/async.
- Use constructor injection over global state.

## Important Files

- `pyproject.toml` — dependencies, scripts, tool configuration
- `src/hevy/cli/main.py` — CLI commands
- `src/hevy/services/hevy_client.py` — Hevy API client
- `src/hevy/repositories/workout_repository.py` — JSON persistence
- `src/hevy/config.py` — environment settings
- `src/hevy/models/workout.py` — primary domain model with validation

## Runtime/Tooling Preferences

- Runtime: Python `>=3.11`
- Package manager: `uv` (required)
- Build system: `hatchling`
- Tooling: `ruff` (lint/format), `mypy` (types), `pytest` (tests)
- Secrets: store in `.env` or OS keyring; never commit source.

## Testing & QA

- Framework: `pytest`; tests live in `tests/unit/`.
- Run: `uv run pytest` (addopts `-q`; testpaths `tests`).
- Mark tests requiring network/credentials with `@pytest.mark.integration`.
- Isolation: use `httpx.MockTransport` for HTTP and `tmp_path` for filesystem.
- Current tests cover config defaults/env parsing, client parsing/error propagation, repository round-trip/missing files, and model validation/frozen behavior.
- Tests must pass before commit; new features and bug fixes should include tests.

No integration test directory exists currently, despite the `integration` marker being declared.