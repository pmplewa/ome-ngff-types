# OME-NGFF Types

This package contains `pydantic` models to represent and validate
[OME-NGFF](https://ngff.openmicroscopy.org) metadata, according to version
[0.4](https://ngff.openmicroscopy.org/0.4) of the
[NGFF specification](https://ngff.openmicroscopy.org/specifications).

The included models cover the `axes`, `coordinateTransformations`,
`multiscales`, `omero`, `labels`, `image-label`, `plate`, and `well` metadata.
They implement all requirements from the specification, as well as the following
constraints that are **slightly more restrictive** than the original versions.

### Axis Metadata

- The value of the field `type` **MUST** be one of `space`, `time` or `channel`.
- The value of the field `unit` **MUST** be one of the `UDUNITS-2` units.

### Coordinate Transformation Metadata

- Both translation vectors and scale vectors **MUST** be specified as a list of
  floats.

## Installation

To install the latest development version, run:

```bash
pip install git+https://github.com/pmplewa/ome-ngff-types.git
```

## Examples

```python
import zarr

from ome_ngff_types.v0_4 import Metadata

group = zarr.open("https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0044A/4007801.zarr")
metadata = Metadata.model_validate(group.attrs)

assert metadata.multiscales is not None
multiscales = metadata.multiscales[0]
assert multiscales.version == "0.4"
```

## Sample Data

The sample data for testing this package has been aggregated from the
specification itself, as well as the following public datasets:

```
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0044A/4007801.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0047A/4496763.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0048A/9846152.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0052A/5514375.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0054A/5025551.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0054A/5025552.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0054A/5025553.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0062A/6001240.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0062A/6001247.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0073A/9798462.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0076A/10501752.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0083A/9822152.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0101A/13457227.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0101A/13457537.zarr
https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.4/idr0101A/13457539.zarr
```
