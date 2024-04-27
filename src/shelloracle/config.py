from __future__ import annotations

import logging
import os
import sys
from collections.abc import Mapping, Iterator
from pathlib import Path
from typing import Any
from yaspin.spinners import SPINNERS_DATA

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

logger = logging.getLogger(__name__)
shelloracle_home = Path.home() / ".shelloracle"
shelloracle_home.mkdir(exist_ok=True)


class Configuration(Mapping):
    """ShellOracle application configuration

    The configuration is loaded at program startup, and persisted for the life of the application. Any changes made
    to the configuration while the application is running, will have no effect.
    """
    if "SHELLORACLE_CONFIG" in os.environ:
        filepath = Path(os.environ["SHELLORACLE_CONFIG"]).absolute()
    else:
        filepath = shelloracle_home / "config.toml"

    def __init__(self) -> None:
        with self.filepath.open("rb") as config_file:
            self._config = tomllib.load(config_file)

    def __getitem__(self, key) -> Any:
        return self._config[key]

    def __len__(self) -> int:
        return len(self._config)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._config)

    @property
    def provider(self) -> str:
        return self["shelloracle"]["provider"]

    @property
    def spinner_style(self) -> str | None:
        style = self["shelloracle"].get("spinner_style", None)
        if not style:
            return None
        if style not in SPINNERS_DATA:
            logger.warning("invalid spinner style: %s", style)
            return None
        return style


_config: Configuration | None = None


def get_config() -> Configuration:
    """Returns the global configuration object.

    Creates global configuration from the configuration toml the first time the function is called.

    :return: the global configuration
    """
    global _config
    if _config is None:
        _config = Configuration()
    return _config
