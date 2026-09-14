from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from geopulse.domain.exceptions import (
    InvalidDateTimeError,
    InvalidFreshnessPolicyError,
)
from geopulse.domain.models.availability import Availability


@dataclass(frozen=True, slots=True)
class FreshnessPolicy:
    """Accept observations aged from zero to max_age_minutes, inclusive."""

    max_age_minutes: int

    def __post_init__(self) -> None:
        if self.max_age_minutes < 0:
            raise InvalidFreshnessPolicyError("Maximum age cannot be negative")

    def is_fresh(self, availability: Availability, *, now: datetime | None = None) -> bool:
        """Check observed_at against an aware reference time (current UTC by default).

        Future observations are not fresh. received_at does not affect freshness.

        Note : Chaque timezone dans le monde est définie par rapport à UTC (le temps universel).

        Si on est à l’est de UTC → on est en avance → offset positif
        Exemple : Paris (UTC+2 l’été) → +02:00

        Si on est à l’ouest de UTC → on est en retard → offset négatif
        Exemple : New York (UTC−5) → -05:00

        ------------------------
        ```
        from datetime import datetime, timezone, timedelta

        paris = timezone(timedelta(hours=2))
        ny = timezone(timedelta(hours=-5))

        print(datetime.now(paris).utcoffset())  # 2:00:00
        print(datetime.now(ny).utcoffset())     # -5:00:00
        ```

        Il faut vérifier que les dates sont timezone-aware
        Sinon, impossible de comparer correctement des dates venant de différents fuseaux.
        ainsi ```if now.utcoffset() is None``` est incontournable
        """
        if now is None:
            now = datetime.now(UTC)
        if now.utcoffset() is None or availability.observed_at.utcoffset() is None:
            raise InvalidDateTimeError("Datetime must be timezone aware")

        age: timedelta = now.astimezone(UTC) - availability.observed_at.astimezone(UTC)
        return timedelta(0) <= age <= timedelta(minutes=self.max_age_minutes)
