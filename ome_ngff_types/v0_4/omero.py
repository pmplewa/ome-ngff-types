from typing import Annotated

from pydantic import Field, model_validator

from .base import ExtrasAllowedModel, ExtrasForbiddenModel


class Window(ExtrasForbiddenModel):
    min: int | float
    max: int | float
    start: int | float
    end: int | float

    @model_validator(mode="after")
    def check_window(self) -> "Window":
        if not self.min <= self.start <= self.end <= self.max:
            raise ValueError("The window limits are invalid.")
        return self


Color = Annotated[str, Field(pattern=r"^(?:[0-9a-fA-F]{3}){1,2}$")]


class Channel(ExtrasAllowedModel):
    color: Color
    window: Window


Channels = list[Channel]


class Omero(ExtrasAllowedModel):
    channels: Channels
