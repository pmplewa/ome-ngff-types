from typing import Annotated

from pydantic import AfterValidator

from .base import ExtrasForbiddenModel, VersionedModel
from .types import AlphaNumeric
from .validators import check_unique


class Image(ExtrasForbiddenModel):
    path: AlphaNumeric
    acquisition: int | None = None


Images = Annotated[list[Image], AfterValidator(check_unique("path"))]


class Well(ExtrasForbiddenModel, VersionedModel):
    images: Images
