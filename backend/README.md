# Backend

Python backend for the supply chain MLOps solution. The intended entry point for
the frontend is an HTTP API. This is the initial repository structure; application
logic and framework integrations have not been implemented yet.

## Layout

```text
backend/
|-- src/supply_chain/
|   |-- api/
|   |   `-- routes/       # HTTP endpoints
|   |-- core/             # Application settings and logging
|   |-- schemas/          # Request and response definitions
|   |-- services/         # Application logic used by API routes
|   |-- pipelines/
|   |   |-- ingestion/    # Load and validate source data
|   |   |-- preprocessing/ # Shared data transformations
|   |   |-- training/     # Fit models
|   |   |-- evaluation/   # Evaluate and compare models
|   |   `-- inference/    # Generate predictions
|   `-- monitoring/       # Data drift and model performance
|-- config/
|   |-- base/             # Shared, non-sensitive configuration
|   `-- local/            # Ignored developer configuration
|-- data/
|   |-- raw/              # Original source data
|   |-- processed/        # Cleaned data and features
|   `-- predictions/      # Batch prediction output
|-- models/               # Local model and preprocessing artifacts
|-- notebooks/            # Exploration and experiments
|-- tests/
|   |-- unit/             # Pipeline and service tests
|   `-- integration/      # API and external-system tests
`-- pyproject.toml        # Backend package and dependencies
```

## Responsibilities

API routes handle HTTP requests and responses. Services coordinate application
logic and call inference code. Pipelines own data preparation, model training,
evaluation, and prediction. Keep reusable transformations shared between training
and inference so the same input processing is used in both.

Run training separately from interactive prediction requests. An API may later
submit training jobs to an orchestrator and return their status.

The illustrative bank project informs the separation of pipelines, configuration,
data, and tests. It is not a dependency of this backend. API, orchestration, and
experiment tracking frameworks will be selected and configured when implemented.

## Development

Use Python 3.12 or newer, matching the root project's Python requirement. Backend
dependencies belong in this folder's `pyproject.toml`. The root starter manifest
remains separate.

To install this package locally from the repository root in PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

There is no server command or executable ML workflow yet. The first implementation
step is to define the prediction input/output contract and add the API application.

Git tracks the empty directory placeholders but ignores local datasets, models,
and developer configuration. Dataset and model versioning are future MLOps work.

The [frontend](../frontend/README.md) will communicate with this backend over HTTP.
