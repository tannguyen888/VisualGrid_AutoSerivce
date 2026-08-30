"""
Purpose:
- Upsert CarAPI reference data (years/makes/models) into the same Postgres
  tables the Java backend owns (car_year, car_make, car_model), so both
  services share one source of truth.

Input:
- Parsed year/make/model records from CarApiSource.

Output:
- Count of rows affected, respecting dry-run mode.

Dependencies:
- psycopg
- config.settings

Future implementation:
- Batch inserts with executemany once volumes grow beyond a few hundred rows.
"""

from __future__ import annotations

import logging
from typing import Any

from config import settings

LOGGER = logging.getLogger(__name__)


class CarApiLoader:
    def __init__(self, database_url: str | None = None, dry_run: bool | None = None) -> None:
        self.database_url = database_url or settings.postgres_url
        self.dry_run = settings.dry_run if dry_run is None else dry_run

    def _connect(self):
        import psycopg

        if not self.database_url:
            raise ValueError("POSTGRES_URL (or POSTGRES_HOST/DB/USER/PASSWORD) is required when dry_run=False")
        return psycopg.connect(self.database_url.replace("postgresql+psycopg://", "postgresql://"))

    def upsert_years(self, years: list[int]) -> int:
        if self.dry_run:
            LOGGER.info("[dry-run] would upsert %s years", len(years))
            return len(years)
        with self._connect() as conn, conn.cursor() as cur:
            for year in years:
                cur.execute("INSERT INTO car_year (year) VALUES (%s) ON CONFLICT (year) DO NOTHING", (year,))
            conn.commit()
        return len(years)

    def upsert_makes(self, makes: list[dict[str, Any]]) -> int:
        if self.dry_run:
            LOGGER.info("[dry-run] would upsert %s makes", len(makes))
            return len(makes)
        with self._connect() as conn, conn.cursor() as cur:
            for make in makes:
                cur.execute(
                    "INSERT INTO car_make (id, name) VALUES (%s, %s) "
                    "ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name",
                    (make["id"], make["name"]),
                )
            conn.commit()
        return len(makes)

    def upsert_models(self, models: list[dict[str, Any]], year: int) -> int:
        if self.dry_run:
            LOGGER.info("[dry-run] would upsert %s models for year=%s", len(models), year)
            return len(models)
        with self._connect() as conn, conn.cursor() as cur:
            for model in models:
                cur.execute(
                    "INSERT INTO car_model (id, name, make_id, make_name, year) VALUES (%s, %s, %s, %s, %s) "
                    "ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, make_id = EXCLUDED.make_id, "
                    "make_name = EXCLUDED.make_name, year = EXCLUDED.year",
                    (model["id"], model["name"], model.get("make_id"), model.get("make"), year),
                )
            conn.commit()
        return len(models)
