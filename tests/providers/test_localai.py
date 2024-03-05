import pytest


class TestLocalAI:
    @pytest.fixture
    def localai_config(self, set_config):
        config = {'shelloracle': {'provider': 'LocalAI'},
                  'provider': {'LocalAI': {'host': 'localhost', 'port': 8080, 'model': 'gpt-3.5-turbo'}}}

        return set_config(config)
