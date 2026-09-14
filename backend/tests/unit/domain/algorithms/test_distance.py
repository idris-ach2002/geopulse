import pytest

from geopulse.domain.algorithms.distance import calculer_distance
from geopulse.domain.models.location import Location


def test_same_location_returns_zero_distance() -> None:
    location = Location(
        latitude=45.1885,
        longitude=5.7245,
        accuracy_meters=10,
    )

    metres, km = calculer_distance(
        location,
        location,
    )

    assert metres == pytest.approx(0)
    assert km == pytest.approx(0)


def test_distance_is_symmetrical() -> None:
    lyon = Location(
        latitude=45.764,
        longitude=4.8357,
        accuracy_meters=10,
    )

    paris = Location(
        latitude=48.8566,
        longitude=2.3522,
        accuracy_meters=10,
    )

    distance_ab = calculer_distance(
        lyon,
        paris,
    )

    distance_ba = calculer_distance(
        paris,
        lyon,
    )

    assert distance_ab[0] == pytest.approx(distance_ba[0])

    assert distance_ab[1] == pytest.approx(distance_ba[1])


def test_lyon_paris_distance_is_reasonable() -> None:
    lyon = Location(
        latitude=45.764,
        longitude=4.8357,
        accuracy_meters=10,
    )

    paris = Location(
        latitude=48.8566,
        longitude=2.3522,
        accuracy_meters=10,
    )

    metres, km = calculer_distance(
        lyon,
        paris,
    )

    # Distance réelle environ 392 km
    assert km == pytest.approx(
        392,
        rel=0.03,
    )


def test_equator_one_degree_longitude() -> None:
    point_a = Location(
        latitude=0,
        longitude=0,
        accuracy_meters=1,
    )

    point_b = Location(
        latitude=0,
        longitude=1,
        accuracy_meters=1,
    )

    metres, km = calculer_distance(
        point_a,
        point_b,
    )

    # 1 degré longitude à l'équateur ≈ 111.2 km
    assert km == pytest.approx(
        111.2,
        rel=0.01,
    )
