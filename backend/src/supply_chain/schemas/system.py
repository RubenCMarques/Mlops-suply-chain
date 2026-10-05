from typing import Literal

from pydantic import BaseModel


class FeatureStoreStatus(BaseModel):
    provider: str = "Hopsworks"
    configured: bool
    connection: Literal["not_checked"] = "not_checked"


class PipelineSummary(BaseModel):
    name: str
    nodes: int


class SystemStatus(BaseModel):
    service: str = "Supply Chain API"
    environment: str
    feature_store: FeatureStoreStatus
    pipelines: list[PipelineSummary]
