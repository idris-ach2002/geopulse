class ApplicationError(Exception):
    """Base exception for application layer errors."""


class InvalidRadiusError(ApplicationError):
    """Raised when a search radius is invalid."""


class ResourceCreationError(ApplicationError):
    """Raised when a resource cannot be created."""
