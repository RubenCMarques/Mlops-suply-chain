from kedro.pipeline import Pipeline, node

from supply_chain.pipelines.ingestion.nodes import validate_raw_table
from supply_chain.services.feature_store import read_batch_features
from supply_chain.services.kaggle import load_kaggle_csv

KAGGLE_TABLES = {
    "orders": "dataco_orders_raw",
    "descriptions": "dataco_column_descriptions_raw",
}


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


def create_kaggle_pipeline() -> Pipeline:
    """Download the DataCo supply chain dataset from Kaggle into the raw data layer."""
    nodes = []
    for table, output in KAGGLE_TABLES.items():
        params = f"params:kaggle_ingestion.{table}"
        nodes += [
            node(
                load_kaggle_csv,
                inputs={
                    "dataset": "params:kaggle_ingestion.dataset",
                    "file_path": f"{params}.file_path",
                    "encoding": f"{params}.encoding",
                },
                outputs=f"{output}_download",
                name=f"download_{table}",
            ),
            node(
                validate_raw_table,
                inputs=[f"{output}_download", f"{params}.required_columns"],
                outputs=output,
                name=f"validate_{table}",
            ),
        ]
    return Pipeline(nodes)
