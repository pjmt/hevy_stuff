"""Tests for hevy config."""

import pytest

from hevy.config import Settings


def test_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HEVY_API_KEY", raising=False)
    monkeypatch.delenv("HEVY_BASE_URL", raising=False)
    s = Settings(_env_file=None)
    assert s.base_url == "https://api.hevyapp.com"
    assert s.api_key is None


def test_api_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HEVY_API_KEY", "secret")
    s = Settings(_env_file=None)
    assert s.api_key == "secret"


def test_base_url_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HEVY_BASE_URL", "http://example.test")
    s = Settings(_env_file=None)
    assert s.base_url == "http://example.test"


def test_extra_ignored() -> None:
    s = Settings(_env_file=None)
    assert s.base_url == "https://api.hevyapp.com"
