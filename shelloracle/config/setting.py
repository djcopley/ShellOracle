from __future__ import annotations

from typing import TypeVar, Generic, TYPE_CHECKING

if TYPE_CHECKING:
    from ..provider import Provider

T = TypeVar("T")


class Setting(Generic[T]):
    def __init__(self, *, default: T | None = None):
        self.default = default

    def __set_name__(self, owner: Provider, name: str) -> None:
        self.name = name

    def __get__(self, instance: Provider, owner: type[Provider]) -> T:
        return self.default

    def __set__(self, instance: Provider, value: T) -> None:
        self.default = value
