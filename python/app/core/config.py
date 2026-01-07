from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "changethis"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Original config structure compatibility
    isInstalled: bool = False
    applicationName: str = "EspoCRM Python"
    applicationDescription: str = "EspoCRM – Open Source CRM application."
    useCache: bool = False
    isDeveloperMode: bool = True
    cacheTimestamp: int = 0
    appTimestamp: int = 0
    ajaxTimeout: int = 60000
    clientSecurityHeadersDisabled: bool = False
    clientCspDisabled: bool = False
    clientCspFormActionDisabled: bool = False
    clientXFrameOptionsHeaderDisabled: bool = False
    clientStrictTransportSecurityHeaderDisabled: bool = False
    siteUrl: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def set(self, key: str, value: Any):
        setattr(self, key, value)

    def is_installed(self) -> bool:
        return self.isInstalled

# Singleton instance
settings = Settings()

class Config:
    """Wrapper to maintain backward compatibility with previous Config class usage if needed."""
    def __init__(self):
        self._settings = settings

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def set(self, key: str, value: Any):
        self._settings.set(key, value)

    def is_installed(self) -> bool:
        return self._settings.is_installed()
