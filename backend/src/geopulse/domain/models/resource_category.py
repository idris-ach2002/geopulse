from enum import StrEnum


class ResourceCategory(StrEnum):
    """
    Category of a GeoPulse resource.
    """

    WATER = "water"
    FOOD = "food"
    HEALTH = "health"
    TRANSPORT = "transport"
    SHELTER = "shelter"
    OTHER = "other"
