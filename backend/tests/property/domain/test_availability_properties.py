from datetime import UTC, datetime

import pytest
from hypothesis import given
from hypothesis import strategies as st

from geopulse.domain.exceptions import InvalidAvailabilityError
from geopulse.domain.models.availability import Availability


@given(
    capacity=st.integers(min_value=0, max_value=10000),
)
def test_available_zero_is_always_valid(
    capacity: int,
) -> None:
    availability = Availability(
        capacity=capacity,
        available=0,
        observed_at=datetime.now(UTC),
        received_at=datetime.now(UTC),
    )

    assert availability.available == 0


@given(
    capacity=st.integers(min_value=0, max_value=10000),
    extra=st.integers(min_value=1, max_value=10000),
)
def test_available_above_capacity_is_always_rejected(
    capacity: int,
    extra: int,
) -> None:
    with pytest.raises(InvalidAvailabilityError):
        Availability(
            capacity=capacity,
            available=capacity + extra,
            observed_at=datetime.now(UTC),
            received_at=datetime.now(UTC),
        )


@given(
    available=st.integers(
        min_value=-10000,
        max_value=-1,
    )
)
def test_negative_available_is_always_rejected(
    available: int,
) -> None:
    with pytest.raises(InvalidAvailabilityError):
        Availability(
            capacity=10,
            available=available,
            observed_at=datetime.now(UTC),
            received_at=datetime.now(UTC),
        )
