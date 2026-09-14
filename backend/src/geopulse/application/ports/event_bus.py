from typing import Protocol


class EventBus(Protocol):
    """Technology-neutral domain/application event publisher."""

    async def publish(self, event: object) -> None:
        """Publish an event without exposing a broker implementation."""
        ...
