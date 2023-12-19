from pathlib import Path
from typing import TextIO

from tomlkit import document, table, load

data_home = Path.home() / "Library/Application Support" / "shelloracle"


def _default_config():
    doc = document()
    shelloracle = table()
    shelloracle.add("provider", "ollama")
    doc.add("shelloracle", shelloracle)
    return doc


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Configuration(metaclass=SingletonMeta):
    filepath = data_home / "config.toml"

    def __init__(self):
        self.file: TextIO | None = None
        self._ensure_config_exists()

    def _ensure_config_exists(self):
        if not self.filepath.exists():
            data_home.mkdir(exist_ok=True)
            self.filepath.write_text(_default_config())

    @property
    def provider(self) -> str | None:
        with self.filepath.open("r") as config_file:
            file = load(config_file)
        return file.get("shelloracle", {}).get("provider", None)

