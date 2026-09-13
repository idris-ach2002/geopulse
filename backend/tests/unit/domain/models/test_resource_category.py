from geopulse.domain.models.resource_category import ResourceCategory


def test_category_values() -> None:
    assert ResourceCategory.FOOD.value == "food"
