from enum import StrEnum


class ResourceCategory(StrEnum):
    """Stable internal resource categories."""

    PARKING = "parking"
    EV_CHARGING = "ev_charging"
    PHARMACY = "pharmacy"
    SHOP = "shop"

    # Extensions already used by current development fixtures/tests.
    WATER = "water"
    FOOD = "food"
    HEALTH = "health"
    TRANSPORT = "transport"
    SHELTER = "shelter"
    OTHER = "other"
