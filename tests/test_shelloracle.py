from __future__ import annotations

import os
import sys
from unittest.mock import MagicMock, call

import pytest
from yaspin.spinners import Spinners

from shelloracle.shelloracle import get_query_from_pipe, spinner


@pytest.fixture
def mock_yaspin(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("shelloracle.shelloracle.yaspin", mock)
    return mock


@pytest.mark.parametrize(("spinner_style", "expected"), [(None, call()), ("earth", call(Spinners.earth))])
def test_spinner(spinner_style, expected, mock_yaspin):
    spinner(spinner_style)
    assert mock_yaspin.call_args == expected


def test_spinner_fail(mock_yaspin):
    with pytest.raises(AttributeError):
        spinner("not a spinner style")


@pytest.mark.parametrize(
    ("isatty", "readlines", "expected"), [(True, None, None), (False, [], None), (False, ["what is up"], "what is up")]
)
def test_get_query_from_pipe(isatty, readlines, expected, monkeypatch):
    monkeypatch.setattr(os, "isatty", lambda _: isatty)
    monkeypatch.setattr(sys.stdin, "readlines", lambda: readlines)
    assert get_query_from_pipe() == expected


def test_get_query_from_pipe_fail(monkeypatch):
    monkeypatch.setattr(os, "isatty", lambda _: False)
    monkeypatch.setattr(sys.stdin, "readlines", lambda: ["what is up", "what is down"])
    with pytest.raises(ValueError, match="Multi-line input is not supported"):
        get_query_from_pipe()
