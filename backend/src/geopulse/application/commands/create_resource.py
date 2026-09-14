from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from geopulse.domain.models.availability import Availability
from geopulse.domain.models.location import Location
from geopulse.domain.models.provider import Provider
from geopulse.domain.models.resource_category import ResourceCategory


@dataclass(frozen=True, slots=True)
class CreateResourceCommand:
    """
    Command requesting creation of a GeoPulse resource.
    """

    id: UUID
    name: str
    category: ResourceCategory
    location: Location
    provider: Provider
    availability: Availability
    created_at: datetime
