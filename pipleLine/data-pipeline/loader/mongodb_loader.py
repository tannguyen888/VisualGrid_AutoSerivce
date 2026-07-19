"""
Purpose:
- Compatibility module using MongoLoader with mongodb_loader naming.

Input:
- Collection name and payload.

Output:
- Mongo load status dictionary.

Responsibilities:
- Expose expected class name/module path for callers.

TODO implementation notes:
- Consolidate to one module path once imports are migrated.
"""

from loader.mongo_loader import MongoLoader

__all__ = ["MongoLoader"]
