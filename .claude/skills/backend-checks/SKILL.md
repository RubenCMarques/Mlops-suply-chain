---
name: backend-checks
description: Run the same lint, format and test checks as CI for the supply-chain backend and fix failures. Use before committing backend changes or when the user asks to test, lint, or verify the backend.
---

# Backend checks

Mirrors `.github/workflows/ci.yml` and `pylint.yml` (Python 3.13, uv).

Run from `backend/`:
```bash
uv sync --extra dev
uv run ruff check src tests
uv run ruff format --check src tests
uv run pylint src
uv run pytest -q
```

## On failure
- Ruff: `uv run ruff check --fix src tests` and `uv run ruff format src tests`, then re-check.
- Pylint: fix the code; only disable a message inline with a reason if truly unavoidable.
- Pytest: read the failing assertion, fix code (not the test) unless the test encodes outdated behaviour, and say which.
- Tests must pass without Hopsworks credentials; use `Settings(_env_file=None, ...)` overrides.

Report the result of each command. Do not claim success for a step that was not run.
