from datetime import UTC, datetime
from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from geopulse.domain.exceptions import InvalidResourceError
from geopulse.domain.models.availability import Availability
from geopulse.domain.models.location import Location
from geopulse.domain.models.provider import Provider
from geopulse.domain.models.resource import Resource
from geopulse.domain.models.resource_category import ResourceCategory


@given(
    name=st.text(
        min_size=1,
        max_size=50,
    )
)
def test_resource_name_with_content_is_accepted(
    name: str,
) -> None:
    if not name.strip():
        return

    resource = Resource(
        id=uuid4(),
        name=name,
        category=ResourceCategory.OTHER,
        location=Location(0, 0, 1),
        provider=Provider(uuid4(), "Provider"),
        availability=Availability(
            capacity=10,
            available=5,
            observed_at=datetime.now(UTC),
            received_at=datetime.now(UTC),
        ),
        created_at=datetime.now(UTC),
    )

    assert resource.name == name


@given(
    name=st.just(""),
)
def test_empty_resource_name_is_rejected(
    name: str,
) -> None:
    with pytest.raises(InvalidResourceError):
        Resource(
            id=uuid4(),
            name=name,
            category=ResourceCategory.OTHER,
            location=Location(0, 0, 1),
            provider=Provider(uuid4(), "Provider"),
            availability=Availability(
                capacity=10,
                available=5,
                observed_at=datetime.now(UTC),
                received_at=datetime.now(UTC),
            ),
            created_at=datetime.now(UTC),
        )
