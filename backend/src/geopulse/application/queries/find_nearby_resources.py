from dataclasses import dataclass

from geopulse.application.exceptions import InvalidRadiusError
from geopulse.domain.models.location import Location


@dataclass(frozen=True, slots=True)
class FindNearbyResourcesQuery:
    """
    Request to find resources around a location.
    """

    location: Location
    radius_km: float

    def __post_init__(self) -> None:
        if self.radius_km < 0:
            raise InvalidRadiusError("Radius cannot be negative")
