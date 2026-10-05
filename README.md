# MLOps Supply Chain

Machine learning platform for supply chain workflows. A FastAPI backend serves the
API, Kedro runs the data and ML pipelines, Hopsworks provides the external feature
store, and a React (Vite) frontend displays the results.

```text
React / Vite -> FastAPI -> application services
                              |
Kedro pipelines -> Hopsworks feature view -> Parquet snapshot
```

## Repository layout

```text
backend/    FastAPI app, Kedro pipelines, tests (Python 3.13, uv)
frontend/   React app built with Vite, served by Nginx in production
deploy/     Kubernetes manifests and deployment guide
compose.yaml  Local stack with Docker Compose
```

## Prerequisites

- Python 3.13 and [uv](https://docs.astral.sh/uv/)
- Node.js 22.12 or newer
- Docker Desktop, for the containerised stack
- A Hopsworks account, only for feature-store pipelines

## Backend setup

Always run `uv` commands from the `backend` folder. The backend has its own
`pyproject.toml`, `uv.lock` and `.venv`. Running `uv sync` from the repository root
targets a different, empty project and fails with
`Extra 'dev' is not defined`.

If another virtual environment is active in your terminal, deactivate it first.

```powershell
deactivate
cd backend
uv sync --extra dev
.venv\Scripts\Activate.ps1
python --version
```

The last command should print Python 3.13. If `backend/.venv` was created with an
older Python, stop any running backend server, delete `backend/.venv` and run the
steps again.

Start the API:

```powershell
uvicorn supply_chain.api.main:app --reload
```

The API runs at http://127.0.0.1:8000, with documentation at `/docs`.

For Hopsworks credentials, copy `backend/.env.example` to `backend/.env` and fill
in your values. `.env` is ignored by Git. Never commit API keys to this repository.

See the [backend guide](backend/README.md) for Kedro pipelines, Hopsworks and checks.

## Frontend setup

In a second terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Vite serves the app at http://127.0.0.1:5173 and proxies API calls to the backend.
See the [frontend guide](frontend/README.md).

## Docker Compose

From the repository root, with Docker Desktop running:

```powershell
docker compose up --build -d
```

- Frontend: http://localhost:8080
- API documentation: http://localhost:8000/docs

Stop any local backend server first, because Compose also uses port 8000. See the
[deployment guide](deploy/README.md) for Compose and Kubernetes details.

## Contributing

The `develop` branch is protected. Direct pushes are blocked, so work on a feature
branch and open a pull request into `develop`. CI runs backend tests, Pylint, Ruff
and the frontend build on every push and pull request.
