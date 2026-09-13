class DomainError(Exception):
    """Base exception for domain errors."""


class InvalidLocationError(DomainError):
    """Raised when geographic coordinates are invalid."""


class InvalidAvailabilityError(DomainError):
    """Raised when availability invariants are violated."""


class InvalidResourceError(DomainError):
    """Raised when resource invariants are violated."""


class InvalidProviderError(DomainError):
    """Raised when provider invariants are violated."""


class InvalidOpeningHoursError(DomainError):
    """Raised when opening hours are invalid."""
