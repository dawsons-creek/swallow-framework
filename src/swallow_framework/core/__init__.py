"""
src/swallow_framework/core/__init__.py
Core components of the Swallow Framework.

This package contains the fundamental components of the framework,
including event handling and utility functions.
"""
from swallow_framework.core.events import Event, EventDispatcher
from swallow_framework.core.utils import validate_instance_type

__all__ = ["Event", "EventDispatcher", "validate_instance_type"]
