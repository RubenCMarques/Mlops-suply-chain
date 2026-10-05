# Backend

FastAPI serves the HTTP API, Kedro runs data workflows, and Hopsworks provides the
external feature store. Python 3.12 is the development and container baseline.

## Development

From this directory:

```powershell
uv sync --frozen --extra dev
uv run --frozen --extra dev uvicorn supply_chain.api.main:app --reload
```

The API is available at http://127.0.0.1:8000, with interactive documentation at
`/docs`. Use a second terminal for the frontend.

| Route | Purpose |
| --- | --- |
| `GET /health/live` | Process health, without external requests |
| `GET /health/ready` | Readiness for the currently implemented endpoints |
| `GET /api/v1/status` | Environment, registered pipelines, feature-store configuration status |

There is no trained model or prediction endpoint yet. Readiness currently covers
the status API; add model-loading checks when implementing prediction serving.
Hopsworks configuration status does not establish remote connectivity.

## Kedro

```powershell
uv run --frozen --extra dev kedro run --pipelines smoke
```

The default pipeline is also `smoke`. It checks project configuration and executes
a real Kedro node without external services. `feature_snapshot` reads an existing
Hopsworks feature view into `data/processed/features.parquet`.

```text
src/supply_chain/
|-- api/                  FastAPI application and routes
|-- core/                 Environment-based settings
|-- schemas/              HTTP response contracts
|-- services/             Hopsworks adapter and future model services
|-- pipeline_registry.py  Named Kedro pipelines
|-- settings.py           Kedro configuration source
|-- pipelines/
|   |-- smoke/            Local runtime check
|   |-- ingestion/        Hopsworks feature snapshot
|   |-- preprocessing/   Reserved for feature transformations
|   |-- training/        Reserved for model training
|   |-- evaluation/      Reserved for model evaluation
|   `-- inference/       Reserved for predictions
`-- monitoring/          Reserved for drift and model performance checks
```

Kedro reads `config/base/catalog.yml` and `parameters.yml`. Developer overrides go
in the ignored `config/local/` folder. The bank example is only a reference.

## Hopsworks

Copy `.env.example` to `.env`, then set the host, project, API key, feature-view
name, and version for an existing Hopsworks project. Never put keys in frontend
configuration. Settings read `.env` from the backend working directory; process
environment variables take precedence.

The optional SDK group targets Hopsworks 5.0.x. Match this SDK major version to
your Hopsworks server before connecting. The adapter uses explicit credentials,
the Python engine, and TLS hostname verification. It does not create or modify
remote feature groups or views.

```powershell
uv sync --frozen --extra dev --extra hopsworks
uv run --frozen --extra dev --extra hopsworks kedro run --pipelines feature_snapshot
```

On Windows, the SDK's `twofish` dependency needs Microsoft C++ Build Tools.
The backend Docker image includes the SDK and builds native dependencies in its
Linux build stage, so Docker is an alternative for feature-store jobs:

```powershell
# From the repository root, after starting Docker Desktop:
docker compose build backend
docker compose run --rm backend kedro run --pipelines feature_snapshot
```

The Compose data volume retains the snapshot after the job exits. The snapshot is
a batch feature export, not a versioned training dataset. Define labels, entity
keys, splits, and point-in-time training datasets once the ML use case is known.
If the feature view uses fitted transformations, set
`HOPSWORKS_TRAINING_DATASET_VERSION` to the matching training dataset version.

See the official [Hopsworks login API](https://docs.hopsworks.ai/latest/python-api/hopsworks/)
and [feature-view API](https://docs.hopsworks.ai/latest/python-api/hsfs/feature_view/).

## Verification and CI

```powershell
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev pylint src/supply_chain
uv run --frozen --extra dev ruff check src tests
uv run --frozen --extra dev ruff format --check src tests
```

Tests exercise the real Kedro configuration, Parquet output, and HTTP routes.
Hopsworks network calls are mocked; CI requires no Hopsworks credentials.

The [CI workflow](../.github/workflows/ci.yml) runs backend tests and the React
production build. The [Pylint workflow](../.github/workflows/pylint.yml) runs
Pylint, Ruff, and formatting checks. Both run on pushes, pull requests, and manual
dispatch. Python 3.12 and Node.js 22 match the containers.
Dependencies are installed from the committed lockfiles. Pylint checks application
code; Ruff also checks tests. Missing-docstring style checks are disabled to match
the current code style; other Pylint diagnostics fail the job.

The checked-in `uv.lock` is shared by local development and Docker builds.
See [deployment instructions](../deploy/README.md) for Compose and Kubernetes.
