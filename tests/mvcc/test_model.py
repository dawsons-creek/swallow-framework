import unittest
from unittest.mock import Mock, patch, call

from src.swallow_framework.exceptions import SwallowStateError
from src.swallow_framework.mvcc.model import Model
from src.swallow_framework.state.property import state, StateProperty


class MockModel(Model):
    """Mock model implementation for unit tests."""

    # Define some state properties for testing
    string_prop = state("initial_string")
    int_prop = state(42)
    list_prop = state([1, 2, 3])

    # Define a regular attribute (not a state property)
    regular_attr = "not_a_state_property"


class ModelTests(unittest.TestCase):

    def setUp(self):
        self.model = MockModel()

    def test_init_initializes_state_properties(self):
        # Access the properties to verify they're initialized
        self.assertEqual(self.model.string_prop.value, "initial_string")
        self.assertEqual(self.model.int_prop.value, 42)
        self.assertEqual(list(self.model.list_prop), [1, 2, 3])

    def test_on_change_with_invalid_property(self):
        with self.assertRaises(SwallowStateError):
            self.model.on_change("non_existent_prop", lambda v: None)

    def test_on_change_with_non_state_property(self):
        with self.assertRaises(SwallowStateError):
            self.model.on_change("regular_attr", lambda v: None)

    def test_on_change_with_non_callable_callback(self):
        with self.assertRaises(SwallowStateError):
            self.model.on_change("string_prop", "not_a_callable")

    def test_on_change_direct_usage(self):
        callback = Mock()

        # Register the callback
        result = self.model.on_change("string_prop", callback)

        # Verify the callback was returned
        self.assertEqual(result, callback)

        # Change the property value
        self.model.string_prop.value = "new_value"

        # Verify the callback was called with the new value
        callback.assert_called_once_with("new_value")

    def test_on_change_decorator_usage(self):
        callback = Mock()

        # Use the decorator
        @self.model.on_change("int_prop")
        def on_int_prop_change(value):
            callback(value)

        # Change the property value
        self.model.int_prop.value = 100

        # Verify the callback was called with the new value
        callback.assert_called_once_with(100)

    def test_on_change_decorator_with_non_callable(self):
        with self.assertRaises(SwallowStateError):
            decorator = self.model.on_change("string_prop")
            decorator("not_a_callable")

    def test_multiple_callbacks_for_same_property(self):
        callback1 = Mock()
        callback2 = Mock()

        # Register both callbacks
        self.model.on_change("string_prop", callback1)
        self.model.on_change("string_prop", callback2)

        # Change the property value
        self.model.string_prop.value = "new_value"

        # Verify both callbacks were called with the new value
        callback1.assert_called_once_with("new_value")
        callback2.assert_called_once_with("new_value")

    def test_callback_for_list_property(self):
        callback = Mock()

        # Register the callback
        self.model.on_change("list_prop", callback)

        # Modify the list
        self.model.list_prop.append(4)

        # Verify the callback was called with the modified list
        callback.assert_called_once()
        self.assertEqual(list(callback.call_args[0][0]), [1, 2, 3, 4])

        # Reset the mock and modify the list again
        callback.reset_mock()
        self.model.list_prop.pop(0)

        # Verify the callback was called again
        callback.assert_called_once()
        self.assertEqual(list(callback.call_args[0][0]), [2, 3, 4])

    def test_callback_not_called_for_same_value(self):
        callback = Mock()

        # Register the callback
        self.model.on_change("string_prop", callback)

        # Set the same value
        current_value = self.model.string_prop.value
        self.model.string_prop.value = current_value

        # Verify the callback was not called
        callback.assert_not_called()

    def test_state_property_assignment(self):
        # Assign a new string value
        self.model.string_prop = "directly_assigned"
        self.assertEqual(self.model.string_prop.value, "directly_assigned")

        # Assign a new int value
        self.model.int_prop = 99
        self.assertEqual(self.model.int_prop.value, 99)

        # Assign a new list value
        self.model.list_prop = [4, 5, 6]
        self.assertEqual(list(self.model.list_prop), [4, 5, 6])

    def test_state_property_assignment_triggers_callbacks(self):
        callback = Mock()

        # Register the callback
        self.model.on_change("string_prop", callback)

        # Assign a new value
        self.model.string_prop = "new_value"

        # Verify the callback was called with the new value
        callback.assert_called_once_with("new_value")

    def test_init_state_properties_method(self):
        with patch.object(MockModel, '_init_state_properties') as mock_init:
            model = MockModel()
            mock_init.assert_called_once()

    def test_state_property_descriptor_access(self):
        # Access the descriptor directly
        descriptor = MockModel.string_prop

        # Verify it's a StateProperty instance
        self.assertIsInstance(descriptor, StateProperty)


if __name__ == '__main__':
    unittest.main()
