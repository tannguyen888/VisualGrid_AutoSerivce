"""
Purpose:
- MongoDB loader for document-oriented repair/manual records.

Input:
- Collection name and canonical payload.

Output:
- Load status dictionary with inserted id when available.

Responsibilities:
- Insert documents into MongoDB collections.
- Support dry-run mode during local development.

TODO implementation notes:
- Add upsert by external source id.
- Add version history collection strategy.
"""

from __future__ import annotations

from typing import Any

from config import settings


class MongoLoader:
    def __init__(self, mongodb_url: str | None = None, database_name: str = "autocare", dry_run: bool | None = None) -> None:
        self.mongodb_url = mongodb_url or settings.mongodb_url
        self.database_name = database_name
        self.dry_run = settings.dry_run if dry_run is None else dry_run

    def save(self, collection_name: str, payload: dict[str, Any]) -> dict[str, Any]:
        if self.dry_run:
            return {
                "status": "dry-run",
                "target": "mongodb",
                "collection": collection_name,
                "payload": payload,
            }

        if not self.mongodb_url:
            raise ValueError("MONGODB_URL is required when dry_run=False")

        from pymongo import MongoClient

        client = MongoClient(self.mongodb_url)
        result = client[self.database_name][collection_name].insert_one(payload)
        return {
            "status": "inserted",
            "target": "mongodb",
            "collection": collection_name,
            "inserted_id": str(result.inserted_id),
        }
