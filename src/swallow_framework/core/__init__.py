"""
Core components of the Swallow Framework.

This package contains the fundamental components of the framework,
including event handling and utility functions.
"""
from src.swallow_framework.core.events import Event, EventDispatcher
from src.swallow_framework.core.utils import validate_instance_type

__all__ = ["Event", "EventDispatcher", "validate_instance_type"]
