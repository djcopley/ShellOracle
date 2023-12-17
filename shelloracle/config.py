import tomllib
from pathlib import Path

data_home = Path.home() / "Library/Application Support" / "shelloracle"

_default_configuration = """\
[shelloracle]
provider = "ollama"
"""


class Configuration:
    _config_filepath = data_home / "config.toml"

    def __init__(self):
        data_home.mkdir(exist_ok=True)
        if not self._config_filepath.exists():
            self._config_filepath.write_text(_default_configuration)

    @property
    def provider(self) -> str | None:
        with self._config_filepath.open("rb") as config_file:
            file = tomllib.load(config_file)
        return file["shelloracle"]["provider"]
