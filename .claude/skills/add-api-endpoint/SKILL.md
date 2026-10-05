---
name: add-api-endpoint
description: Add a new FastAPI endpoint to the supply-chain backend (route, Pydantic schema, router registration, integration test). Use when the user asks to add, expose, or change an API route, e.g. predictions, forecasts, inventory, or model info endpoints.
---

# Add an API endpoint

The backend API lives in `backend/src/supply_chain/`. Follow the existing layout exactly.

## Layout
- `api/main.py` — `create_app()` builds the app and calls `include_router` for each router.
- `api/routes/<name>.py` — one `APIRouter` per domain. Business routes use `prefix="/api/v1"` and a `tags=[...]` value. Health routes have no prefix.
- `schemas/<name>.py` — Pydantic v2 `BaseModel` request/response models. Never return raw dicts from business routes.
- `services/<name>.py` — logic that talks to models, Kedro, or Hopsworks. Routes stay thin.
- `core/config.py` — `Settings` (pydantic-settings) and `get_settings()`. Inject with `Annotated[Settings, Depends(get_settings)]`.

## Steps
1. Create the schema in `schemas/<domain>.py` with explicit types (`Literal`, `list[...]`, `Field(..., ge=0)` for validation).
2. Put logic in `services/<domain>.py` as plain functions or a class; make it testable without network or credentials.
3. Create `api/routes/<domain>.py`:
   ```python
   from typing import Annotated
   from fastapi import APIRouter, Depends, HTTPException
   from supply_chain.core.config import Settings, get_settings
   from supply_chain.schemas.<domain> import <Request>, <Response>

   router = APIRouter(prefix="/api/v1", tags=["<Domain>"])

   @router.post("/<path>", response_model=<Response>)
   def handler(body: <Request>, settings: Annotated[Settings, Depends(get_settings)]) -> <Response>:
       ...
   ```
4. Register the router in `api/main.py` with `application.include_router(<domain>.router)`.
5. Add a test in `backend/tests/integration/test_<domain>.py` using `TestClient(create_app())` and `app.dependency_overrides[get_settings]` with `Settings(_env_file=None, ...)` so it runs without secrets. Unit-test the service in `tests/unit/`.
6. Never put secrets (e.g. `hopsworks_api_key`) in responses; assert they are absent.
7. Run the `backend-checks` skill before finishing.

## Conventions
- Python 3.13, line length 100, ruff rules E/F/I/UP.
- Return HTTP 422 via Pydantic validation, 404/409 via `HTTPException`, 503 when a model or feature store is unavailable.
- If the frontend consumes it, update the frontend API client too.
