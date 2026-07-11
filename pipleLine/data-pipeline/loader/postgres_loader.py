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
        # TODO: persist the payload into PostgreSQL.
        pass
