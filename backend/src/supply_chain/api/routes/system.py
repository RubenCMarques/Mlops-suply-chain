from typing import Annotated

from fastapi import APIRouter, Depends

from supply_chain.core.config import Settings, get_settings
from supply_chain.pipeline_registry import register_pipelines
from supply_chain.schemas.system import FeatureStoreStatus, PipelineSummary, SystemStatus

router = APIRouter(prefix="/api/v1", tags=["System"])


@router.get("/status", response_model=SystemStatus)
def status(settings: Annotated[Settings, Depends(get_settings)]) -> SystemStatus:
    return SystemStatus(
        environment=settings.environment,
        feature_store=FeatureStoreStatus(configured=settings.hopsworks_configured),
        pipelines=[
            PipelineSummary(name=name, nodes=len(pipeline.nodes))
            for name, pipeline in register_pipelines().items()
            if name != "__default__"
        ],
    )
