"""
Context component for the Swallow Framework MVC pattern.

This module provides the base Context class for mapping commands to events
and managing event dispatching in applications.
"""

from abc import ABC

from swallow_framework.core.events import EventDispatcher, Event
from swallow_framework.core.utils import validate_instance_type
from swallow_framework.mvcc.command import Command


class Context(ABC):
    """
    The Context class serves as an abstract base class that provides methods to
    map commands to specific events and facilitate event dispatching within an
    application.

    This class is designed to integrate an event dispatching mechanism with a
    command execution pattern, ensuring commands are executed automatically
    when specific events are dispatched. It requires an EventDispatcher instance
    to handle the dispatching and mapping processes.

    :ivar event_dispatcher: The event dispatcher instance used to add, remove, or
                            invoke listeners for specific events.
    :type event_dispatcher: EventDispatcher
    """

    def __init__(self, event_dispatcher: EventDispatcher):
        validate_instance_type('event_dispatcher', event_dispatcher, EventDispatcher)
        self.event_dispatcher = event_dispatcher

    def map_command(self, event_name: str, command: Command) -> None:
        """
        Map a command to an event name.

        Args:
            event_name: The name of the event to map the command to.
            command: The command to execute when the event is dispatched.
        """
        validate_instance_type('command', command, Command)
        self.event_dispatcher.add_listener(event_name, lambda event: command.execute(event.data))

    def dispatch(self, event: Event) -> None:
        """
        Dispatch an event through the event dispatcher.

        Args:
            event: The event to dispatch.
        """
        validate_instance_type('event', event, Event)
        self.event_dispatcher.dispatch(event)
