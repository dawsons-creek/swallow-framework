"""
src/swallow_framework/core/utils.py
Utility functions for the Swallow Framework.
"""
from swallow_framework.exceptions import SwallowArgumentError


def validate_instance_type(param_name: str, value, expected_type: type) -> None:
    """Ensures that the given value is an instance of the expected type.

    Args:
        param_name (str): The name of the parameter being checked.
        value: The actual value being passed.
        expected_type (type): The expected type for the parameter.

    Raises:
        TypeError: If the value is not an instance of the expected type.
    """
    if not isinstance(value, expected_type):
        raise SwallowArgumentError(
            f"{param_name} expects an instance of {expected_type.__name__}, "
            f"but got {type(value).__name__}"
        )


def validate_non_empty_string(param_name: str, value: str) -> None:
    """Ensures that the given value is a non-empty string.

    Args:
        param_name (str): The name of the parameter being checked.
        value (str): The actual value being passed.

    Raises:
        SwallowTypeError: If the value is not a string or is an empty string.
    """
    if not isinstance(value, str):
        raise SwallowArgumentError(
            f"{param_name} expects a non-empty string, but got {type(value).__name__}"
        )
    if not value.strip():
        raise SwallowArgumentError(f"{param_name} expects a non-empty string, but got an empty string")


def validate_callback(event_name: str, callback: callable) -> None:
    if not callable(callback):
        raise SwallowArgumentError(f"Callback for '{event_name}' must be callable")