from collections import Counter
from enum import Enum
from typing import Annotated

from pydantic import AfterValidator, Field, model_validator

from .base import ExtrasForbiddenModel
from .types import Expected
from .units import SpaceUnit, TimeUnit
from .validators import check_unique


class AxisType(str, Enum):
    space = "space"
    time = "time"
    channel = "channel"


class Axis(ExtrasForbiddenModel):
    name: str
    type: Expected[AxisType | None] = None
    unit: Annotated[
        Expected[SpaceUnit | TimeUnit | None], Field(validation_alias="units")
    ] = None

    @model_validator(mode="after")
    def check_unit_matches_type(self) -> "Axis":
        if self.unit is None or self.type is None:
            return self
        if isinstance(self.unit, SpaceUnit) and self.type != AxisType.space:
            raise ValueError("An axis with a space unit must be of type 'space'.")
        if isinstance(self.unit, TimeUnit) and self.type != AxisType.time:
            raise ValueError("An axis with a time unit must be of type 'time'.")
        return self


def _check_axis_tally(axes: list[Axis]) -> list[Axis]:
    type_counts = Counter([axis.type for axis in axes])
    type_list = list(type_counts)
    if type_counts[AxisType.space] not in (2, 3):
        raise ValueError("There must be two or three axes of type 'space'.")
    if type_list.index(AxisType.space) != len(type_list) - 1:
        raise ValueError("The axes of type 'space' must come last.")
    if type_counts[AxisType.time] > 0:
        if type_counts[AxisType.time] > 1:
            raise ValueError("There may only be one axis of type 'time'.")
        if type_list.index(AxisType.time) != 0:
            raise ValueError("The axis of type 'time' must come first.")
    if type_counts[AxisType.channel] > 1:
        raise ValueError("There may only be one axis of type 'channel'.")
    return axes


Axes = Annotated[
    list[Axis],
    Field(min_length=2, max_length=5),
    AfterValidator(check_unique("name")),
    AfterValidator(_check_axis_tally),
]
