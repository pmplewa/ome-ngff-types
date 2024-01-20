from typing import Annotated

from pydantic import Field, model_validator

from .base import ExtrasIgnoredModel
from .image_label import ImageLabel
from .multiscales import Multiscales
from .omero import Omero
from .plate import Plate
from .well import Well


class Metadata(ExtrasIgnoredModel):
    multiscales: list[Multiscales] | None = None
    omero: Omero | None = None
    labels: list[str] | None = None
    image_label: Annotated[ImageLabel | None, Field(alias="image-label")] = None
    plate: Plate | None = None
    well: Well | None = None

    @model_validator(mode="after")
    def check_image_acquisitions_exist_in_plate(self) -> "Metadata":
        if self.well is None or self.plate is None or self.plate.acquisitions is None:
            return self
        acquisition_ids = [acquisition.id for acquisition in self.plate.acquisitions]
        for image in self.well.images:
            if image.acquisition is None:
                continue
            if image.acquisition not in acquisition_ids:
                raise ValueError("Acquisition missing from plate.")
        return self
