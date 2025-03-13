import pytest
from swallow_framework.core.events import Event
from swallow_framework.core.utils import (
    validate_instance_type,
    validate_non_empty_string,
    validate_callback,
)
from swallow_framework.exceptions import SwallowArgumentError


class TestUtils:
    def test_validate_instance_type_success(self):
        validate_instance_type("param", 123, int)
        validate_instance_type("param", "abc", str)
        validate_instance_type("param", [], list)
        validate_instance_type("param", Event("test"), Event)

    def test_validate_instance_type_failure(self):
        with pytest.raises(SwallowArgumentError) as exc_info:
            validate_instance_type("param", 123, str)
        assert "param expects an instance of str, but got int" in str(
            exc_info.value
        )

        with pytest.raises(SwallowArgumentError) as exc_info:
            validate_instance_type("param", "abc", int)
        assert "param expects an instance of int, but got str" in str(
            exc_info.value
        )

        with pytest.raises(SwallowArgumentError) as exc_info:
            validate_instance_type("param", 123, Event)
        assert "param expects an instance of Event, but got int" in str(
            exc_info.value
        )

        with pytest.raises(SwallowArgumentError) as exc_info:
            validate_instance_type("param", "string", Event)
        assert "param expects an instance of Event, but got str" in str(
            exc_info.value
        )

    def test_validate_non_empty_string_success(self):
        validate_non_empty_string("param", "abc")
        validate_non_empty_string("param", "  abc  ")

    def test_validate_non_empty_string_failure(self):
        with pytest.raises(SwallowArgumentError) as exc_info:
            validate_non_empty_string("param", "")
        assert "param expects a non-empty string, but got an empty string" in str(
            exc_info.value
        )

        with pytest.raises(SwallowArgumentError) as exc_info:
            validate_non_empty_string("param", "   ")
        assert "param expects a non-empty string, but got an empty string" in str(
            exc_info.value
        )

        with pytest.raises(SwallowArgumentError) as exc_info:
            validate_non_empty_string("param", 123)
        assert "param expects a non-empty string, but got int" in str(exc_info.value)

    def test_validate_callback_success(self):
        def my_function():
            pass

        validate_callback("event_name", my_function)
        validate_callback("event_name", lambda: None)

    def test_validate_callback_failure(self):
        with pytest.raises(SwallowArgumentError) as exc_info:
            validate_callback("event_name", "not callable")
        assert "Callback for 'event_name' must be callable" in str(
            exc_info.value
        )

        with pytest.raises(SwallowArgumentError) as exc_info:
            validate_callback("event_name", 123)
        assert "Callback for 'event_name' must be callable" in str(
            exc_info.value
        )
