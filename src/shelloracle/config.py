from __future__ import annotations

import logging
import sys
from collections.abc import Iterator, Mapping
from typing import TYPE_CHECKING, Any

from yaspin.spinners import SPINNERS_DATA

from shelloracle.settings import Settings

if TYPE_CHECKING:
    from pathlib import Path

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

logger = logging.getLogger(__name__)


class Configuration(Mapping):
    def __init__(self, filepath: Path) -> None:
        """ShellOracle application configuration

        :param filepath: Path to the configuration file
        :raises FileNotFoundError: if the configuration file does not exist
        """
        self.filepath = filepath
        with filepath.open("rb") as config_file:
            self._config = tomllib.load(config_file)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def __len__(self) -> int:
        return len(self._config)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._config)

    def __str__(self):
        return f"Configuration({self._config})"

    def __repr__(self) -> str:
        return str(self)

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


def initialize_config() -> None:
    """Initialize the configuration file

    :raises RuntimeError: if the config is already initialized
    :raises FileNotFoundError: if the config file is not found
    """
    global _config  # noqa: PLW0603
    if _config:
        msg = "Configuration already initialized"
        raise RuntimeError(msg)
    filepath = Settings.shelloracle_home / "config.toml"
    _config = Configuration(filepath)


def get_config() -> Configuration:
    """Returns the global configuration object.

    :return: the global configuration
    :raises RuntimeError: if the configuration is not initialized
    """
    if _config is None:
        msg = "Configuration not initialized"
        raise RuntimeError(msg)
    return _config
