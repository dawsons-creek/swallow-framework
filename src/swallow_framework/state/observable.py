"""
Observable components for reactive state management.

This module provides classes for creating observable values and collections that
can notify listeners when they change.
"""

from collections.abc import MutableSequence
from typing import List


class Observable:
    """
    This class represents an observable object, which monitors changes to its
    internal state and notifies registered callbacks whenever a change occurs.

    The purpose of this class is to assist in implementing observer patterns,
    making it easier to decouple components and enable reactions to state changes.
    The class allows registering multiple callbacks that will be executed whenever
    the observed state is updated.

    :ivar _value: Holds the current value being observed.
    :type _value: Any
    :ivar _notify_callback: Function to call when the value changes.
    :type _notify_callback: Callable[[Any], None]
    """

    def __init__(self, value, notify_callback=None):
        self._value = value
        self._notify_callback = notify_callback or (lambda val: None)

    def on_change(self, callback):
        """Register a callback to be notified when the value changes."""
        original_callback = self._notify_callback

        def combined_callback(value):
            if original_callback:
                original_callback(value)
            callback(value)

        self._notify_callback = combined_callback
        return callback

    def _notify(self):
        """Trigger notification with the current value."""
        self._notify_callback(self._value)


class ObservableValue(Observable):
    """
    Represents an observable value that can notify observers when its value changes.

    The `ObservableValue` class is used to encapsulate a value that can be observed
    for changes. Observers can be notified upon changes to the encapsulated value.
    This class behaves like the contained value in terms of equality comparison
    and provides a concise representation of the encapsulated value.

    :ivar _value: The encapsulated value being observed.
    :type _value: Any
    """

    def __init__(self, value, notify_callback=None):
        super().__init__(value, notify_callback)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value != new_value:
            self._value = new_value
            self._notify()

    # Allow the observable to act like its contained value
    def __eq__(self, other):
        if isinstance(other, ObservableValue):
            return self._value == other._value
        return self._value == other

    def __repr__(self):
        return f"ObservableValue({repr(self._value)})"


class ObservableList(MutableSequence, Observable):
    """
    A list-like container that supports observation for changes.

    ObservableList behaves similarly to a standard Python list but allows
    observation of changes in the list, enabling notifications to be sent when
    modifications are made. This can be useful in scenarios where the list's state
    needs to be monitored or reacted to dynamically.

    :ivar _value: The internal list holding the elements of the ObservableList.
    :type _value: List[Any]
    :ivar _notify_callback: Callback function to be triggered upon list modifications.
    :type _notify_callback: Callable[[List[Any]], None]
    :ivar _batch_updates: Flag indicating if batching of updates is active.
    :type _batch_updates: bool
    :ivar _pending_notification: Flag indicating a pending notification during a
        batch update.
    :type _pending_notification: bool
    """

    def __init__(self, data=None, notify_callback=None):
        Observable.__init__(self, data or [], notify_callback)
        self._batch_updates = False
        self._pending_notification = False

    def __getitem__(self, index):
        return self._value[index]

    def __setitem__(self, index, value):
        self._value[index] = value
        self._notify()

    def __delitem__(self, index):
        del self._value[index]
        self._notify()

    def insert(self, index, value):
        self._value.insert(index, value)
        self._notify()

    def append(self, value):
        self._value.append(value)
        self._notify()

    def remove(self, value):
        self._value.remove(value)
        self._notify()

    def extend(self, values):
        self._value.extend(values)
        self._notify()

    def clear(self):
        self._value.clear()
        self._notify()

    def pop(self, index=-1):
        value = self._value.pop(index)
        self._notify()
        return value

    def begin_batch_update(self):
        """Start batching updates to prevent multiple notifications."""
        self._batch_updates = True
        self._pending_notification = False

    def end_batch_update(self):
        """End batching updates and trigger a notification if needed."""
        self._batch_updates = False
        if self._pending_notification:
            self._notify_callback(self._value)
            self._pending_notification = False

    def _notify(self):
        """Internal method to handle notifications with batching support."""
        if self._batch_updates:
            self._pending_notification = True
        else:
            self._notify_callback(self._value)

    def __len__(self):
        return len(self._value)

    def __repr__(self):
        return f"ObservableList({self._value})"
