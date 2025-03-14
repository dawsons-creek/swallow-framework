"""
Swallow Framework - A lightweight Python framework.

This package provides tools for building applications with a streamlined
architecture, including state management, event handling, and MVC components.
"""

from swallow_framework.core.events import Event, EventDispatcher
from swallow_framework.core.utils import validate_instance_type
from swallow_framework.exceptions import (
    SwallowFrameworkError,
    SwallowArgumentError,
    SwallowConfigurationError,
    SwallowStateError,
    EventError,
    EventNotFoundError
)
from swallow_framework.mvcc import Model, View, Command, Context
from swallow_framework.state import Observable, ObservableValue, ObservableList, StateProperty, state

__version__ = "1.0.2"

__all__ = [
    # Core
    "Event",
    "EventDispatcher",
    "validate_instance_type",

    # Exceptions
    "SwallowFrameworkError",
    "SwallowArgumentError",
    "SwallowConfigurationError",
    "SwallowStateError",
    "EventError",
    "EventNotFoundError",

    # MVCC
    "Model",
    "View",
    "Command",
    "Context",

    # State
    "Observable",
    "ObservableValue",
    "ObservableList",
    "StateProperty",
    "state"
]