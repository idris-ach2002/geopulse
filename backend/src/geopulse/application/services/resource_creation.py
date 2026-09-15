from geopulse.application.commands.create_resource import (
    CreateResourceCommand,
)
from geopulse.application.ports.resource_repository import (
    ResourceRepository,
)
from geopulse.domain.models.resource import Resource


class ResourceCreationService:
    """
    Application service responsible for resource creation.
    """

    def __init__(
        self,
        repository: ResourceRepository,
    ) -> None:
        self.repository = repository

    def execute(
        self,
        command: CreateResourceCommand,
    ) -> Resource:

        resource = Resource(
            id=command.id,
            name=command.name,
            category=command.category,
            location=command.location,
            provider=command.provider,
            availability=command.availability,
            created_at=command.created_at,
        )

        self.repository.save(resource)

        return resource
