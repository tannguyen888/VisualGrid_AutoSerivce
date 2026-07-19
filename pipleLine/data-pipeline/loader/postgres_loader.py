"""
Purpose:
- PostgreSQL loader for relational automotive entities.

Input:
- Table name and canonical payload.

Output:
- Load status dictionary.

Responsibilities:
- Persist records using SQLAlchemy text query execution.
- Provide dry-run mode for non-destructive testing.

TODO implementation notes:
- Add efficient bulk upsert strategy.
- Add table metadata-driven insert validation.
"""

from __future__ import annotations

from typing import Any

from config import settings


class PostgresLoader:
    def __init__(self, database_url: str | None = None, dry_run: bool | None = None) -> None:
        self.database_url = database_url or settings.postgres_url
        self.dry_run = settings.dry_run if dry_run is None else dry_run

    def save(self, table_name: str, payload: dict[str, Any]) -> dict[str, Any]:
        if self.dry_run:
            return {"status": "dry-run", "target": "postgres", "table": table_name, "payload": payload}

        if not self.database_url:
            raise ValueError("POSTGRES_URL is required when dry_run=False")

        from sqlalchemy import create_engine, text

        columns = list(payload.keys())
        values = {key: payload[key] for key in columns}
        placeholders = ", ".join([f":{column}" for column in columns])
        quoted_columns = ", ".join(columns)
        query = text(f"INSERT INTO {table_name} ({quoted_columns}) VALUES ({placeholders})")

        engine = create_engine(self.database_url)
        with engine.begin() as connection:
            connection.execute(query, values)
        return {"status": "inserted", "target": "postgres", "table": table_name}
