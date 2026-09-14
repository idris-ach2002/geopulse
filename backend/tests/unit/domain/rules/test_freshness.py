from datetime import UTC, datetime, timedelta, timezone, tzinfo
from unittest.mock import patch
from zoneinfo import ZoneInfo

import pytest

from geopulse.domain.exceptions import (
    InvalidDateTimeError,
    InvalidFreshnessPolicyError,
)
from geopulse.domain.models.availability import Availability
from geopulse.domain.rules.freshness import FreshnessPolicy

NOW = datetime(2026, 9, 14, 18, tzinfo=UTC)


@pytest.mark.parametrize(
    ("age", "expected"),
    [
        (timedelta(0), True),
        (timedelta(minutes=15), True),
        (timedelta(minutes=30), True),
        (timedelta(minutes=30, microseconds=1), False),
        (timedelta(hours=8), False),
        (timedelta(microseconds=-1), False),
    ],
)
def test_freshness_by_observation_age(age: timedelta, expected: bool) -> None:
    availability = Availability(None, 20, NOW - age, NOW)

    assert FreshnessPolicy(max_age_minutes=30).is_fresh(availability, now=NOW) is expected


def test_negative_maximum_age_is_rejected() -> None:
    with pytest.raises(InvalidFreshnessPolicyError, match="Maximum age cannot be negative"):
        FreshnessPolicy(max_age_minutes=-1)


def test_zero_maximum_age_only_accepts_current_observation() -> None:
    policy = FreshnessPolicy(max_age_minutes=0)

    assert policy.is_fresh(Availability(None, 20, NOW, NOW), now=NOW)
    assert not policy.is_fresh(
        Availability(None, 20, NOW - timedelta(microseconds=1), NOW), now=NOW
    )


def test_current_utc_time_is_used_by_default() -> None:
    availability = Availability(None, 20, NOW - timedelta(minutes=15), NOW)

    with patch("geopulse.domain.rules.freshness.datetime") as clock:
        clock.now.return_value = NOW

        assert FreshnessPolicy(30).is_fresh(availability)
        clock.now.assert_called_once_with(UTC)


def test_naive_reference_time_is_rejected() -> None:
    with pytest.raises(InvalidDateTimeError, match="Datetime must be timezone aware"):
        FreshnessPolicy(30).is_fresh(Availability(None, 20, NOW, NOW), now=NOW.replace(tzinfo=None))


def test_observation_with_undefined_utc_offset_is_rejected() -> None:
    # A tzinfo object alone does not guarantee that a datetime is aware.
    class UndefinedOffset(tzinfo):
        def utcoffset(self, dt: datetime | None) -> None:
            return None

    observed_at = NOW.replace(tzinfo=UndefinedOffset())
    with pytest.raises(InvalidDateTimeError, match="Datetime must be timezone aware"):
        FreshnessPolicy(30).is_fresh(Availability(None, 20, observed_at, NOW), now=NOW)


def test_different_timezones_representing_same_instant() -> None:
    observed_at = NOW.astimezone(timezone(timedelta(hours=2)))

    assert FreshnessPolicy(0).is_fresh(Availability(None, 20, observed_at, NOW), now=NOW)


def test_elapsed_time_across_daylight_saving_transition() -> None:
    paris = ZoneInfo("Europe/Paris")
    observed_at = datetime(2026, 10, 25, 2, 15, tzinfo=paris, fold=0)
    now = datetime(2026, 10, 25, 2, 15, tzinfo=paris, fold=1)
    availability = Availability(None, 20, observed_at, now)

    assert not FreshnessPolicy(30).is_fresh(availability, now=now)
    assert FreshnessPolicy(60).is_fresh(availability, now=now)
