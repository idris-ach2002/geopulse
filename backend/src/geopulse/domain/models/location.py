from dataclasses import dataclass


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

        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Invalid latitude: {self.latitude}")

        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Invalid longitude: {self.longitude}")

        if self.accuracy_meters < 0:
            raise ValueError(f"Invalid accuracy: {self.accuracy_meters}")
