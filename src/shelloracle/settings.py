from pathlib import Path


class Settings:
    shelloracle_home = Path.home() / ".shelloracle"
    shelloracle_home.mkdir(exist_ok=True)
