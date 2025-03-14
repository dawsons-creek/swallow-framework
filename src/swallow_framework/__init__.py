"""
Swallow Framework
~~~~~~~~~~~~~~~~

A lightweight Python framework designed for reactive state management and event-driven architecture.
"""

__version__ = "1.0.1"

from swallow_framework.core.events import Event, EventDispatcher
from swallow_framework.mvcc.model import Model
from swallow_framework.mvcc.view import View
from swallow_framework.mvcc.command import Command
from swallow_framework.mvcc.context import Context
from swallow_framework.state.property import state

__all__ = ['Event', 'EventDispatcher', 'Model', 'View', 'Command', 'Context', 'state']
