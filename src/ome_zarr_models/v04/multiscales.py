from typing import Any

from pydantic import Field, field_validator

from ome_zarr_models.base import Base
from ome_zarr_models.utils import unique_items_validator
from ome_zarr_models.v04.axes import Axis
from ome_zarr_models.v04.coordinate_transformations import (
    PathScale,
    PathTranslation,
    VectorScale,
    VectorTranslation,
)
from ome_zarr_models.v04.omero import Omero


class Dataset(Base):
    """
    Model for an element of `Multiscale.datasets`.

    See https://ngff.openmicroscopy.org/0.4/#multiscale-md
    """

    # TODO: validate that path resolves to an actual zarr array
    path: str
    # TODO: validate that transforms are consistent w.r.t dimensionality
    coordinateTransformations: (
        tuple[VectorScale | PathScale]
        | tuple[VectorScale | PathScale, VectorTranslation | PathTranslation]
    )


class Multiscale(Base):
    """
    Model for an element of `NgffImageMeta.multiscales`.

    See https://ngff.openmicroscopy.org/0.4/#multiscale-md.
    """

    datasets: list[Dataset] = Field(..., min_length=1)
    version: Any | None = None
    # TODO: validate correctness of axes
    # TODO: validate uniqueness of axes
    axes: list[Axis] = Field(..., max_length=5, min_length=2)
    coordinateTransformations: (
        tuple[VectorScale | PathScale]
        | tuple[VectorScale | PathScale, VectorTranslation | PathTranslation]
        | None
    ) = None
    metadata: Any = None
    name: Any | None = None
    type: Any = None
    _check_unique = field_validator("axes")(unique_items_validator)


class MultiscaleGroupAttrs(Base):
    """
    Model for the metadata of a NGFF image.

    See https://ngff.openmicroscopy.org/0.4/#image-layout.
    """

    multiscales: list[Multiscale] = Field(
        ...,
        description="The multiscale datasets for this image",
        min_length=1,
    )
    omero: Omero | None = None
    _check_unique = field_validator("multiscales")(unique_items_validator)
