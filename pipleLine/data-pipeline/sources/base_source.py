"""
Purpose:
- Defines reusable source connector primitives for external automotive data providers.

Input:
- Endpoint path and request parameters.

Output:
- Raw JSON payload or bytes from provider APIs.

Responsibilities:
- Manage authenticated requests and timeout behavior.
- Provide consistent error handling for upstream failures.

TODO implementation notes:
- Add exponential backoff retry policy per source.
- Add response schema fingerprinting for change detection.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

import requests

LOGGER = logging.getLogger(__name__)


class SourceError(RuntimeError):
    pass


class BaseSource(ABC):
    def __init__(self, base_url: str, api_key: str = "", timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.api_key = api_key
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _request_json(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.base_url:
            raise SourceError("Base URL is empty for source connector")
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            response = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            LOGGER.exception("Source request failed: %s", url)
            raise SourceError(str(exc)) from exc

    @abstractmethod
    def fetch(self, **kwargs: Any) -> Any:
        raise NotImplementedError
