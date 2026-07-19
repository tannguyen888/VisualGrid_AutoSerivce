"""Loader package."""

from loader.mongo_loader import MongoLoader
from loader.postgres_loader import PostgresLoader
from loader.storage_loader import StorageLoader

__all__ = ["PostgresLoader", "MongoLoader", "StorageLoader"]
