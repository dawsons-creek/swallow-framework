"""
Model component for the Swallow Framework MVC pattern.

This module provides the base Model class for managing state properties
and change notifications in applications.
"""
from swallow_framework.exceptions import SwallowStateError
from swallow_framework.state.property import StateProperty


class Model:
    """
    Represents a model that manages state properties and allows registration
    of callbacks for changes in these properties. This includes dynamically
    initializing all state properties defined as `StateProperty` descriptors
    and providing mechanisms to observe property changes reactively.

    The model facilitates interaction with stateful properties by allowing users
    to listen for changes using the `on_change` method, which can be used
    both directly or as a decorator.

    :ivar _state_properties_initialized: Indicates whether state properties
        are initialized properly.
    :type _state_properties_initialized: bool
    """

    def __init__(self):
        # Initialize all state properties
        self._init_state_properties()

    def _init_state_properties(self):
        """Initialize all state properties to ensure descriptors are set up."""
        # Find all state descriptors
        for name, attr in type(self).__dict__.items():
            if isinstance(attr, StateProperty):
                # Initialize property by accessing it (triggers __get__)
                getattr(self, name)

    def on_change(self, prop_name, callback=None):
        """
        Register a callback to be called when a property changes.
        Can be used both directly or as a decorator.

        Examples:
            # Direct usage
            model.watch('property_name', callback_function)

            # As a decorator
            @model.watch('property_name')
            def on_property_changed(value):
                # Handle property change
        """
        # Find the state descriptor
        descriptor = type(self).__dict__.get(prop_name)
        if not descriptor or not isinstance(descriptor, StateProperty):
            raise SwallowStateError(f"Property '{prop_name}' is not a @state property")

        # If callback is provided, register it directly and return it
        if callback is not None:
            if not callable(callback):
                raise SwallowStateError(f"Callback for property '{prop_name}' must be callable")
            descriptor.on_change(self, callback)
            return callback

        # If no callback is provided, return a decorator that will register the callback
        def decorator(func):
            if not callable(func):
                raise SwallowStateError(f"Decorator for property '{prop_name}' must be applied to a callable")
            descriptor.on_change(self, func)
            return func

        return decorator
