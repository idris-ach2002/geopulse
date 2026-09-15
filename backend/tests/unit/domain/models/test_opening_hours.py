from datetime import time

import pytest

from geopulse.domain.exceptions import InvalidOpeningHoursError
from geopulse.domain.models.opening_hours import OpeningHours


def test_opening_hours_valid() -> None:
    OpeningHours(
        opening=time(8),
        closing=time(18),
    )


def test_opening_hours_invalid() -> None:
    with pytest.raises(InvalidOpeningHoursError):
        OpeningHours(
            opening=time(18),
            closing=time(8),
        )
