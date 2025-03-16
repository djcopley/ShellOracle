from __future__ import annotations

import logging
import sys
from collections.abc import Iterator, Mapping
from typing import TYPE_CHECKING, Any

from yaspin.spinners import SPINNERS_DATA

if TYPE_CHECKING:
    from pathlib import Path


if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

logger = logging.getLogger(__name__)


class Configuration(Mapping):
    def __init__(self, config: dict[str, Any]) -> None:
        """ShellOracle application configuration

        :param config: configuration dict
        :raises FileNotFoundError: if the configuration file does not exist
        """
        self._config = config

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
    def raw_config(self) -> dict[str, Any]:
        return self._config

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

    @classmethod
    def from_file(cls, filepath: Path):
        with filepath.open("rb") as config_file:
            config = tomllib.load(config_file)
        return cls(config)
