from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from geopulse.domain.exceptions import (
    InvalidDateTimeError,
    InvalidFreshnessPolicyError,
)
from geopulse.domain.models.availability import Availability
from geopulse.domain.models.resource_category import ResourceCategory
from geopulse.domain.rules.freshness import (
    FreshnessPolicy,
    FreshnessState,
    FreshnessThresholds,
)

NOW = datetime(2026, 9, 14, 18, tzinfo=UTC)


def availability_at(age: timedelta) -> Availability:
    return Availability(
        capacity=100,
        available=20,
        observed_at=NOW - age,
        received_at=NOW,
    )


@pytest.mark.parametrize(
    ("age", "expected"),
    [
        (timedelta(seconds=0), FreshnessState.FRESH),
        (timedelta(seconds=60), FreshnessState.FRESH),
        (timedelta(seconds=61), FreshnessState.ACCEPTABLE),
        (timedelta(seconds=180), FreshnessState.ACCEPTABLE),
        (timedelta(seconds=181), FreshnessState.STALE),
        (timedelta(seconds=300), FreshnessState.STALE),
        (
            timedelta(seconds=301),
            FreshnessState.EXPIRED,
        ),
    ],
)
def test_piecewise_freshness_states(
    age: timedelta,
    expected: FreshnessState,
) -> None:
    result = FreshnessPolicy().evaluate(
        availability_at(age),
        now=NOW,
    )

    assert result.state is expected


def test_future_observation_is_expired() -> None:
    availability = Availability(
        capacity=100,
        available=20,
        observed_at=NOW + timedelta(seconds=1),
        received_at=NOW,
    )

    result = FreshnessPolicy().evaluate(
        availability,
        now=NOW,
    )

    assert result.state is FreshnessState.EXPIRED


def test_provider_policy_has_priority() -> None:
    provider_id = uuid4()

    policy = FreshnessPolicy(
        by_category={
            ResourceCategory.PARKING: FreshnessThresholds(
                10,
                20,
                30,
            )
        },
        by_provider={
            provider_id: FreshnessThresholds(
                100,
                200,
                300,
            )
        },
    )

    result = policy.evaluate(
        availability_at(timedelta(seconds=50)),
        now=NOW,
        category=ResourceCategory.PARKING,
        provider_id=provider_id,
    )

    assert result.state is FreshnessState.FRESH


def test_category_policy_overrides_default() -> None:
    policy = FreshnessPolicy(
        by_category={
            ResourceCategory.PARKING: FreshnessThresholds(
                10,
                20,
                30,
            )
        }
    )

    result = policy.evaluate(
        availability_at(timedelta(seconds=50)),
        now=NOW,
        category=ResourceCategory.PARKING,
    )

    assert result.state is FreshnessState.EXPIRED


def test_negative_threshold_is_rejected() -> None:
    with pytest.raises(InvalidFreshnessPolicyError):
        FreshnessThresholds(-1, 10, 20)


def test_unordered_thresholds_are_rejected() -> None:
    with pytest.raises(InvalidFreshnessPolicyError):
        FreshnessThresholds(20, 10, 30)


def test_naive_now_is_rejected() -> None:
    with pytest.raises(InvalidDateTimeError):
        FreshnessPolicy().evaluate(
            availability_at(timedelta(seconds=10)),
            now=NOW.replace(tzinfo=None),
        )
