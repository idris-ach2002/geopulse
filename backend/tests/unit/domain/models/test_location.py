from dataclasses import FrozenInstanceError

import pytest

from geopulse.domain.exceptions import InvalidLocationError
from geopulse.domain.models.location import Location


def test_valid_location_creation() -> None:
    location = Location(
        latitude=45.1885,
        longitude=5.7245,
        accuracy_meters=10,
    )

    assert location.latitude == 45.1885


def test_latitude_out_of_range() -> None:
    with pytest.raises(InvalidLocationError):
        Location(
            latitude=100,
            longitude=5,
            accuracy_meters=10,
        )


def test_longitude_out_of_range() -> None:
    with pytest.raises(InvalidLocationError):
        Location(
            latitude=45,
            longitude=200,
            accuracy_meters=10,
        )


def test_negative_accuracy_rejected() -> None:
    with pytest.raises(InvalidLocationError):
        Location(
            latitude=45,
            longitude=5,
            accuracy_meters=-1,
        )


def test_location_is_immutable() -> None:
    location = Location(
        latitude=45,
        longitude=5,
        accuracy_meters=10,
    )

    with pytest.raises(FrozenInstanceError):
        location.latitude = 50
