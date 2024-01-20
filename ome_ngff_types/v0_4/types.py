import warnings
from typing import Annotated, TypeVar

from pydantic import AfterValidator, Field, ValidationInfo

from .warnings import ValidationWarning

T = TypeVar("T")


def _should_not_be_none(value: T, info: ValidationInfo) -> T:
    if value is None:
        title = info.config["title"].lower()
        name = info.field_name
        warnings.warn(f"Field {title}.{name} should have a value.", ValidationWarning)
    return value


Expected = Annotated[
    T, Field(validate_default=True), AfterValidator(_should_not_be_none)
]

AlphaNumeric = Annotated[str, Field(pattern=r"^[a-zA-Z0-9]*$")]

PositiveInt = Annotated[int, Field(gt=0)]
NonNegativeInt = Annotated[int, Field(ge=0)]
UInt8 = Annotated[int, Field(ge=0, le=255)]

RGBA = Annotated[list[UInt8], Field(min_length=4, max_length=4)]
