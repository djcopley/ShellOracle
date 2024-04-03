from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from unittest.mock import MagicMock, call

import pytest
from yaspin.spinners import Spinners

from shelloracle.shelloracle import get_query_from_pipe, spinner


@dataclass
class MockConfig:
    provider: str
    spinner_style: str | None


@pytest.fixture
def set_config(monkeypatch):
    def setter(config):
        return monkeypatch.setattr("shelloracle.config._config", config)
    return setter


def test_spinner(monkeypatch, set_config):
    yaspin_mock = MagicMock()
    monkeypatch.setattr("shelloracle.shelloracle.yaspin", yaspin_mock)

    set_config(MockConfig(provider="Ollama", spinner_style=None))
    spinner()
    assert yaspin_mock.call_args == call()

    set_config(MockConfig(provider="Ollama", spinner_style="earth"))
    spinner()
    assert yaspin_mock.call_args == call(Spinners.earth)

    set_config(MockConfig(provider="Ollama", spinner_style="not a real spinner"))
    with pytest.raises(AttributeError):
        spinner()


def test_get_query_from_pipe(monkeypatch):
    # Is a TTY
    monkeypatch.setattr(os, "isatty", lambda _: True)
    assert get_query_from_pipe() is None

    # Not a TTY and no lines in the pipe
    monkeypatch.setattr(os, "isatty", lambda _: False)
    monkeypatch.setattr(sys.stdin, "readlines", lambda: [])
    assert get_query_from_pipe() is None

    # Not TTY and one line in the pipe
    monkeypatch.setattr(sys.stdin, "readlines", lambda: ["what is up"])
    assert get_query_from_pipe() == "what is up"

    # Not a TTY and multiple lines in the pipe
    monkeypatch.setattr(sys.stdin, "readlines", lambda: ["what is up", "what is down"])
    with pytest.raises(ValueError):
        get_query_from_pipe()
