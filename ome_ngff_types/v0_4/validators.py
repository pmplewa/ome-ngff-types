from collections.abc import Callable
from typing import TypeVar

from pydantic import ValidationInfo
from pydantic_core import PydanticCustomError

T = TypeVar("T")


def check_unique(attr: str | None = None) -> Callable:
    def _check(values: list[T], info: ValidationInfo) -> list[T]:
        _values = (
            [getattr(value, attr) for value in values] if attr is not None else values
        )
        if len(set(_values)) != len(_values):
            field_name = attr if attr is not None else info.field_name
            raise PydanticCustomError(
                "unique_list", f"The field '{field_name}' must be unique."
            )
        return values

    return _check
