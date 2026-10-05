from kedro.pipeline import Pipeline, node

from supply_chain.services.feature_store import read_batch_features


def create_pipeline() -> Pipeline:
    return Pipeline(
        [
            node(
                read_batch_features,
                inputs=None,
                outputs="feature_snapshot",
                name="read_hopsworks_features",
            )
        ]
    )
