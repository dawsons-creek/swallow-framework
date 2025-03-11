"""
Swallow Framework
~~~~~~~~~~~~~~~~

A lightweight Python framework designed for reactive state management and event-driven architecture.
"""

__version__ = "0.1.0"

from src.swallow_framework.core import Event, EventDispatcher, validate_instance_type
from src.swallow_framework.mvcc import Model, View, Command, Context
from src.swallow_framework.state import Observable, ObservableValue, ObservableList

__all__ = [
    # Core
    "Event",
    "EventDispatcher",

    # State
    "Observable",
    "ObservableValue",
    "ObservableList",
    "state",

    # MVC
    "Model",
    "View",
    "Command",
    "Context",

    # Utils
    "validate_instance_type"
]
