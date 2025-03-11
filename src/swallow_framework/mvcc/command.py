"""
Command component for the Swallow Framework MVC pattern.

This module provides the base Command class for encapsulating actions
that can be performed on models.
"""

from abc import ABC, abstractmethod
from typing import Any

from src.swallow_framework.core.utils import validate_instance_type
from src.swallow_framework.mvcc.model import Model


class Command(ABC):
    """
    Represents an abstract base class for commands.

    This class serves as a blueprint for specific command implementations,
    enforcing the implementation of the `execute` method. Commands encapsulate
    actions that can be performed on the model.

    :ivar model: The model instance that this command operates on.
    :type model: Model
    """

    def __init__(self, model: Model):
        validate_instance_type('model', model, Model)
        self.model = model

    @abstractmethod
    def execute(self, data: Any) -> None:
        """
        Execute the command with the given data.

        Args:
            data: The data to use when executing the command.
        """
        pass