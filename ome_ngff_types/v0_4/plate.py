from typing import Annotated, TypeVar

from pydantic import (
    AfterValidator,
    BaseModel,
    Field,
    model_validator,
)

from .base import ExtrasForbiddenModel, VersionedModel
from .types import AlphaNumeric, Expected, NonNegativeInt, PositiveInt
from .validators import check_unique

T = TypeVar("T")


class Acquisition(ExtrasForbiddenModel):
    id: NonNegativeInt
    name: Expected[str | None] = None
    maximum_field_count: Annotated[
        Expected[PositiveInt | None], Field(alias="maximumfieldcount")
    ] = None
    description: str | None = None
    start_time: Annotated[int | None, Field(alias="starttime")] = None
    end_time: Annotated[int | None, Field(alias="endtime")] = None

    @model_validator(mode="after")
    def check_times(self) -> "Acquisition":
        if self.start_time is None or self.end_time is None:
            return self
        if self.end_time <= self.start_time:
            raise ValueError("The end time is earlier than the start time.")
        return self


Acquisitions = Annotated[list[Acquisition], AfterValidator(check_unique("id"))]


class NamedModel(BaseModel):
    name: AlphaNumeric


Named = Annotated[T, AfterValidator(check_unique("name"))]


class Column(ExtrasForbiddenModel, NamedModel):
    ...


Columns = Named[list[Column]]


class Row(ExtrasForbiddenModel, NamedModel):
    ...


Rows = Named[list[Row]]


class Well(ExtrasForbiddenModel):
    path: str
    row_index: NonNegativeInt
    column_index: NonNegativeInt


Wells = list[Well]


class Plate(ExtrasForbiddenModel, VersionedModel):
    columns: Columns
    rows: Rows
    wells: Wells
    acquisitions: Acquisitions | None = None
    field_count: Expected[PositiveInt | None] = None
    name: Expected[str | None] = None

    @model_validator(mode="after")
    def check_wells(self) -> "Plate":
        for well in self.wells:
            try:
                column = self.columns[well.column_index]
                row = self.rows[well.row_index]
            except IndexError as err:
                raise ValueError("No matching column or row.") from err
            expected_path = f"{row.name}/{column.name}"
            if well.path != expected_path:
                raise ValueError("Invalid well path.")
        return self
