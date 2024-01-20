from pydantic import model_validator

from .axes import Axes
from .base import ExtrasForbiddenModel, VersionedModel
from .datasets import DataSets
from .transformations import (
    CoordinateTransformations,
    ScaleTransformation,
    TransformationType,
    TranslationTransformation,
)
from .types import Expected


class Multiscales(ExtrasForbiddenModel, VersionedModel):
    axes: Axes
    datasets: DataSets
    coordinate_transformations: CoordinateTransformations | None = None
    name: Expected[str | None] = None
    type: Expected[str | None] = None
    metadata: Expected[dict | None] = None

    @model_validator(mode="after")
    def check_transformations_match_axes(self) -> "Multiscales":
        num_axes = len(self.axes)
        tfs = self.coordinate_transformations or []
        for dataset in self.datasets:
            tfs += dataset.coordinate_transformations
        for tf in tfs:
            if isinstance(tf, ScaleTransformation):
                assert tf.type == TransformationType.scale
                if len(tf.scale) != num_axes:
                    raise ValueError("There must be a scale for each axis.")
            elif isinstance(tf, TranslationTransformation):
                assert tf.type == TransformationType.translation
                if len(tf.translation) != num_axes:
                    raise ValueError("There must be a translation for each axis.")
        return self
