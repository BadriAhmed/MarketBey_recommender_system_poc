import logging
import os

from pydantic import BaseSettings, Field


class ServerConfig(BaseSettings):
    SERVER_HOST: str = Field(default="0.0.0.0", description="Host of the application", env="SERVER_HOST")
    SERVER_PORT: int = Field(default=8000, description="Port of the application", env="SERVER_PORT")


ServerSettings = ServerConfig()


class LoggingConfiguration(BaseSettings):
    LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
    JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


LoggingSettings = LoggingConfiguration()
