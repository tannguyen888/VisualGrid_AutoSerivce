"""
Purpose:
- Centralized runtime settings for the automotive ETL pipeline.

Input:
- Environment variables.

Output:
- Typed settings object used by scheduler, sources, and loaders.

Responsibilities:
- Read scheduler timing and retry settings.
- Read source authentication and endpoint settings.
- Read database and object storage settings.

TODO implementation notes:
- Add secret manager integration for production deployments.
- Add source-specific rate limits and per-provider timeouts.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _build_postgres_url() -> str:
    explicit = os.getenv("POSTGRES_URL", "")
    if explicit:
        return explicit

    host = os.getenv("POSTGRES_HOST", "")
    db = os.getenv("POSTGRES_DB", "")
    if not host or not db:
        return ""

    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"


@dataclass(slots=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "dev")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    sync_cron_hour: int = int(os.getenv("PIPELINE_CRON_HOUR", "2"))
    sync_cron_minute: int = int(os.getenv("PIPELINE_CRON_MINUTE", "0"))
    max_retries: int = int(os.getenv("PIPELINE_MAX_RETRIES", "3"))
    retry_backoff_seconds: int = int(os.getenv("PIPELINE_RETRY_BACKOFF_SECONDS", "10"))

    vin_base_url: str = os.getenv("VIN_API_URL", "")
    vin_api_key: str = os.getenv("VIN_API_KEY", "")
    vehicle_base_url: str = os.getenv("VEHICLE_API_URL", "")
    vehicle_api_key: str = os.getenv("VEHICLE_API_KEY", "")
    parts_base_url: str = os.getenv("PARTS_API_URL", "")
    parts_api_key: str = os.getenv("PARTS_API_KEY", "")
    repair_base_url: str = os.getenv("REPAIR_API_URL", "")
    repair_api_key: str = os.getenv("REPAIR_API_KEY", "")
    document_base_url: str = os.getenv("DOCUMENT_API_URL", "")
    document_api_key: str = os.getenv("DOCUMENT_API_KEY", "")

    carapi_base_url: str = os.getenv("CARAPI_BASE_URL", "https://carapi.app")
    carapi_api_token: str = os.getenv("CARAPI_API_TOKEN", "")
    carapi_api_secret: str = os.getenv("CARAPI_API_SECRET", "")
    carapi_sync_makes: list[str] = field(
        default_factory=lambda: [
            m.strip() for m in os.getenv("CARAPI_SYNC_MAKES", "Toyota,Honda,Ford").split(",") if m.strip()
        ]
    )

    postgres_url: str = field(default_factory=_build_postgres_url)
    mongodb_url: str = os.getenv("MONGODB_URL", "")
    object_storage_root: str = os.getenv("OBJECT_STORAGE_ROOT", "./artifacts")

    dry_run: bool = _get_bool("PIPELINE_DRY_RUN", True)


settings = Settings()
