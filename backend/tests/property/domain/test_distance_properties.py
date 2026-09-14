from hypothesis import given
from hypothesis import strategies as st

from geopulse.domain.algorithms.distance import calculer_distance
from geopulse.domain.models.location import Location

latitude_strategy = st.floats(
    min_value=-90,
    max_value=90,
    allow_nan=False,
    allow_infinity=False,
)

longitude_strategy = st.floats(
    min_value=-180,
    max_value=180,
    allow_nan=False,
    allow_infinity=False,
)


def location_strategy() -> st.SearchStrategy[Location]:
    return st.builds(
        Location,
        latitude=latitude_strategy,
        longitude=longitude_strategy,
        accuracy_meters=st.floats(
            min_value=0,
            max_value=10000,
            allow_nan=False,
            allow_infinity=False,
        ),
    )


@given(location=location_strategy())
def test_distance_to_same_location_is_zero(
    location: Location,
) -> None:
    metres, km = calculer_distance(
        location,
        location,
    )

    assert metres == 0
    assert km == 0


@given(
    a=location_strategy(),
    b=location_strategy(),
)
def test_distance_is_symmetric(
    a: Location,
    b: Location,
) -> None:
    distance_ab = calculer_distance(a, b)
    distance_ba = calculer_distance(b, a)

    assert distance_ab[0] == distance_ba[0]
    assert distance_ab[1] == distance_ba[1]


@given(
    a=location_strategy(),
    b=location_strategy(),
)
def test_distance_is_always_positive(
    a: Location,
    b: Location,
) -> None:
    metres, km = calculer_distance(a, b)

    assert metres >= 0
    assert km >= 0
