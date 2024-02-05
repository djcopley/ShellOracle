from __future__ import annotations

import os
import sys
from collections.abc import Mapping, Iterator
from pathlib import Path
from typing import Any

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

data_home = Path.home() / ".shelloracle"


class Configuration(Mapping):
    """ShellOracle application configuration

    The configuration is loaded at program startup, and persisted for the life of the application. Any changes made
    to the configuration while the application is running, will have no effect.
    """
    if env_path := os.environ.get("SHELLORACLE_CONFIG"):
        filepath = Path(env_path).absolute()
    else:
        filepath = data_home / "config.toml"

    def __init__(self) -> None:
        with self.filepath.open("rb") as config_file:
            self._config = tomllib.load(config_file)

    def __getitem__(self, __key) -> Any:
        return self._config[__key]

    def __len__(self) -> int:
        return len(self._config)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._config)

    @property
    def provider(self) -> str:
        return self["shelloracle"]["provider"]


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
