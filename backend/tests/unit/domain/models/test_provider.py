from uuid import uuid4

import pytest

from geopulse.domain.exceptions import InvalidProviderError
from geopulse.domain.models.provider import Provider


def test_provider_creation() -> None:
    provider = Provider(
        id=uuid4(),
        name="City Hall",
    )

    assert provider.name == "City Hall"


def test_provider_empty_name() -> None:
    with pytest.raises(InvalidProviderError):
        Provider(
            id=uuid4(),
            name=" ",
        )
