"""GeoPulse application configuration."""

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True, slots=True)
class Settings:
    """Configuration loaded from environment variables."""

    environment: str = "dev"


def load_settings() -> Settings:
    """Load application settings."""
    return Settings(environment=getenv("GEOPULSE_ENV", "dev"))
