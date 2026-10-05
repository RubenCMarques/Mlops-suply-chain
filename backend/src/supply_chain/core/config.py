from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "local"
    hopsworks_host: str = ""
    hopsworks_project: str = ""
    hopsworks_api_key: SecretStr = SecretStr("")
    hopsworks_feature_view: str = ""
    hopsworks_feature_view_version: int = Field(default=1, ge=1)
    hopsworks_training_dataset_version: int | None = Field(default=None, ge=1)

    @property
    def hopsworks_configured(self) -> bool:
        return all(
            (
                self.hopsworks_host.strip(),
                self.hopsworks_project.strip(),
                self.hopsworks_api_key.get_secret_value().strip(),
                self.hopsworks_feature_view.strip(),
            )
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
