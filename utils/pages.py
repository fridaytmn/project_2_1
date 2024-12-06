from __future__ import annotations
from pathlib import Path
from typing import (
    List,
    Callable,
    Any,
    TypeVar,
    Set,
)
from natsort import humansorted

T = TypeVar("T")


class BaseProvider(Set[T]):
    def filter(self, func: Callable[[T], bool]) -> BaseProvider[Set[T]]:
        return BaseProvider(filter(func, self))

    def sort_natural(self, key_func: Callable[[T], Any], reverse: bool = False) -> List[T]:
        return humansorted(self, key=key_func, reverse=reverse)

    def one(self) -> T:
        if len(self) > 0:
            return self.pop()

        return None


def get_module_name(path: Path) -> str:
    return ".".join(
        [
            *filter(lambda x: x not in [".", ".."], path.parts[:-1]),
            *[path.name[: -len(".py")]],
        ]
    )


def get_short_url(path: Path) -> str:
    return "/".join(
        [
            *path.parts[1:-1],
            *[path.name[: -len(".py")]],
        ]
    )
