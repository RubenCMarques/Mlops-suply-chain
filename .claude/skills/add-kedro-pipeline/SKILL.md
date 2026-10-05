---
name: add-kedro-pipeline
description: Create or extend a Kedro pipeline in the supply-chain backend (ingestion, preprocessing, training, evaluation, inference). Use when the user asks for a new ML pipeline, node, dataset in the catalog, or model training step.
---

# Add a Kedro pipeline

Kedro package: `backend/src/supply_chain/pipelines/`. Config: `backend/config/base/` (`catalog.yml`, `parameters.yml`). Secrets go in `backend/config/local/` (git-ignored), never in base.

## Steps
1. In `pipelines/<name>/` create:
   - `nodes.py` — pure functions, typed, no I/O. Inputs/outputs are DataFrames, dicts, or models.
   - `pipeline.py` — `def create_pipeline(**kwargs) -> Pipeline:` returning `Pipeline([node(func, inputs, outputs, name="...")])`.
2. Declare every persisted dataset in `config/base/catalog.yml` (e.g. `pandas.ParquetDataset` under `data/processed/`, models under `models/`). Use `params:<key>` for parameters from `parameters.yml`.
3. Register it in `pipeline_registry.py` by adding `"<name>": <name>_pipeline.create_pipeline()` to the returned dict. Decide whether it joins `__default__`.
4. Note: `tests/integration/test_api.py` asserts the exact set of pipeline names from `/api/v1/status`. Update that set when adding a pipeline.
5. Add unit tests for nodes in `backend/tests/unit/` and a run test in `tests/integration/test_pipelines.py`.
6. Run locally from `backend/`:
   ```bash
   uv run kedro run --pipeline <name>
   ```
7. Run the `backend-checks` skill.

## ML conventions
- Training nodes return the fitted model plus a metrics dict; evaluation compares against a threshold from parameters.
- Inference pipeline must use the same preprocessing nodes as training so the API serves consistent features.
- Hopsworks access goes through `services/feature_store.py` and must degrade gracefully when not configured.
