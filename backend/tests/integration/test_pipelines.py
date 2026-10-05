from pathlib import Path
from unittest.mock import Mock

import pandas as pd
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project

from supply_chain.services import feature_store

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_smoke_runs_with_real_project_configuration(monkeypatch):
    monkeypatch.chdir(PROJECT_ROOT)
    bootstrap_project(PROJECT_ROOT)
    with KedroSession.create(project_path=PROJECT_ROOT) as session:
        result = session.run(pipeline_names=["smoke"])
    assert result["runtime_status"].load() == {"project": "Supply Chain", "status": "ok"}


def test_feature_snapshot_writes_parquet_with_mocked_remote_store(monkeypatch, tmp_path):
    monkeypatch.chdir(PROJECT_ROOT)
    bootstrap_project(PROJECT_ROOT)
    view = Mock()
    expected = pd.DataFrame({"sku": ["SKU-001"], "demand": [12]})
    view.get_batch_data.return_value = expected
    monkeypatch.setattr(feature_store, "get_feature_view", lambda settings: view)
    from kedro.io import DataCatalog
    from kedro.runner import SequentialRunner

    from supply_chain.pipeline_registry import register_pipelines

    output = tmp_path / "features.parquet"
    catalog = DataCatalog.from_config(
        {"feature_snapshot": {"type": "pandas.ParquetDataset", "filepath": str(output)}}
    )
    SequentialRunner().run(register_pipelines()["feature_snapshot"], catalog)
    pd.testing.assert_frame_equal(pd.read_parquet(output), expected)


def test_kaggle_ingestion_writes_raw_parquet_with_mocked_download(monkeypatch, tmp_path):
    monkeypatch.chdir(PROJECT_ROOT)
    bootstrap_project(PROJECT_ROOT)
    from kedro.runner import SequentialRunner
    from kedro_datasets.pandas import ParquetDataset

    from supply_chain.pipelines.ingestion import pipeline as ingestion

    with KedroSession.create(project_path=PROJECT_ROOT) as session:
        context = session.load_context()
    params = context.params["kaggle_ingestion"]
    orders = pd.DataFrame({column: [1] for column in params["orders"]["required_columns"]})
    descriptions = pd.DataFrame({"FIELDS": ["Type"], "DESCRIPTION": [":  Type of transaction"]})
    downloads = {
        params["orders"]["file_path"]: orders,
        params["descriptions"]["file_path"]: descriptions,
    }
    calls = []

    def fake_download(dataset, file_path, encoding):
        calls.append((dataset, file_path, encoding))
        return downloads[file_path]

    monkeypatch.setattr(ingestion, "load_kaggle_csv", fake_download)
    catalog = context.catalog
    outputs = {
        "dataco_orders_raw": tmp_path / "orders.parquet",
        "dataco_column_descriptions_raw": tmp_path / "descriptions.parquet",
    }
    for name, path in outputs.items():
        catalog[name] = ParquetDataset(filepath=str(path))

    SequentialRunner().run(ingestion.create_kaggle_pipeline(), catalog)

    assert sorted(calls) == sorted(
        (params["dataset"], table["file_path"], "latin-1")
        for table in (params["orders"], params["descriptions"])
    )
    pd.testing.assert_frame_equal(pd.read_parquet(outputs["dataco_orders_raw"]), orders)
    pd.testing.assert_frame_equal(
        pd.read_parquet(outputs["dataco_column_descriptions_raw"]), descriptions
    )
