"""
Purpose:
- JSON extractor for API payloads and serialized source snapshots.

Input:
- Raw JSON payload as string or bytes.

Output:
- Parsed Python object.

Responsibilities:
- Decode payload safely.
- Raise meaningful parsing errors.

TODO implementation notes:
- Add schema fingerprinting for provider drift detection.
- Add line/column mapping for parser diagnostics.
"""

from __future__ import annotations

import json
from typing import Any


class JsonExtractor:
    def extract(self, raw_json: str | bytes | dict[str, Any] | list[Any]) -> dict[str, Any] | list[Any]:
        if isinstance(raw_json, (dict, list)):
            return raw_json
        if isinstance(raw_json, bytes):
            raw_json = raw_json.decode("utf-8", errors="replace")
        if not raw_json:
            return {}
        return json.loads(raw_json)
