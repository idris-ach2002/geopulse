import pytest
from hypothesis import given
from hypothesis import strategies as st

from geopulse.domain.exceptions import InvalidLocationError
from geopulse.domain.models.location import Location


@given(
    latitude=st.floats(
        min_value=-90,
        max_value=90,
        allow_nan=False,
        allow_infinity=False,
    ),
    longitude=st.floats(
        min_value=-180,
        max_value=180,
        allow_nan=False,
        allow_infinity=False,
    ),
    accuracy=st.floats(
        min_value=0,
        max_value=10000,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_valid_coordinates_always_create_location(
    latitude: float,
    longitude: float,
    accuracy: float,
) -> None:
    location = Location(
        latitude=latitude,
        longitude=longitude,
        accuracy_meters=accuracy,
    )

    assert location.latitude == latitude
    assert location.longitude == longitude
    assert location.accuracy_meters == accuracy


@given(
    latitude=st.floats(
        min_value=90.000001,
        max_value=1000,
        allow_nan=False,
        allow_infinity=False,
    )
)
def test_invalid_latitude_is_always_rejected(
    latitude: float,
) -> None:
    with pytest.raises(InvalidLocationError):
        Location(
            latitude=latitude,
            longitude=0,
            accuracy_meters=1,
        )


@given(
    longitude=st.floats(
        min_value=180.000001,
        max_value=1000,
        allow_nan=False,
        allow_infinity=False,
    )
)
def test_invalid_longitude_is_always_rejected(
    longitude: float,
) -> None:
    with pytest.raises(InvalidLocationError):
        Location(
            latitude=0,
            longitude=longitude,
            accuracy_meters=1,
        )
