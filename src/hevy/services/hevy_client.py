"""Thin synchronous httpx client for the Hevy API."""

from __future__ import annotations

from typing import Any

import httpx

from hevy.config import settings
from hevy.models.workout import Workout


class HevyClient:
    def __init__(self, *, api_key: str | None = None, base_url: str | None = None,
                 timeout: float = 10.0, transport: httpx.MockTransport | None = None,
                 client: httpx.Client | None = None) -> None:
        self.api_key = api_key if api_key is not None else settings.api_key
        self.base_url = base_url or settings.base_url
        if client is not None:
            self._client = client
        else:
            self._client = httpx.Client(base_url=self.base_url, timeout=timeout,
                                        headers=self._headers(), transport=transport)

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Accept": "application/json"}
        if self.api_key:
            headers["api-key"] = self.api_key
        return headers

    def list_workouts(self) -> list[Workout]:
        response = self._client.get("/v1/workouts")
        response.raise_for_status()
        payload: Any = response.json()
        items = payload if isinstance(payload, list) else payload.get("workouts", [])
        result: list[Workout] = []
        for item in items:
            result.append(
                Workout(
                    id=str(item["id"]),
                    title=str(item["title"]),
                   sets=int(item.get("sets") or 0),
                )
            )
        return result

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> HevyClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()