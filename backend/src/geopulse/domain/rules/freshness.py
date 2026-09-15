from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from types import MappingProxyType
from uuid import UUID

from geopulse.domain.exceptions import (
    InvalidDateTimeError,
    InvalidFreshnessPolicyError,
)
from geopulse.domain.models.availability import Availability
from geopulse.domain.models.resource_category import ResourceCategory


class FreshnessState(StrEnum):
    """Piecewise freshness states defined by V1."""

    FRESH = "fresh"
    ACCEPTABLE = "acceptable"
    STALE = "stale"
    EXPIRED = "expired"


@dataclass(frozen=True, slots=True)
class FreshnessThresholds:
    """Increasing age thresholds expressed in seconds."""

    fresh_until_s: int
    acceptable_until_s: int
    stale_until_s: int

    def __post_init__(self) -> None:
        if self.fresh_until_s < 0:
            raise InvalidFreshnessPolicyError("Fresh threshold cannot be negative")

        if not (self.fresh_until_s <= self.acceptable_until_s <= self.stale_until_s):
            raise InvalidFreshnessPolicyError("Freshness thresholds must be ordered")


@dataclass(frozen=True, slots=True)
class Freshness:
    """Result of evaluating the age of an observation."""

    state: FreshnessState
    age_s: float
    score: float | None = None

    def __post_init__(self) -> None:
        if self.age_s < 0:
            raise InvalidFreshnessPolicyError("Freshness age cannot be negative")

        if self.score is not None and not 0 <= self.score <= 1:
            raise InvalidFreshnessPolicyError("Freshness score must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class FreshnessPolicy:
    """Piecewise policy configurable by resource category or provider.

    Provider-specific thresholds take precedence over category thresholds,
    which take precedence over the default thresholds.

    `now` is always injected by the caller. The domain never obtains the
    current clock implicitly.
    """

    default: FreshnessThresholds = field(
        default_factory=lambda: FreshnessThresholds(
            fresh_until_s=60,
            acceptable_until_s=180,
            stale_until_s=300,
        )
    )
    by_category: Mapping[ResourceCategory, FreshnessThresholds] = field(default_factory=dict)
    by_provider: Mapping[UUID, FreshnessThresholds] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "by_category",
            MappingProxyType(dict(self.by_category)),
        )
        object.__setattr__(
            self,
            "by_provider",
            MappingProxyType(dict(self.by_provider)),
        )

    def evaluate(
        self,
        availability: Availability,
        *,
        now: datetime,
        category: ResourceCategory | None = None,
        provider_id: UUID | None = None,
    ) -> Freshness:
        """Evaluate freshness from observed_at, never received_at."""

        if now.utcoffset() is None:
            raise InvalidDateTimeError("Datetime must be timezone aware")

        observed_at = availability.observed_at

        if observed_at.utcoffset() is None:
            raise InvalidDateTimeError("Datetime must be timezone aware")

        age = now.astimezone(UTC) - observed_at.astimezone(UTC)

        # A future observation must never be promoted to fresh.
        if age < timedelta(0):
            return Freshness(
                state=FreshnessState.EXPIRED,
                age_s=0.0,
                score=0.0,
            )

        age_s = age.total_seconds()
        thresholds = self._thresholds(
            category=category,
            provider_id=provider_id,
        )

        if age_s <= thresholds.fresh_until_s:
            state = FreshnessState.FRESH
            score = 1.0
        elif age_s <= thresholds.acceptable_until_s:
            state = FreshnessState.ACCEPTABLE
            score = 0.75
        elif age_s <= thresholds.stale_until_s:
            state = FreshnessState.STALE
            score = 0.25
        else:
            state = FreshnessState.EXPIRED
            score = 0.0

        return Freshness(
            state=state,
            age_s=age_s,
            score=score,
        )

    def _thresholds(
        self,
        *,
        category: ResourceCategory | None,
        provider_id: UUID | None,
    ) -> FreshnessThresholds:
        if provider_id is not None and provider_id in self.by_provider:
            return self.by_provider[provider_id]

        if category is not None and category in self.by_category:
            return self.by_category[category]

        return self.default
