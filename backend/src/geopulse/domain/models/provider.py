from dataclasses import dataclass
from uuid import UUID

from geopulse.domain.exceptions import InvalidProviderError


@dataclass(frozen=True, slots=True)
class Provider:
    """
    Organization providing resources.
    """

    id: UUID
    name: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise InvalidProviderError("Provider name cannot be empty")
