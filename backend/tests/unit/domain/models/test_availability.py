from datetime import UTC, datetime

import pytest

from geopulse.domain.exceptions import InvalidAvailabilityError
from geopulse.domain.models.availability import Availability


def test_availability_valid() -> None:
    Availability(
        capacity=10,
        available=5,
        observed_at=datetime.now(UTC),
        received_at=datetime.now(UTC),
    )


def test_available_cannot_exceed_capacity() -> None:
    with pytest.raises(InvalidAvailabilityError):
        Availability(
            capacity=5,
            available=10,
            observed_at=datetime.now(UTC),
            received_at=datetime.now(UTC),
        )
