# Repository Guidelines

## Project Overview

`hevy` is a Python application designed for experiments and scripts relating to Hevy fitness/workout tracking data. The project implements a boring, explicit data flow (Input $\rightarrow$ Parse $\rightarrow$ Transform $\rightarrow$ Output) and strictly avoids global state to maintain a predictable and testable codebase.

## Architecture & Data Flow

The project follows a **Layered Service-Repository Architecture**.

### High-Level Structure
- **CLI Layer**: Orchestrates the application flow and handles user I/O via `typer`.
- **Service Layer**: Contains business logic and external API integration (`HevyClient`).
- **Repository Layer**: Manages local persistence via JSON files (`WorkoutRepository`).
- **Model Layer**: Defines domain objects as immutable, frozen dataclasses.

### Data Flow
`CLI` $\rightarrow$ `Service` $\rightarrow$ `Model` $\rightarrow$ `CLI`
*(Optional persistence: `Service` $\rightarrow$ `Repository` $\rightarrow$ `Disk`)*

### Key Patterns
- **Dependency Injection**: Services (e.g., `HevyClient`) accept configuration and transport objects in their constructors, enabling seamless mocking in unit tests.
- **Immutability**: Domain models are `frozen=True` dataclasses, ensuring a strict, read-only contract between layers.
- **Resource Management**: Clients implement context managers (`__enter__`/`__exit__`) to ensure HTTP session closure.

## Key Directories

| Directory | Purpose |
| :--- | :--- |
| `src/hevy/cli/` | Command-line entry points and orchestration. |
| `src/hevy/services/` | API integration logic and domain services. |
| `src/hevy/repositories/` | Local data persistence logic. |
| `src/hevy/models/` | Pure domain data models and validation. |
| `tests/unit/` | Isolated component tests (Models, Services, Repos). |
| `tests/integration/` | End-to-end flow tests (network/credential gated). |

## Development Commands

Managed via `uv`. All commands assume the environment is active or run via `uv run`.

```bash
# Run CLI
uv run hevy version            # Print package version
uv run hevy workouts           # List workouts from API

# Quality Assurance
uv run pytest                  # Run all tests
uv run ruff check . --fix       # Lint and auto-fix
uv run ruff format             # Format codebase
uv run mypy .                  # Static type checking

# Environment Management
uv venv                        # Create virtual environment
source .venv/bin/activate      # Activate environment
```

## Code Conventions & Common Patterns

- **Formatting**: Ruff (Line length: 100, Target: Python 3.11+).
- **Naming**: Modules `snake_case.py`, Classes `PascalCase`, Functions/Variables `snake_case`, Constants `UPPER_SNAKE`.
- **Error Handling**: Use domain-specific exceptions; avoid swallowing errors; validate external data at the Service boundary.
- **Async Patterns**: Use `asyncio` only for I/O-bound tasks; avoid mixing sync/async without a clear boundary.
- **State Management**: Pass configuration via `hevy.config.settings` (Pydantic) and dependencies via constructors.

## Important Files

- **Entry Point**: `src/hevy/cli/main.py` ($\rightarrow$ `hevy` command).
- **Config**: `src/hevy/config.py` (Pydantic settings from `.env` with `HEVY_` prefix).
- **Manifest**: `pyproject.toml` (Dependencies, tool config, entry points).
- **Tooling**: `.gitignore` (Standard Python/uv exclusions).

## Runtime/Tooling Preferences

- **Runtime**: Python $\ge$ 3.11 (Local baseline: 3.14).
- **Package Manager**: `uv` (Required).
- **Build System**: `hatchling`.
- **Tooling**: `ruff` (lint/format), `mypy` (types), `pytest` (testing).
- **Secrets**: MUST be stored in `.env` or the OS keyring; never committed to source.

## Testing & QA

### Framework & Expectations
- **Framework**: `pytest`
- **Isolation**: All unit tests must be deterministic and isolated.
- **Mocking**: 
  - Use `httpx.MockTransport` for API isolation (do not use `unittest.mock` for HTTP).
  - Use `tmp_path` for filesystem isolation.
- **Boundaries**:
  - Unit tests (`tests/unit/`) focus on logic and parsing.
  - Integration tests (`tests/integration/`) validate actual network/disk flows; mark with `@pytest.mark.integration`.

### Verification
- Tests must pass (`uv run pytest`) before any commit.
- All new features MUST include a corresponding unit test.
- Regression tests are required for every bug fix.