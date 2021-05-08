import os
from typing import Any, List, Dict

import toml
from pydantic import (
    BaseSettings,
    BaseModel,
    HttpUrl,
    DirectoryPath,
    FilePath
)

def toml_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """
    A simple settings source that loads variables from a TOML file
    """
    with open(os.environ.get('FEED_GENERATOR_CONFIG', 'config.toml'), 'r') as f:
        return toml.load(f)

class FeedModel(BaseModel):
    url: HttpUrl
    name: str

class Settings(BaseSettings):
    base_dir: DirectoryPath
    urls: FilePath

    class Config:
        env_prefix = 'FEED_GENERATOR_'
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                env_settings,
                toml_config_settings_source,
                file_secret_settings,
            )
