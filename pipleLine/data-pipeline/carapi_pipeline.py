"""
Purpose:
- Orchestrate the real CarAPI -> Postgres sync: fetch years/makes/models,
  validate shape, and upsert into car_year/car_make/car_model.

Input:
- Runtime trigger (called directly or by SyncScheduler on a fixed cron time).

Output:
- CarApiSyncResult with counts, used for logging/alerting.

Responsibilities:
- Keep this idempotent and safe to run repeatedly on a schedule.

TODO implementation notes:
- Sync all makes instead of settings.carapi_sync_makes once rate limits allow.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from config import settings
from loader.carapi_loader import CarApiLoader
from sources.carapi_source import CarApiSource

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class CarApiSyncResult:
    success: bool
    years_synced: int
    makes_synced: int
    models_synced: int
    error_count: int


def _validate_make(make: dict) -> bool:
    return isinstance(make.get("id"), int) and bool(make.get("name"))


def _validate_model(model: dict) -> bool:
    return isinstance(model.get("id"), int) and bool(model.get("name"))


def run_carapi_sync() -> CarApiSyncResult:
    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))

    if not settings.carapi_api_token or not settings.carapi_api_secret:
        raise ValueError("CARAPI_API_TOKEN / CARAPI_API_SECRET must be set to run the CarAPI sync")

    source = CarApiSource(
        base_url=settings.carapi_base_url,
        api_token=settings.carapi_api_token,
        api_secret=settings.carapi_api_secret,
    )
    loader = CarApiLoader()

    error_count = 0
    years_synced = 0
    makes_synced = 0
    models_synced = 0

    try:
        years = source.fetch_years()
        years_synced = loader.upsert_years(years)
    except Exception:
        LOGGER.exception("CarAPI years sync failed")
        error_count += 1
        years = []

    valid_makes: list[dict] = []
    try:
        makes = source.fetch_makes()
        valid_makes = [m for m in makes if _validate_make(m)]
        if len(valid_makes) != len(makes):
            LOGGER.warning("Dropped %s invalid make records", len(makes) - len(valid_makes))
        makes_synced = loader.upsert_makes(valid_makes)
    except Exception:
        LOGGER.exception("CarAPI makes sync failed")
        error_count += 1

    target_makes = [m for m in valid_makes if m["name"] in settings.carapi_sync_makes]
    for make in target_makes:
        for year in years:
            try:
                models = source.fetch_models(year=year, make_id=make["id"])
                valid_models = [m for m in models if _validate_model(m)]
                models_synced += loader.upsert_models(valid_models, year=year)
            except Exception:
                LOGGER.exception("CarAPI models sync failed make=%s year=%s", make["name"], year)
                error_count += 1

    result = CarApiSyncResult(
        success=error_count == 0,
        years_synced=years_synced,
        makes_synced=makes_synced,
        models_synced=models_synced,
        error_count=error_count,
    )
    LOGGER.info("CarAPI sync result: %s", result)
    return result
