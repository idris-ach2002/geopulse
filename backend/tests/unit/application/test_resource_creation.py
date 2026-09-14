from datetime import UTC, datetime
from uuid import uuid4

from geopulse.application.commands.create_resource import (
    CreateResourceCommand,
)
from geopulse.application.services.resource_creation import (
    ResourceCreationService,
)
from geopulse.domain.models.availability import Availability
from geopulse.domain.models.location import Location
from geopulse.domain.models.provider import Provider
from geopulse.domain.models.resource_category import ResourceCategory


class FakeResourceRepository:
    def __init__(self) -> None:
        self.saved = None

    def save(self, resource) -> None:
        self.saved = resource


def create_command() -> CreateResourceCommand:
    return CreateResourceCommand(
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


def test_resource_creation_service_creates_resource() -> None:

    repository = FakeResourceRepository()

    service = ResourceCreationService(repository)

    command = create_command()

    resource = service.execute(command)

    assert resource.name == "Water point"
    assert repository.saved == resource


def test_created_resource_keeps_command_values() -> None:

    repository = FakeResourceRepository()

    service = ResourceCreationService(repository)

    command = create_command()

    resource = service.execute(command)

    assert resource.location == command.location
    assert resource.category == command.category
