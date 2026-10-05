from kedro.pipeline import Pipeline, node

from supply_chain.pipelines.ingestion.pipeline import create_kaggle_pipeline, create_pipeline
from supply_chain.pipelines.smoke.nodes import check_runtime


def register_pipelines() -> dict[str, Pipeline]:
    smoke = Pipeline(
        [node(check_runtime, "params:project_name", "runtime_status", name="check_runtime")]
    )
    return {
        "__default__": smoke,
        "smoke": smoke,
        "kaggle_ingestion": create_kaggle_pipeline(),
        "feature_snapshot": create_pipeline(),
    }
