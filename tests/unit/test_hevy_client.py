"""Tests for HevyClient parsing with mocked transport."""

import httpx
import pytest

from hevy.models.workout import Workout
from hevy.services.hevy_client import HevyClient

from hevy.models.user_info import UserInfo


def _client(handler) -> HevyClient:
    transport = httpx.MockTransport(handler)
    return HevyClient(transport=transport, api_key="k", base_url="https://x")


def test_list_workouts_list_payload() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/workouts"
        assert request.headers.get("api-key") == "k"
        return httpx.Response(200, json=[{"id": 1, "title": "Chest", "sets": 3}])

    client = _client(handler)
    assert client.list_workouts() == [Workout(id="1", title="Chest", sets=3)]
    client.close()


def test_list_workouts_wrapped_payload() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"workouts": [{"id": 2, "title": "Back", "sets": None}]})

    client = _client(handler)
    try:
        # sets defaults to 0 when "sets" missing or None? spec says sets optional
        result = client.list_workouts()
    finally:
        client.close()
    assert result[0].id == "2"
    assert result[0].sets == 0


def test_http_error_propagates() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401)

    client = _client(handler)
    try:
        with pytest.raises(httpx.HTTPStatusError):
            client.list_workouts()
    finally:
        client.close()


def test_get_userinfo_success() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/user/info"
        return httpx.Response(
            200,
            json={
                "data": {
                    "id": "user_123",
                    "username": "testuser",
                    "name": "Test User",
                    "url": "https://hevyapp.me/user/testuser",
                    "weight_unit": "kg",
                    "distance_unit": "km",
                    "is_pro": True,
                },
            },
        )

    client = _client(handler)
    try:
        result = client.get_userinfo()
        assert result == UserInfo(
            id="user_123",
            username="testuser",
            name="Test User",
            url="https://hevyapp.me/user/testuser",
            weight_unit="kg",
            distance_unit="km",
            is_pro=True,
        )
    finally:
        client.close()


def test_get_userinfo_malformed_payload() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        # Missing 'data' key
        return httpx.Response(200, json={"error": "not found"})

    client = _client(handler)
    try:
        with pytest.raises(KeyError):
            client.get_userinfo()
    finally:
        client.close()