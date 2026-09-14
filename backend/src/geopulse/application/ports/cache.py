from typing import Protocol


class CachePort(Protocol):
    """Technology-neutral cache contract."""

    def get(self, key: str) -> object | None:
        """Read a cached value."""
        ...

    def set(
        self,
        key: str,
        value: object,
        *,
        ttl_seconds: int,
    ) -> None:
        """Store a value for a bounded amount of time."""
        ...
