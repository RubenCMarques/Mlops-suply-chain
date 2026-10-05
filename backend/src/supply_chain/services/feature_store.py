from typing import Any

from supply_chain.core.config import Settings, get_settings


def get_feature_view(settings: Settings | None = None) -> Any:
    settings = settings or get_settings()
    if not settings.hopsworks_configured:
        raise ValueError(
            "Set HOPSWORKS_HOST, HOPSWORKS_PROJECT, HOPSWORKS_API_KEY, "
            "and HOPSWORKS_FEATURE_VIEW before accessing the feature store."
        )

    # Keep SDK initialization and remote access out of API imports and health checks.
    try:
        import hopsworks
    except ModuleNotFoundError as error:
        if error.name != "hopsworks":
            raise
        raise RuntimeError(
            "Install the Hopsworks extra with 'uv sync --extra hopsworks' "
            "or run this pipeline in the backend Docker image."
        ) from error

    project = hopsworks.login(
        host=settings.hopsworks_host,
        project=settings.hopsworks_project,
        api_key_value=settings.hopsworks_api_key.get_secret_value(),
        engine="python",
        hostname_verification=True,
    )
    return project.get_feature_store().get_feature_view(
        name=settings.hopsworks_feature_view,
        version=settings.hopsworks_feature_view_version,
    )


def read_batch_features() -> Any:
    settings = get_settings()
    feature_view = get_feature_view(settings)
    if settings.hopsworks_training_dataset_version is not None:
        feature_view.init_batch_scoring(
            training_dataset_version=settings.hopsworks_training_dataset_version
        )
    return feature_view.get_batch_data()
