"""
src/swallow_framework/exceptions.py
Custom exceptions for the Swallow Framework.
"""


class SwallowFrameworkError(Exception):
    """Base exception class for all Swallow Framework errors."""
    pass


class SwallowArgumentError(SwallowFrameworkError):
    """Exception raised when an operation is configured/performed with an invalid type."""
    pass


class SwallowConfigurationError(SwallowFrameworkError):
    """Exception raised when a configuration error occurs."""
    pass


class SwallowStateError(SwallowFrameworkError):
    """Exception raised when a configuration error occurs."""
    pass


class EventError(SwallowFrameworkError):
    """Base exception class for event-related errors."""
    pass


class EventNotFoundError(EventError):
    """Exception raised when an event is not found."""
    pass
