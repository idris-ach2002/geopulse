from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from geopulse.domain.exceptions import InvalidResourceError
from geopulse.domain.models.availability import Availability
from geopulse.domain.models.location import Location
from geopulse.domain.models.provider import Provider
from geopulse.domain.models.resource_category import ResourceCategory


@dataclass(frozen=True, slots=True)
class Resource:
    """
    Domain entity representing a GeoPulse resource.
    """

    id: UUID
    name: str
    category: ResourceCategory
    location: Location
    provider: Provider
    availability: Availability
    created_at: datetime

    def __post_init__(self) -> None:

        if not self.name.strip():
            raise InvalidResourceError("Resource name cannot be empty")

        if self.created_at.tzinfo is None:
            raise InvalidResourceError("created_at must be timezone aware")
