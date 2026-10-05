import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pandas as pd
import pytest

from supply_chain.pipelines.ingestion.nodes import validate_raw_table
from supply_chain.services.kaggle import load_kaggle_csv


def test_valid_table_is_returned_unchanged():
    table = pd.DataFrame({"Order Id": [1], "Sales": [9.5]})
    assert validate_raw_table(table, ["Order Id"]) is table


@pytest.mark.parametrize(
    ("table", "message"),
    [
        (pd.DataFrame({"Order Id": []}), "no rows"),
        (pd.DataFrame([[1, 2]], columns=["Order Id", "Order Id"]), "duplicated columns"),
        (pd.DataFrame({"Sales": [1]}), r"missing required columns: \['Order Id'\]"),
    ],
)
def test_invalid_tables_are_rejected(table, message):
    with pytest.raises(ValueError, match=message):
        validate_raw_table(table, ["Order Id"])


def fake_kagglehub(monkeypatch, dataset_dir):
    download = Mock(return_value=str(dataset_dir))
    monkeypatch.setitem(sys.modules, "kagglehub", SimpleNamespace(dataset_download=download))
    return download


def test_kaggle_csv_is_read_from_cached_dataset_with_encoding(monkeypatch, tmp_path):
    (tmp_path / "data.csv").write_bytes("city\nSão Paulo\n".encode("latin-1"))
    download = fake_kagglehub(monkeypatch, tmp_path)
    result = load_kaggle_csv("owner/dataset", "data.csv", "latin-1")
    download.assert_called_once_with("owner/dataset")
    pd.testing.assert_frame_equal(result, pd.DataFrame({"city": ["São Paulo"]}))


def test_missing_kaggle_file_lists_available_files(monkeypatch, tmp_path):
    (tmp_path / "other.csv").write_text("a\n1\n")
    fake_kagglehub(monkeypatch, tmp_path)
    with pytest.raises(FileNotFoundError, match=r"Available files: \['other.csv'\]"):
        load_kaggle_csv("owner/dataset", "data.csv", "latin-1")


def test_kaggle_download_requires_a_file_name():
    with pytest.raises(ValueError, match="file_path"):
        load_kaggle_csv("owner/dataset", " ", "latin-1")
