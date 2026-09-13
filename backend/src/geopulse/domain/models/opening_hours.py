from dataclasses import dataclass
from datetime import time

from geopulse.domain.exceptions import InvalidOpeningHoursError


@dataclass(frozen=True, slots=True)
class OpeningHours:
    """
    Daily opening interval.
    """

    opening: time
    closing: time

    def __post_init__(self) -> None:
        if self.opening >= self.closing:
            raise InvalidOpeningHoursError("Opening time must be before closing time")
