from geopulse.application.ports.resource_repository import (
    ResourceRepository,
)
from geopulse.application.queries.find_nearby_resources import (
    FindNearbyResourcesQuery,
)
from geopulse.domain.models.resource import Resource


class ResourceSearchService:
    """
    Application service handling resource search use cases.
    """

    def __init__(
        self,
        repository: ResourceRepository,
    ) -> None:
        self.repository = repository

    def execute(
        self,
        query: FindNearbyResourcesQuery,
    ) -> list[Resource]:

        return self.repository.find_nearby(
            query.location,
            query.radius_km,
        )
