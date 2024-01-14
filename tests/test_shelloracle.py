import os
import sys

import pytest

from shelloracle.shelloracle import get_query_from_pipe


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
