"""
State management components for the Swallow Framework.

This package provides tools for creating and managing observable state
in applications, including value monitoring and change detection.
"""

from swallow_framework.state.observable import Observable, ObservableValue, ObservableList
from swallow_framework.state.property import StateProperty, state

__all__ = ["Observable", "ObservableValue", "ObservableList", "StateProperty", "state"]
