from typing import Protocol

from geopulse.domain.models.location import Location
from geopulse.domain.models.resource import Resource


class ResourceRepository(Protocol):
    """
    Port defining resource persistence operations.

    Implementations belong to infrastructure layer.
    """

    def find_nearby(
        self,
        location: Location,
        radius_km: float,
    ) -> list[Resource]:
        """
        Find resources around a geographic position.
        """

    def save(
        self,
        resource: Resource,
    ) -> None:
        """
        Persist a resource.
        """
