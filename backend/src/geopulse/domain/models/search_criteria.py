from dataclasses import dataclass

from geopulse.domain.models.resource_category import ResourceCategory


@dataclass(frozen=True, slots=True)
class SearchCriteria:
    """
    User search constraints.
    """

    category: ResourceCategory | None
    radius_km: float

    def __post_init__(self) -> None:
        if self.radius_km < 0:
            raise ValueError("radius_km cannot be negative")
