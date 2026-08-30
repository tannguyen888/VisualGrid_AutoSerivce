"""
Purpose:
- Call the Java (Spring Boot) backend's /api/ai/** endpoints to fetch vehicle/DTC
  context before diagnosis, and to persist AI-generated repair procedures back.

Input:
- OBD/DTC code plus optional make/model/trim/year for context lookups.
- Structured repair procedure payload (title, steps, parts, tools) to save.

Output:
- Parsed JSON dicts from the backend's ApiResponse envelope.

Dependencies:
- httpx
- os

Future implementation:
- Add retry/backoff and circuit breaking for backend outages.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8081")
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "")


class BackendClient:
    def __init__(self, base_url: str = BACKEND_BASE_URL, api_key: str = BACKEND_API_KEY) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> dict[str, str]:
        return {"X-Internal-Api-Key": self.api_key} if self.api_key else {}

    async def get_context(
        self,
        code: str,
        make: str = "",
        model: str = "",
        trim: str = "",
        year: int | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"code": code}
        if make:
            params["make"] = make
        if model:
            params["model"] = model
        if trim:
            params["trim"] = trim
        if year:
            params["year"] = year

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/api/ai/context", params=params, headers=self._headers()
            )
            response.raise_for_status()
            return response.json().get("data", {})

    async def save_repair_procedure(self, payload: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{self.base_url}/api/ai/repairs", json=payload, headers=self._headers()
            )
            response.raise_for_status()
            return response.json().get("data", {})
