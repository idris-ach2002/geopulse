from dataclasses import replace
from datetime import UTC, datetime, timedelta, timezone

from hypothesis import given
from hypothesis import strategies as st

from geopulse.domain.models.availability import Availability
from geopulse.domain.rules.freshness import FreshnessPolicy

NOW = datetime(2026, 9, 14, 18, tzinfo=UTC)
max_ages = st.integers(min_value=0, max_value=100_000)
ages = st.timedeltas(min_value=timedelta(0), max_value=timedelta(days=100))


@given(max_age=max_ages)
def test_observations_at_limit_are_fresh(max_age: int) -> None:
    availability = Availability(None, 20, NOW - timedelta(minutes=max_age), NOW)

    assert FreshnessPolicy(max_age).is_fresh(availability, now=NOW)


@given(
    max_age=max_ages,
    ahead=st.timedeltas(min_value=timedelta(microseconds=1), max_value=timedelta(days=100)),
)
def test_future_observations_are_never_fresh(max_age: int, ahead: timedelta) -> None:
    assert not FreshnessPolicy(max_age).is_fresh(Availability(None, 20, NOW + ahead, NOW), now=NOW)


@given(
    max_age=max_ages,
    extra=st.timedeltas(min_value=timedelta(microseconds=1), max_value=timedelta(days=100)),
)
def test_observations_older_than_limit_are_never_fresh(max_age: int, extra: timedelta) -> None:
    observed_at = NOW - timedelta(minutes=max_age) - extra

    assert not FreshnessPolicy(max_age).is_fresh(Availability(None, 20, observed_at, NOW), now=NOW)


@given(max_age=max_ages, age=ages, increase=max_ages)
def test_increasing_limit_cannot_make_fresh_observation_stale(
    max_age: int, age: timedelta, increase: int
) -> None:
    availability = Availability(None, 20, NOW - age, NOW)

    if FreshnessPolicy(max_age).is_fresh(availability, now=NOW):
        assert FreshnessPolicy(max_age + increase).is_fresh(availability, now=NOW)


@given(max_age=max_ages, age=ages, elapsed=ages)
def test_stale_observations_remain_stale_as_time_passes(
    max_age: int, age: timedelta, elapsed: timedelta
) -> None:
    availability = Availability(None, 20, NOW - age, NOW)
    policy = FreshnessPolicy(max_age)

    if not policy.is_fresh(availability, now=NOW):
        assert not policy.is_fresh(availability, now=NOW + elapsed)


@given(max_age=max_ages, age=ages, receipt_delay=ages)
def test_receipt_time_does_not_affect_freshness(
    max_age: int, age: timedelta, receipt_delay: timedelta
) -> None:
    availability = Availability(None, 20, NOW - age, NOW)
    policy = FreshnessPolicy(max_age)

    assert policy.is_fresh(availability, now=NOW) == policy.is_fresh(
        replace(availability, received_at=NOW + receipt_delay), now=NOW
    )


@given(max_age=max_ages, age=ages, offset=st.integers(min_value=-1439, max_value=1439))
def test_timezone_representation_does_not_affect_freshness(
    max_age: int, age: timedelta, offset: int
) -> None:
    availability = Availability(None, 20, NOW - age, NOW)
    policy = FreshnessPolicy(max_age)
    zone = timezone(timedelta(minutes=offset))

    assert policy.is_fresh(availability, now=NOW) == policy.is_fresh(
        replace(availability, observed_at=availability.observed_at.astimezone(zone)),
        now=NOW.astimezone(zone),
    )
