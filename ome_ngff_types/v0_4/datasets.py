from typing import Annotated

from pydantic import AfterValidator

from .base import ExtrasForbiddenModel
from .transformations import (
    CoordinateTransformations,
    ScaleTransformation,
    TransformationType,
)


class DataSet(ExtrasForbiddenModel):
    path: str
    coordinate_transformations: CoordinateTransformations


def _check_dataset_order(datasets: list[DataSet]) -> list[DataSet]:
    scale_factors = []
    for dataset in datasets:
        for tf in dataset.coordinate_transformations:
            if isinstance(tf, ScaleTransformation):
                assert tf.type == TransformationType.scale
                scale_factors.append(tf.scale)
    assert len(scale_factors) == len(datasets)
    for factors in map(list, zip(*scale_factors)):
        if sorted(factors) != factors:
            raise ValueError("The datasets must be sorted from largest to smallest.")
    return datasets


DataSets = Annotated[list[DataSet], AfterValidator(_check_dataset_order)]
