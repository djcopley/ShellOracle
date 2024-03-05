import pytest
import tomlkit

from shelloracle.config import Configuration


@pytest.fixture(autouse=True)
def tmp_shelloracle_home(monkeypatch, tmp_path):
    monkeypatch.setattr("shelloracle.settings.Settings.shelloracle_home", tmp_path)
    return tmp_path


@pytest.fixture
def set_config(monkeypatch, tmp_shelloracle_home):
    config_path = tmp_shelloracle_home / "config.toml"

    def setter(config: dict) -> Configuration:
        with config_path.open("w") as f:
            tomlkit.dump(config, f)
        configuration = Configuration(config_path)
        monkeypatch.setattr("shelloracle.config._config", configuration)
        return configuration

    yield setter

    config_path.unlink()

