from datetime import UTC, datetime
from uuid import uuid4

import pytest

from geopulse.domain.exceptions import InvalidResourceError
from geopulse.domain.models.availability import Availability
from geopulse.domain.models.location import Location
from geopulse.domain.models.provider import Provider
from geopulse.domain.models.resource import Resource
from geopulse.domain.models.resource_category import ResourceCategory


def create_resource() -> Resource:
    return Resource(
        id=uuid4(),
        name="Water point",
        category=ResourceCategory.WATER,
        location=Location(
            latitude=45,
            longitude=5,
            accuracy_meters=10,
        ),
        provider=Provider(
            id=uuid4(),
            name="City Hall",
        ),
        availability=Availability(
            capacity=10,
            available=5,
            observed_at=datetime.now(UTC),
            received_at=datetime.now(UTC),
        ),
        created_at=datetime.now(UTC),
    )


def test_resource_creation() -> None:
    resource = create_resource()

    assert resource.name == "Water point"


def test_resource_empty_name() -> None:
    with pytest.raises(InvalidResourceError):
        Resource(
            id=uuid4(),
            name=" ",
            category=ResourceCategory.WATER,
            location=Location(45, 5, 10),
            provider=Provider(uuid4(), "City Hall"),
            availability=Availability(
                capacity=10,
                available=5,
                observed_at=datetime.now(UTC),
                received_at=datetime.now(UTC),
            ),
            created_at=datetime.now(UTC),
        )


def test_resource_naive_created_at_rejected() -> None:
    with pytest.raises(InvalidResourceError):
        Resource(
            id=uuid4(),
            name="Water point",
            category=ResourceCategory.WATER,
            location=Location(45, 5, 10),
            provider=Provider(uuid4(), "City Hall"),
            availability=Availability(
                capacity=10,
                available=5,
                observed_at=datetime.now(UTC),
                received_at=datetime.now(UTC),
            ),
            created_at=datetime.now(),
        )
