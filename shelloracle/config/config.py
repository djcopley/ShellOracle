from __future__ import annotations

from collections.abc import MutableMapping, Iterator
from pathlib import Path
from typing import Any

import tomlkit

data_home = Path.home() / ".shelloracle"


def _default_config() -> tomlkit.TOMLDocument:
    config = tomlkit.document()
    shor_table = tomlkit.table()
    shor_table.add("provider", "Ollama")
    config.add("shelloracle", shor_table)
    return config


class Configuration(MutableMapping):
    filepath = data_home / "config.toml"

    def __init__(self) -> None:
        self._ensure_config_exists()

    def __getitem__(self, item: str) -> dict:
        with self.filepath.open("r") as file:
            config = tomlkit.load(file)
        return config[item]

    def __setitem__(self, key: str, value: Any) -> None:
        with self.filepath.open("r") as file:
            config = tomlkit.load(file)
        config[key] = value
        config.multiline = True
        with self.filepath.open("w") as file:
            tomlkit.dump(config, file)

    def __delitem__(self, key: str) -> None:
        with self.filepath.open("r") as file:
            config = tomlkit.load(file)
        del config[key]
        with self.filepath.open("w") as file:
            tomlkit.dump(config, file)

    def __iter__(self) -> Iterator[str]:
        with self.filepath.open("r") as file:
            config = tomlkit.load(file)
        return iter(config)

    def __len__(self) -> int:
        with self.filepath.open("r") as file:
            config = tomlkit.load(file)
        return len(config)

    def _ensure_config_exists(self) -> None:
        if self.filepath.exists():
            return
        data_home.mkdir(exist_ok=True)
        config = _default_config()
        with self.filepath.open("w") as file:
            tomlkit.dump(config, file)

    @property
    def provider(self) -> str:
        return self["shelloracle"]["provider"]


global_config = Configuration()
