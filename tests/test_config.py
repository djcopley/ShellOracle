from __future__ import annotations

import pytest

from shelloracle.config import get_config, initialize_config


class TestConfiguration:
    @pytest.fixture
    def default_config(self, set_config):
        config = {
            "shelloracle": {"provider": "Ollama", "spinner_style": "earth"},
            "provider": {"Ollama": {"host": "localhost", "port": 11434, "model": "dolphin-mistral"}},
        }
        set_config(config)
        return config

    def test_initialize_config(self, default_config):
        with pytest.raises(RuntimeError):
            initialize_config()

    def test_from_file(self, default_config):
        assert get_config() == default_config

    def test_getitem(self, default_config):
        for key in default_config:
            assert default_config[key] == get_config()[key]

    def test_len(self, default_config):
        assert len(default_config) == len(get_config())

    def test_iter(self, default_config):
        assert list(iter(default_config)) == list(iter(get_config()))

    def test_str(self, default_config):
        assert str(get_config()) == f"Configuration({default_config})"

    def test_repr(self, default_config):
        assert repr(default_config) == str(default_config)

    def test_provider(self, default_config):
        assert get_config().provider == "Ollama"

    def test_spinner_style(self, default_config):
        assert get_config().spinner_style == "earth"

    def test_no_spinner_style(self, caplog, set_config):
        config_dict = {
            "shelloracle": {"provider": "Ollama"},
            "provider": {"Ollama": {"host": "localhost", "port": 11434, "model": "dolphin-mistral"}},
        }
        set_config(config_dict)
        assert get_config().spinner_style is None
        assert "invalid spinner style" not in caplog.text

    def test_invalid_spinner_style(self, caplog, set_config):
        config_dict = {
            "shelloracle": {"provider": "Ollama", "spinner_style": "invalid"},
            "provider": {"Ollama": {"host": "localhost", "port": 11434, "model": "dolphin-mistral"}},
        }
        set_config(config_dict)
        assert get_config().spinner_style is None
        assert "invalid spinner style" in caplog.text
