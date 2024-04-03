import os
import sys
from unittest.mock import MagicMock, call

import pytest
from yaspin.spinners import Spinners

from shelloracle.config import Configuration
from shelloracle.shelloracle import get_query_from_pipe, spinner


def test_spinner(monkeypatch):
    yaspin_mock = MagicMock()
    monkeypatch.setattr("shelloracle.shelloracle.yaspin", yaspin_mock)

    monkeypatch.setattr(Configuration, "spinner_style", None)
    spinner()
    assert yaspin_mock.call_args == call()

    monkeypatch.setattr(Configuration, "spinner_style", "earth")
    spinner()
    assert yaspin_mock.call_args == call(Spinners.earth)

    monkeypatch.setattr(Configuration, "spinner_style", "not a real spinner")
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
