from typing import Protocol
from uuid import UUID

from geopulse.domain.models.availability import Availability


class AvailabilityRepository(Protocol):
    """Persistence port for current resource availability."""

    def get_current(self, resource_id: UUID) -> Availability | None:
        """Return current availability when known."""
        ...

    def save_current(self, availability: Availability) -> None:
        """Persist the current availability state."""
        ...
