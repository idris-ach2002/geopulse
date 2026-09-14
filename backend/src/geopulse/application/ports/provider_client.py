from collections.abc import Sequence
from typing import Protocol

from geopulse.domain.models.resource import Resource


class ProviderClient(Protocol):
    """Port for retrieving resources from an external provider."""

    async def fetch_resources(self) -> Sequence[Resource]:
        """Fetch provider resources without exposing provider technology."""
        ...
