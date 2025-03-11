"""
Event handling system for the Swallow Framework.
"""

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, Set

from src.swallow_framework.core.utils import validate_instance_type, validate_non_empty_string, validate_callback
from src.swallow_framework.exceptions import EventError, SwallowArgumentError

logger = logging.getLogger(__name__)


@dataclass
class Event:
    """
    Represents an event with a name and optional payload.

    :ivar name: The name of the event.
    :ivar data: Optional data associated with the event.
    """

    name: str
    data: Any = None

    def __post_init__(self):
        if not self.name or not isinstance(self.name, str):
            raise SwallowArgumentError("Event name must be a non-empty string")


class EventDispatcher:
    """
    Manages the registration and execution of event listeners.

    This class allows adding, removing, and dispatching events. It helps in implementing
    event-driven architectures by keeping track of listeners for specific event names and
    invoking the appropriate callback functions whenever an event is dispatched.
    """

    def __init__(self):
        self._listeners: Dict[str, Set[Callable[[Event], None]]] = defaultdict(set)

    def add_listener(self, event_name: str, callback: Callable[[Event], None]) -> None:
        """
        Registers a callback function to listen for a specific event.

        :param event_name: The name of the event to listen for.
        :param callback: The function to be called when the event is dispatched.
        :raises ValueError: If the event name is empty or not a string.
        :raises TypeError: If the callback is not callable.
        """
        validate_instance_type("event_name", event_name, str)
        validate_non_empty_string("event_name", event_name)
        validate_callback("event_name", callback)

        self._listeners[event_name].add(callback)

    def remove_listener(self, event_name: str, callback: Callable[[Event], None]) -> None:
        """
        Removes a callback function from the listener list of a specific event.

        :param event_name: The name of the event to remove the listener from.
        :param callback: The function to be removed.
        :raises ValueError: If the event name is empty or not a string.
        :raises TypeError: If the callback is not callable.
        """
        validate_instance_type("event_name", event_name, str)
        validate_non_empty_string("event_name", event_name)
        validate_callback("event_name", callback)

        if event_name in self._listeners:
            try:
                self._listeners[event_name].remove(callback)
            except KeyError:
                pass  # Callback not found, silently ignore

            if not self._listeners[event_name]:  # Remove event if no listeners remain
                del self._listeners[event_name]

    def dispatch(self, event: Event) -> None:
        """
        Dispatches an event, calling all registered listeners for the event name.

        :param event: An instance of Event.
        :raises TypeError: If the provided event is not an instance of Event.
        """
        validate_instance_type("event", event, Event)

        event_name = event.name

        if event_name not in self._listeners:
            logger.warning(f"Event '{event_name}' was dispatched but has no listeners")
            return  # Optionally raise an exception instead

        for callback in self._listeners[event_name]:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Error in event '{event_name}' listener: {e}", exc_info=True)
