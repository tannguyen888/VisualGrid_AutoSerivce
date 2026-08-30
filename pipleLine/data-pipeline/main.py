"""
Purpose:
- Main ETL execution orchestration for automotive data synchronization.

Input:
- Runtime trigger and optional source lookup context.

Output:
- ETL run summary with extracted/loaded/error counts.

Responsibilities:
- Coordinate Extract -> Transform -> Validate -> Load flow.
- Apply logging and entity-level error handling.

TODO implementation notes:
- Add parallel source processing by entity type.
- Add robust state checkpointing for incremental runs.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from config import settings
from extractor.json_extractor import JsonExtractor
from loader.mongo_loader import MongoLoader
from loader.postgres_loader import PostgresLoader
from parser.part_parser import PartParser
from parser.repair_parser import RepairParser
from parser.vehicle_parser import VehicleParser
from sources.parts_source import PartsSource
from sources.repair_source import RepairSource
from sources.vin_source import VinSource
from transformer.part_mapper import PartMapper
from transformer.repair_mapper import RepairMapper
from transformer.vehicle_mapper import VehicleMapper
from validator.data_quality import DataQualityValidator
from validator.schema_validator import SchemaValidator

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class PipelineRunResult:
    success: bool
    extracted_count: int
    loaded_count: int
    error_count: int


def _build_sources() -> dict[str, Any]:
    return {
        "vin": VinSource(base_url=settings.vin_base_url, api_key=settings.vin_api_key),
        "parts": PartsSource(base_url=settings.parts_base_url, api_key=settings.parts_api_key),
        "repair": RepairSource(base_url=settings.repair_base_url, api_key=settings.repair_api_key),
    }


def run_pipeline(vin: str = "1HGCM82633A123456") -> PipelineRunResult:
    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))

    extractor = JsonExtractor()
    vehicle_parser = VehicleParser()
    part_parser = PartParser()
    repair_parser = RepairParser()

    vehicle_mapper = VehicleMapper()
    part_mapper = PartMapper()
    repair_mapper = RepairMapper()

    schema_validator = SchemaValidator()
    quality_validator = DataQualityValidator()

    postgres_loader = PostgresLoader()
    mongo_loader = MongoLoader()

    sources = _build_sources()

    extracted_count = 0
    loaded_count = 0
    error_count = 0
    seen_vehicle_keys: set[str] = set()
    seen_part_keys: set[str] = set()

    def _safe_fetch(source_name: str, **kwargs: Any) -> dict[str, Any]:
        nonlocal extracted_count, error_count
        try:
            payload = sources[source_name].fetch(**kwargs)
            extracted_count += 1
            return payload if isinstance(payload, dict) else {"raw": payload}
        except Exception:
            LOGGER.exception("Source fetch failed: %s", source_name)
            error_count += 1
            return {}

    vin_raw = _safe_fetch("vin", vin=vin)
    parts_raw = _safe_fetch("parts", query=vin)
    repair_raw = _safe_fetch("repair", vehicle_id=vin)

    vehicle_payload = vehicle_mapper.map(vehicle_parser.parse(extractor.extract(vin_raw)))
    part_payload = part_mapper.map(part_parser.parse(extractor.extract(parts_raw)))
    repair_payload = repair_mapper.map(repair_parser.parse(extractor.extract(repair_raw)))

    try:
        vehicle_valid = schema_validator.validate("vehicle", vehicle_payload)
        vehicle_quality = quality_validator.check(vehicle_valid, ["make", "model", "year"], unique_key="vin", seen_keys=seen_vehicle_keys)
        if vehicle_quality.passed:
            postgres_loader.save("vehicles", vehicle_valid)
            loaded_count += 1
        else:
            error_count += 1
            LOGGER.warning("Vehicle quality issues: %s", vehicle_quality.issues)
    except Exception:
        LOGGER.exception("Vehicle processing failed")
        error_count += 1

    try:
        part_valid = schema_validator.validate("part", part_payload)
        part_quality = quality_validator.check(part_valid, ["oem_number", "name"], unique_key="oem_number", seen_keys=seen_part_keys)
        if part_quality.passed:
            postgres_loader.save("parts", part_valid)
            loaded_count += 1
        else:
            error_count += 1
            LOGGER.warning("Part quality issues: %s", part_quality.issues)
    except Exception:
        LOGGER.exception("Part processing failed")
        error_count += 1

    try:
        repair_valid = schema_validator.validate("repair", repair_payload)
        repair_quality = quality_validator.check(repair_valid, ["title"])
        if repair_quality.passed:
            mongo_loader.save("repair_documents", repair_valid)
            loaded_count += 1
        else:
            error_count += 1
            LOGGER.warning("Repair quality issues: %s", repair_quality.issues)
    except Exception:
        LOGGER.exception("Repair processing failed")
        error_count += 1

    success = error_count == 0
    return PipelineRunResult(
        success=success,
        extracted_count=extracted_count,
        loaded_count=loaded_count,
        error_count=error_count,
    )


def main() -> None:
    """One-off run of the real CarAPI sync (years/makes/models)."""
    from carapi_pipeline import run_carapi_sync

    result = run_carapi_sync()
    LOGGER.info("CarAPI sync result: %s", result)


def run_legacy_mock_pipeline() -> None:
    """Legacy scaffold pipeline (VIN/parts/repair via mock/unconfigured sources), kept for reference."""
    result = run_pipeline()
    LOGGER.info("Legacy mock pipeline result: %s", result)


def serve() -> None:
    """Run the real CarAPI sync on a fixed daily schedule (settings.sync_cron_hour/minute)."""
    import time

    from carapi_pipeline import run_carapi_sync
    from scheduler.sync_scheduler import SyncScheduler

    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))

    sync_scheduler = SyncScheduler(
        cron_hour=settings.sync_cron_hour,
        cron_minute=settings.sync_cron_minute,
        max_retries=settings.max_retries,
        retry_backoff_seconds=settings.retry_backoff_seconds,
    )
    sync_scheduler.start(job_callable=lambda: run_carapi_sync())
    LOGGER.info(
        "Pipeline scheduler running, CarAPI sync fires daily at %02d:%02d. Ctrl+C to stop.",
        settings.sync_cron_hour,
        settings.sync_cron_minute,
    )
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        sync_scheduler.stop()


if __name__ == "__main__":
    import sys

    if "--serve" in sys.argv:
        serve()
    else:
        main()

