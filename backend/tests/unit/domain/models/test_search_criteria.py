import pytest

from geopulse.domain.models.resource_category import ResourceCategory
from geopulse.domain.models.search_criteria import SearchCriteria


def test_search_criteria_creation() -> None:
    criteria = SearchCriteria(
        category=ResourceCategory.FOOD,
        radius_km=5,
    )

    assert criteria.category == ResourceCategory.FOOD
    assert criteria.radius_km == 5


def test_negative_radius_rejected() -> None:
    with pytest.raises(ValueError):
        SearchCriteria(
            category=None,
            radius_km=-1,
        )
