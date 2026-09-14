from datetime import UTC, datetime, timedelta

from hypothesis import given
from hypothesis import strategies as st

from geopulse.domain.models.availability import Availability
from geopulse.domain.rules.freshness import (
    FreshnessPolicy,
    FreshnessState,
)

NOW = datetime(2026, 9, 14, 18, tzinfo=UTC)


@given(
    age_seconds=st.integers(
        min_value=0,
        max_value=60,
    )
)
def test_age_inside_fresh_window_is_fresh(
    age_seconds: int,
) -> None:
    availability = Availability(
        capacity=None,
        available=20,
        observed_at=NOW - timedelta(seconds=age_seconds),
        received_at=NOW,
    )

    result = FreshnessPolicy().evaluate(
        availability,
        now=NOW,
    )

    assert result.state is FreshnessState.FRESH


@given(
    age_seconds=st.integers(
        min_value=301,
        max_value=100_000,
    )
)
def test_age_beyond_stale_window_is_expired(
    age_seconds: int,
) -> None:
    availability = Availability(
        capacity=None,
        available=20,
        observed_at=NOW - timedelta(seconds=age_seconds),
        received_at=NOW,
    )

    result = FreshnessPolicy().evaluate(
        availability,
        now=NOW,
    )

    assert result.state is FreshnessState.EXPIRED


@given(
    receipt_delay=st.integers(
        min_value=0,
        max_value=100_000,
    )
)
def test_received_at_never_changes_freshness(
    receipt_delay: int,
) -> None:
    observed_at = NOW - timedelta(seconds=120)

    first = Availability(
        capacity=None,
        available=20,
        observed_at=observed_at,
        received_at=NOW,
    )

    second = Availability(
        capacity=None,
        available=20,
        observed_at=observed_at,
        received_at=NOW + timedelta(seconds=receipt_delay),
    )

    policy = FreshnessPolicy()

    assert (
        policy.evaluate(
            first,
            now=NOW,
        ).state
        is policy.evaluate(
            second,
            now=NOW,
        ).state
    )
