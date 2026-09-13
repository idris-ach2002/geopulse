from dataclasses import dataclass
from datetime import datetime

from geopulse.domain.exceptions import InvalidAvailabilityError


@dataclass(frozen=True, slots=True)
class Availability:
    """
    Availability observation.

    observed_at:
        when the information was true.

    received_at:
        when GeoPulse received the information.
    """

    capacity: int | None
    available: int
    observed_at: datetime
    received_at: datetime

    def __post_init__(self) -> None:

        if self.available < 0:
            raise InvalidAvailabilityError("Available cannot be negative")

        if self.capacity is not None:
            if self.capacity < 0:
                raise InvalidAvailabilityError("Capacity cannot be negative")

            if self.available > self.capacity:
                raise InvalidAvailabilityError("Available cannot exceed capacity")

        for value in (
            self.observed_at,
            self.received_at,
        ):
            if value.tzinfo is None:
                raise InvalidAvailabilityError("Datetime must be timezone aware")
