from __future__ import annotations

import typing
from pathlib import Path

if typing.TYPE_CHECKING:
    from shelloracle.config import Configuration

shelloracle_home = Path.home() / ".shelloracle"
shelloracle_home.mkdir(exist_ok=True)


class Application:
    configuration: Configuration

    def __init__(self):
        self.config_path = shelloracle_home / "config.toml"
        self.log_path = shelloracle_home / "shelloracle.log"
