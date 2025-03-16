from __future__ import annotations

import pytest
import tomli_w

from shelloracle.config import Configuration


class TestConfiguration:
    @pytest.fixture
    def default_config(self):
        return Configuration(
            {
                "shelloracle": {"provider": "Ollama", "spinner_style": "earth"},
                "provider": {"Ollama": {"host": "localhost", "port": 11434, "model": "dolphin-mistral"}},
            }
        )

    def test_from_file(self, default_config, tmp_path):
        config_path = tmp_path / "config.toml"
        with config_path.open("wb") as f:
            tomli_w.dump(default_config.raw_config, f)
        assert Configuration.from_file(config_path) == default_config

    def test_getitem(self, default_config):
        for key in default_config:
            assert default_config[key] == default_config.raw_config[key]

    def test_len(self, default_config):
        assert len(default_config) == len(default_config.raw_config)

    def test_iter(self, default_config):
        assert list(iter(default_config)) == list(iter(default_config.raw_config))

    def test_provider(self, default_config):
        assert default_config.provider == "Ollama"

    def test_spinner_style(self, default_config):
        assert default_config.spinner_style == "earth"

    def test_no_spinner_style(self, caplog):
        config = Configuration(
            {
                "shelloracle": {"provider": "Ollama"},
                "provider": {"Ollama": {"host": "localhost", "port": 11434, "model": "dolphin-mistral"}},
            }
        )
        assert config.spinner_style is None
        assert "invalid spinner style" not in caplog.text

    def test_invalid_spinner_style(self, caplog):
        config = Configuration(
            {
                "shelloracle": {"provider": "Ollama", "spinner_style": "invalid"},
                "provider": {"Ollama": {"host": "localhost", "port": 11434, "model": "dolphin-mistral"}},
            }
        )
        assert config.spinner_style is None
        assert "invalid spinner style" in caplog.text
