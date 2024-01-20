from collections import Counter
from enum import Enum
from typing import Annotated, Literal

from pydantic import AfterValidator

from .base import ExtrasForbiddenModel


class TransformationType(str, Enum):
    identity = "identity"
    translation = "translation"
    scale = "scale"


class IdentityTransformation(ExtrasForbiddenModel):
    type: Literal[TransformationType.identity] = TransformationType.identity


class TranslationTransformation(ExtrasForbiddenModel):
    type: Literal[TransformationType.translation] = TransformationType.translation
    translation: list[float]


class ScaleTransformation(ExtrasForbiddenModel):
    type: Literal[TransformationType.scale] = TransformationType.scale
    scale: list[float]


CoordinateTransformation = (
    IdentityTransformation | TranslationTransformation | ScaleTransformation
)


def _check_transformation_tally(
    tfs: list[CoordinateTransformation],
) -> list[CoordinateTransformation]:
    tf_counts = Counter([tf.type for tf in tfs])
    tf_list = list(tf_counts)
    if set(tf_counts) > {TransformationType.translation, TransformationType.scale}:
        raise ValueError("All transformations must be of type translation or scale.")
    if tf_counts[TransformationType.scale] != 1:
        raise ValueError("There must be exactly one scale transformation.")
    if tf_list.index(TransformationType.scale) != 0:
        raise ValueError("The scale transformation must come first.")
    if tf_counts[TransformationType.translation] > 1:
        raise ValueError("There may only be one translation transformation.")
    return tfs


CoordinateTransformations = Annotated[
    list[CoordinateTransformation], AfterValidator(_check_transformation_tally)
]
