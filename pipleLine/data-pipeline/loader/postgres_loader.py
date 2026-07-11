"""
TODO:
PostgreSQL loader.

What this file does:
- Inserts or updates normalized records in PostgreSQL.

Input:
- Validated record payload.

Output:
- Persisted rows.

Dependencies:
- sqlalchemy
- psycopg

Future implementation steps:
- Add UPSERT support
- Add duplicate detection
- Add transaction handling
"""


class PostgresLoader:
    def save(self, payload: dict) -> None:
        # Bước 1: tạo biến connection/session.
        # session = None
        # record = payload
        # Bước 2: insert/update/upsert record.
        # Bước 3: commit hoặc rollback.
        pass
