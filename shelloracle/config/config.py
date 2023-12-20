from collections.abc import MutableMapping
from pathlib import Path

import tomlkit

data_home = Path.home() / "Library/Application Support" / "shelloracle"


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

    def __getitem__(self, item):
        with self.filepath.open("r") as file:
            config = tomlkit.load(file)
        return config[item]

    def __setitem__(self, key, value):
        with self.filepath.open("r") as file:
            config = tomlkit.load(file)
        config[key] = value
        config.multiline = True
        with self.filepath.open("w") as file:
            tomlkit.dump(config, file)

    def __delitem__(self, key):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def __len__(self) -> int:
        raise NotImplementedError()

    def _ensure_config_exists(self) -> None:
        if self.filepath.exists():
            return
        data_home.mkdir(exist_ok=True)
        config = _default_config()
        with self.filepath.open("w") as file:
            tomlkit.dump(config, file)

    @property
    def provider(self) -> str | None:
        return self["shelloracle"]["provider"]


global_config = Configuration()
