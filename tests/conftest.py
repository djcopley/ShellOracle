import pytest

from shelloracle.cli import Application


@pytest.fixture
def global_app():
    return Application()
