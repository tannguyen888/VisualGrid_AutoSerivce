"""
Purpose:
- Real CarAPI (https://carapi.app) connector: logs in with api_token/api_secret,
  caches the JWT in-memory, and fetches years/makes/models.

Input:
- CarAPI base URL, api_token, api_secret (config.settings.carapi_*).

Output:
- Parsed lists of years (ints) / makes (dicts) / models (dicts).

Responsibilities:
- Handle the two-step CarAPI auth flow (POST /api/auth/login -> plain-text JWT).
- Retry once with a fresh token on 401.

TODO implementation notes:
- Persist the cached token to disk/redis if the pipeline runs as short-lived jobs.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import requests

LOGGER = logging.getLogger(__name__)

_TOKEN_TTL_SECONDS = 45 * 60


class CarApiError(RuntimeError):
    pass


class CarApiSource:
    def __init__(self, base_url: str, api_token: str, api_secret: str, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.api_secret = api_secret
        self.timeout = timeout
        self._token: str | None = None
        self._token_fetched_at: float = 0.0

    def _login(self) -> str:
        response = requests.post(
            f"{self.base_url}/api/auth/login",
            json={"api_token": self.api_token, "api_secret": self.api_secret},
            headers={"Content-Type": "application/json"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.text.strip()

    def _current_token(self) -> str:
        if self._token is None or (time.monotonic() - self._token_fetched_at) > _TOKEN_TTL_SECONDS:
            self._token = self._login()
            self._token_fetched_at = time.monotonic()
        return self._token

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        token = self._current_token()
        response = requests.get(
            f"{self.base_url}{path}",
            params={k: v for k, v in params.items() if v is not None},
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            timeout=self.timeout,
        )
        if response.status_code == 401:
            self._token = None
            token = self._current_token()
            response = requests.get(
                f"{self.base_url}{path}",
                params={k: v for k, v in params.items() if v is not None},
                headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
                timeout=self.timeout,
            )
        response.raise_for_status()
        return response.json()

    def fetch_years(self) -> list[int]:
        """/api/years/v2 returns a bare JSON array, not the {data, collection} envelope."""
        response = requests.get(
            f"{self.base_url}/api/years/v2",
            headers={"Authorization": f"Bearer {self._current_token()}", "Accept": "application/json"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def fetch_makes(self) -> list[dict[str, Any]]:
        return self._get("/api/makes/v2", {}).get("data", [])

    def fetch_models(self, year: int, make_id: int) -> list[dict[str, Any]]:
        return self._get("/api/models/v2", {"year": year, "make_id": make_id}).get("data", [])
