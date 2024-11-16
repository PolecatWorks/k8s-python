

from k8spython.hams.config import HamsConfig
from pydantic import Field, BaseModel
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, YamlConfigSettingsSource, SettingsConfigDict
from pydantic_file_secrets import FileSecretsSettingsSource
from pathlib import Path
from typing import List, Dict, Any, Self


# TODO: Look here in future: https://github.com/pydantic/pydantic/discussions/2928#discussioncomment-4744841
class WebServerConfig(BaseModel):
    """
    Configuration for the web server
    """
    url: HttpUrl = Field(description="Host to listen on")
    prefix: str = Field(description="Prefix for the name of the resources")


class ChromaConfig(BaseModel):
    """
    Configuration for ChromaDB
    """
    url: HttpUrl = Field(description="ChromaDB host URL")
    apikey: str = Field(description="Api Key")


class ServiceConfig(BaseSettings):
    """
    Configuration for the service
    """
    webservice: WebServerConfig = Field(description="Web server configuration")
    hams: HamsConfig = Field(description="Health and monitoring configuration")
    chroma: ChromaConfig = Field(description="Chroma configuration")

    model_config = SettingsConfigDict(
        # secrets_dir='/run/secrets',
        secrets_nested_subdir=True,
    )

    @classmethod
    def from_yaml(cls, path: Path) -> Self:
        return cls(**YamlConfigSettingsSource(cls, path)(), _secrets_dir="/Users/bengreene/Development/polecatworks/k8s-python/container/tests/test_data/secrets")


    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            FileSecretsSettingsSource(file_secret_settings),
        )
