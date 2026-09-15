from datetime import UTC, datetime
from uuid import uuid4

import pytest

from geopulse.application.exceptions import (
    InvalidRadiusError,
)
from geopulse.application.queries.find_nearby_resources import (
    FindNearbyResourcesQuery,
)
from geopulse.application.services.resource_search import (
    ResourceSearchService,
)
from geopulse.domain.models.availability import Availability
from geopulse.domain.models.location import Location
from geopulse.domain.models.provider import Provider
from geopulse.domain.models.resource import Resource
from geopulse.domain.models.resource_category import ResourceCategory


class FakeResourceRepository:
    def __init__(self, resources: list[Resource]) -> None:
        self.resources = resources
        self.received_location = None
        self.received_radius = None

    def find_nearby(
        self,
        location: Location,
        radius_km: float,
    ) -> list[Resource]:

        self.received_location = location
        self.received_radius = radius_km

        return self.resources


def create_resource() -> Resource:
    return Resource(
        id=uuid4(),
        name="Water point",
        category=ResourceCategory.WATER,
        location=Location(
            45,
            5,
            10,
        ),
        provider=Provider(
            uuid4(),
            "City Hall",
        ),
        availability=Availability(
            capacity=10,
            available=5,
            observed_at=datetime.now(UTC),
            received_at=datetime.now(UTC),
        ),
        created_at=datetime.now(UTC),
    )


def test_resource_search_service_returns_repository_results() -> None:
    resource = create_resource()

    repository = FakeResourceRepository([resource])

    service = ResourceSearchService(repository)

    query = FindNearbyResourcesQuery(
        location=Location(45, 5, 10),
        radius_km=5,
    )

    result = service.execute(query)

    assert result == [resource]
    assert repository.received_radius == 5


def test_find_nearby_query_rejects_negative_radius() -> None:
    with pytest.raises(InvalidRadiusError, match="Radius cannot be negative"):
        FindNearbyResourcesQuery(
            location=Location(45, 5, 10),
            radius_km=-1,
        )
