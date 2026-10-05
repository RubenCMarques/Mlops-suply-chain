import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from supply_chain.core.config import Settings
from supply_chain.services import feature_store


def configured_settings(**overrides):
    return Settings(
        _env_file=None,
        hopsworks_host="features.example.com",
        hopsworks_project="test-project",
        hopsworks_api_key="test-key",
        hopsworks_feature_view="demand",
        hopsworks_feature_view_version=2,
        **overrides,
    )


def test_missing_configuration_fails_before_sdk_login(monkeypatch):
    login = Mock()
    monkeypatch.setitem(sys.modules, "hopsworks", SimpleNamespace(login=login))
    settings = Settings(_env_file=None, hopsworks_api_key="")
    with pytest.raises(ValueError, match="HOPSWORKS_API_KEY"):
        feature_store.get_feature_view(settings)
    login.assert_not_called()


def test_feature_view_uses_explicit_project_version_and_tls(monkeypatch):
    login = Mock()
    monkeypatch.setitem(sys.modules, "hopsworks", SimpleNamespace(login=login))
    result = feature_store.get_feature_view(configured_settings())
    login.assert_called_once_with(
        host="features.example.com",
        project="test-project",
        api_key_value="test-key",
        engine="python",
        hostname_verification=True,
    )
    store = login.return_value.get_feature_store.return_value
    store.get_feature_view.assert_called_once_with(name="demand", version=2)
    assert result is store.get_feature_view.return_value


@pytest.mark.parametrize("training_version", [None, 3])
def test_batch_read_initializes_statistics_only_when_configured(monkeypatch, training_version):
    settings = configured_settings(hopsworks_training_dataset_version=training_version)
    view = Mock()
    monkeypatch.setattr(feature_store, "get_settings", lambda: settings)
    monkeypatch.setattr(feature_store, "get_feature_view", lambda settings: view)
    assert feature_store.read_batch_features() is view.get_batch_data.return_value
    if training_version is None:
        view.init_batch_scoring.assert_not_called()
    else:
        view.init_batch_scoring.assert_called_once_with(training_dataset_version=3)
