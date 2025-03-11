from unittest.mock import Mock

import pytest

from src.swallow_framework.state.observable import ObservableValue, ObservableList
from src.swallow_framework.exceptions import SwallowStateError
from src.swallow_framework.state import state, StateProperty


class TestStateProperty:
    class TestModel:
        string_prop = state("initial")
        int_prop = state(42)
        list_prop = state([1, 2, 3])

        def __init__(self):
            # Initialize state properties
            self.string_prop
            self.int_prop
            self.list_prop

    def test_init(self):
        prop = StateProperty("test_value")
        assert prop.initial == "test_value"
        assert prop.data == {}

    def test_get_class_access(self):
        # Access via class should return the descriptor
        assert isinstance(self.TestModel.string_prop, StateProperty)

    def test_get_instance_access(self):
        model = self.TestModel()

        # Access via instance should return the observable
        assert isinstance(model.string_prop, ObservableValue)
        assert model.string_prop.value == "initial"

        assert isinstance(model.int_prop, ObservableValue)
        assert model.int_prop.value == 42

        assert isinstance(model.list_prop, ObservableList)
        assert list(model.list_prop) == [1, 2, 3]

    def test_set_value_property(self):
        model = self.TestModel()

        # Set new value
        model.string_prop = "new_value"
        assert model.string_prop.value == "new_value"

        model.int_prop = 100
        assert model.int_prop.value == 100

    def test_set_list_property(self):
        model = self.TestModel()

        # Set new list
        model.list_prop = [4, 5, 6]
        assert list(model.list_prop) == [4, 5, 6]

        # Set to None should clear the list
        model.list_prop = None
        assert list(model.list_prop) == []

    def test_on_change(self):
        model = self.TestModel()
        callback = Mock()

        # Register callback
        result = model.string_prop.on_change(callback)

        # Verify callback is returned
        assert result == callback

        # Change value
        model.string_prop.value = "changed"

        # Verify callback was called
        callback.assert_called_once_with("changed")

    def test_state_property_on_change(self):
        model = self.TestModel()
        callback = Mock()

        # Register callback using StateProperty method
        self.TestModel.string_prop.on_change(model, callback)

        # Change value
        model.string_prop.value = "changed"

        # Verify callback was called
        callback.assert_called_once_with("changed")

    def test_state_property_on_change_none_callback(self):
        model = self.TestModel()

        # Try to register None callback
        with pytest.raises(SwallowStateError) as exc_info:
            self.TestModel.string_prop.on_change(model, None)

        assert "Parameter 'callback' must be provided and cannot be None" in str(
            exc_info.value
        )

    def test_state_decorator(self):
        # Test that state function returns a StateProperty
        prop = state("test")
        assert isinstance(prop, StateProperty)
        assert prop.initial == "test"

    def test_list_property_append_triggers_callback(self):
        model = self.TestModel()
        callback = Mock()
        model.list_prop.on_change(callback)

        model.list_prop.append(4)
        callback.assert_called_once_with([1, 2, 3, 4])

    def test_list_property_remove_triggers_callback(self):
        model = self.TestModel()
        callback = Mock()
        model.list_prop.on_change(callback)

        model.list_prop.remove(2)
        callback.assert_called_once_with([1, 3])

    def test_list_property_insert_triggers_callback(self):
        model = self.TestModel()
        callback = Mock()
        model.list_prop.on_change(callback)

        model.list_prop.insert(1, 4)
        callback.assert_called_once_with([1, 4, 2, 3])
