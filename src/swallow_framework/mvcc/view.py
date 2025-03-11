"""
View component for the Swallow Framework MVC pattern.

This module provides the base View class for handling user interactions
and dispatching events in applications.
"""

from abc import ABC

from src.swallow_framework.core.events import Event
from src.swallow_framework.core.utils import validate_instance_type
from src.swallow_framework.mvcc.context import Context


class View(ABC):
    """
    Represents the base implementation for a view in the application.

    This abstract base class defines a structure for views that operate
    with a given context and handle events via a dispatching mechanism.
    It ensures that derived classes have a consistent interface for
    managing the application-level context and event handling.

    :ivar context: The shared application context used by the view for
        managing state and interacting with other components.
    :type context: Context
    """

    def __init__(self, context: Context):
        validate_instance_type('context', context, Context)
        self._context = context

    @property
    def context(self) -> Context:
        """Get the context associated with this view."""
        return self._context

    def dispatch(self, event: Event) -> None:
        """
        Dispatch an event through the context.

        Args:
            event: The event to dispatch.
        """
        self.context.dispatch(event)
