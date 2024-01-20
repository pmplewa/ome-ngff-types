from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from .types import Expected

_default_config = ConfigDict(
    alias_generator=to_camel,
    populate_by_name=True,
    str_min_length=1,
    str_strip_whitespace=True,
)


class ExtrasAllowedModel(BaseModel):
    model_config = ConfigDict(**_default_config, extra="allow")


class ExtrasForbiddenModel(BaseModel):
    model_config = ConfigDict(**_default_config, extra="forbid")


class ExtrasIgnoredModel(BaseModel):
    model_config = ConfigDict(**_default_config, extra="ignore")


class VersionedModel(BaseModel):
    version: Expected[Literal["0.4"] | None] = None
