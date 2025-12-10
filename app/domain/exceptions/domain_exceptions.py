"""Domain-specific exceptions."""


class DomainException(Exception):
    """Base domain exception."""

    pass


class UserNotFoundError(DomainException):
    """User not found exception."""

    pass


class UserAlreadyExistsError(DomainException):
    """User already exists exception."""

    pass


class InvalidCredentialsError(DomainException):
    """Invalid credentials exception."""

    pass


class TaskNotFoundError(DomainException):
    """Task not found exception."""

    pass


class TaskAlreadyCompletedError(DomainException):
    """Task already completed exception."""

    pass


class TaskCannotBeCancelledError(DomainException):
    """Task cannot be cancelled exception."""

    pass


class InsufficientPermissionsError(DomainException):
    """Insufficient permissions exception."""

    pass

