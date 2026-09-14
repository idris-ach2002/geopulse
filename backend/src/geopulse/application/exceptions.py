class ApplicationError(Exception):
    """Base exception for application layer errors."""


class InvalidRadiusError(ApplicationError):
    """Raised when a search radius is invalid."""
