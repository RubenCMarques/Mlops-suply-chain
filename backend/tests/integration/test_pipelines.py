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
