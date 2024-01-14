from __future__ import annotations

from typing import TypeVar, Generic, TYPE_CHECKING

from . import config

if TYPE_CHECKING:
    from ..provider import Provider

T = TypeVar("T")


class Setting(Generic[T]):
    def __init__(self, *, name: str | None = None, default: T | None = None) -> None:
        self.name = name
        self.default = default

    def __set_name__(self, owner: type[Provider], name: str) -> None:
        if not self.name:
            self.name = name
        # Set the default value in the config dictionary if it doesn't exist
        provider_table = config.global_config.get("provider", {})
        provider_table.setdefault(owner.name, {}).setdefault(name, self.default)
        config.global_config["provider"] = provider_table

    def __get__(self, instance: Provider, owner: type[Provider]) -> T:
        return config.global_config.get("provider", {}).get(instance.name, {})[self.name]

    def __set__(self, instance: Provider, value: T) -> None:
        config.global_config.setdefault("provider", {}).setdefault(instance.name, {})[self.name] = value
