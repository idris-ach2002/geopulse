import math
from dataclasses import dataclass

from geopulse.domain.exceptions import InvalidLocationError


@dataclass(frozen=True, slots=True)
class Location:
    """
    Immutable geographical location.

    Invariants:
    - latitude ∈ [-90, 90]
    - longitude ∈ [-180, 180]
    - accuracy_meters >= 0
    """

    latitude: float
    longitude: float
    accuracy_meters: float

    def __post_init__(self) -> None:

        if not math.isfinite(self.latitude):
            raise InvalidLocationError("Latitude must be finite")

        if not math.isfinite(self.longitude):
            raise InvalidLocationError("Longitude must be finite")

        if not math.isfinite(self.accuracy_meters):
            raise InvalidLocationError("Accuracy must be finite")

        if not -90 <= self.latitude <= 90:
            raise InvalidLocationError(f"Invalid latitude: {self.latitude}")

        if not -180 <= self.longitude <= 180:
            raise InvalidLocationError(f"Invalid longitude: {self.longitude}")

        if self.accuracy_meters < 0:
            raise InvalidLocationError(f"Invalid accuracy: {self.accuracy_meters}")
