from typing import Annotated, TypeVar

from pydantic import AfterValidator, BaseModel, Field

from .base import ExtrasAllowedModel, ExtrasForbiddenModel, VersionedModel
from .types import RGBA, Expected
from .validators import check_unique

T = TypeVar("T")


class LabeledModel(BaseModel):
    label_value: Annotated[int, Field(alias="label-value")]


Labeled = Annotated[T, AfterValidator(check_unique("label_value"))]


class Color(ExtrasForbiddenModel, LabeledModel):
    rgba: RGBA | None = None


Colors = Labeled[list[Color]]


class Property(ExtrasAllowedModel, LabeledModel):
    ...


Properties = Labeled[list[Property]]


class Source(ExtrasAllowedModel):
    image: str = "../../"


class ImageLabel(ExtrasForbiddenModel, VersionedModel):
    colors: Expected[Colors | None] = None
    properties: Properties | None = None
    source: Source | None = None
