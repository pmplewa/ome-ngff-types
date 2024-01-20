import json
from contextlib import nullcontext
from pathlib import Path
from typing import ContextManager

import pytest
from pydantic import ValidationError

from ome_ngff_types.v0_4 import Metadata

SAMPLE_FILES = list((Path(__file__).parent / "samples").glob("*.json"))


@pytest.mark.parametrize("path", SAMPLE_FILES, ids=[path.stem for path in SAMPLE_FILES])
def test_samples(path: Path):
    with open(path) as json_file:
        ctx: ContextManager = nullcontext()
        if path.stem == "idr0052A_5514375":
            ctx = pytest.raises(ValidationError, match="omero.channels.[0-9].window")
        with ctx:
            Metadata.model_validate(json.load(json_file))
