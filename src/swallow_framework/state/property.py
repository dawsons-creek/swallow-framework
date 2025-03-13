"""
Property descriptors for reactive state management.

This module provides descriptor classes that enable reactive properties
in model classes, allowing automatic tracking and notification of state changes.
"""
from swallow_framework.exceptions import SwallowStateError
from swallow_framework.state.observable import ObservableList, ObservableValue


class StateProperty:
    """
    Descriptor class that provides an observable state property for a class. This
    class allows you to define instance-specific state properties which can be
    either single values or lists. The values are wrapped in observable wrappers
    to monitor changes and invoke callbacks for state modifications. Primarily
    used to simplify state management in objects.

    :ivar initial: The initial value set for the property. Can be a single value or
        a list. This defines the default state of the property.
    :ivar data: A dictionary that stores per-instance data. Each instance of the
        class owning the StateProperty will have its own entry in this dictionary,
        containing the wrapped, observable property.
    :type data: dict
    """

    def __init__(self, initial):
        self.initial = initial
        self.data = {}  # Stores values per instance

    def __get__(self, instance, owner):
        if instance is None:
            return self  # Allow access via class

        # Create the observable wrapper if it doesn't exist
        if instance not in self.data:
            if isinstance(self.initial, list):
                self.data[instance] = ObservableList(
                    self.initial[:],
                    lambda v: self._notify(instance, v)
                )
            else:
                self.data[instance] = ObservableValue(
                    self.initial,
                    lambda v: self._notify(instance, v)
                )

        return self.data[instance]

    def __set__(self, instance, value):
        observable = self.__get__(instance, type(instance))

        if isinstance(observable, ObservableList):
            # For lists, replace the content but keep the observable
            observable.clear()
            if value is not None:
                observable.extend(value)
        else:
            # For single values, update the value
            observable.value = value

    def _notify(self, instance, value):
        """This is only used internally for backward compatibility."""
        # The notification is now primarily handled by Observable classes
        pass

    def on_change(self, instance, callback=None):
        """Register a callback for changes in the state property."""
        if callback is None:
            raise SwallowStateError("Parameter 'callback' must be provided and cannot be None")
        observable = self.__get__(instance, type(instance))
        return observable.on_change(callback)


def state(initial_value=None):
    """Decorator to create a reactive property with `.on_change(callback)` support."""
    return StateProperty(initial_value)
