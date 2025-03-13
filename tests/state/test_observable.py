"""
Test cases for the enhanced ObservableValue class.

This module tests the operator overloading and convenience features
of the ObservableValue class.
"""

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from swallow_framework.state.observable import ObservableValue


class TestObservableValue(unittest.TestCase):
    """Test cases for the ObservableValue class."""

    def setUp(self):
        """Set up test fixtures."""
        self.notify_called = False
        self.notify_value = None

        def notify_callback(value):
            self.notify_called = True
            self.notify_value = value

        self.callback = notify_callback
        self.obs_int = ObservableValue(10, self.callback)
        self.obs_float = ObservableValue(3.14, self.callback)
        self.obs_str = ObservableValue("hello", self.callback)
        self.obs_list = ObservableValue([1, 2, 3], self.callback)

    def test_value_property(self):
        """Test the value property."""
        self.assertEqual(self.obs_int.value, 10)
        self.obs_int.value = 20
        self.assertEqual(self.obs_int.value, 20)
        self.assertTrue(self.notify_called)
        self.assertEqual(self.notify_value, 20)

    def test_get_method(self):
        """Test the get() method."""
        self.assertEqual(self.obs_int.get(), 10)

    def test_equality(self):
        """Test equality operator."""
        self.assertTrue(self.obs_int == 10)
        self.assertTrue(self.obs_int == ObservableValue(10))
        self.assertFalse(self.obs_int == 20)

    def test_inequality(self):
        """Test inequality operator."""
        self.assertTrue(self.obs_int != 20)
        self.assertTrue(self.obs_int != ObservableValue(20))
        self.assertFalse(self.obs_int != 10)

    def test_less_than(self):
        """Test less than operator."""
        self.assertTrue(self.obs_int < 20)
        self.assertTrue(self.obs_int < ObservableValue(20))
        self.assertFalse(self.obs_int < 5)

    def test_less_than_equal(self):
        """Test less than or equal operator."""
        self.assertTrue(self.obs_int <= 10)
        self.assertTrue(self.obs_int <= 20)
        self.assertTrue(self.obs_int <= ObservableValue(10))
        self.assertFalse(self.obs_int <= 5)

    def test_greater_than(self):
        """Test greater than operator."""
        self.assertTrue(self.obs_int > 5)
        self.assertTrue(self.obs_int > ObservableValue(5))
        self.assertFalse(self.obs_int > 20)

    def test_greater_than_equal(self):
        """Test greater than or equal operator."""
        self.assertTrue(self.obs_int >= 10)
        self.assertTrue(self.obs_int >= 5)
        self.assertTrue(self.obs_int >= ObservableValue(10))
        self.assertFalse(self.obs_int >= 20)

    def test_addition(self):
        """Test addition operator."""
        self.assertEqual(self.obs_int + 5, 15)
        self.assertEqual(self.obs_int + ObservableValue(5), 15)
        self.assertEqual(5 + self.obs_int, 15)  # Reflected operation

    def test_subtraction(self):
        """Test subtraction operator."""
        self.assertEqual(self.obs_int - 5, 5)
        self.assertEqual(self.obs_int - ObservableValue(5), 5)
        self.assertEqual(15 - self.obs_int, 5)  # Reflected operation

    def test_multiplication(self):
        """Test multiplication operator."""
        self.assertEqual(self.obs_int * 2, 20)
        self.assertEqual(self.obs_int * ObservableValue(2), 20)
        self.assertEqual(2 * self.obs_int, 20)  # Reflected operation

    def test_division(self):
        """Test division operator."""
        self.assertEqual(self.obs_int / 2, 5)
        self.assertEqual(self.obs_int / ObservableValue(2), 5)
        self.assertEqual(100 / self.obs_int, 10)  # Reflected operation

    def test_floor_division(self):
        """Test floor division operator."""
        self.assertEqual(self.obs_int // 3, 3)
        self.assertEqual(self.obs_int // ObservableValue(3), 3)
        self.assertEqual(100 // self.obs_int, 10)  # Reflected operation

    def test_modulo(self):
        """Test modulo operator."""
        self.assertEqual(self.obs_int % 3, 1)
        self.assertEqual(self.obs_int % ObservableValue(3), 1)
        self.assertEqual(103 % self.obs_int, 3)  # Reflected operation

    def test_iadd(self):
        """Test in-place addition."""
        self.notify_called = False
        self.obs_int += 5
        self.assertEqual(self.obs_int.value, 15)
        self.assertTrue(self.notify_called)

        self.notify_called = False
        self.obs_int += ObservableValue(5)
        self.assertEqual(self.obs_int.value, 20)
        self.assertTrue(self.notify_called)

    def test_isub(self):
        """Test in-place subtraction."""
        self.notify_called = False
        self.obs_int -= 5
        self.assertEqual(self.obs_int.value, 5)
        self.assertTrue(self.notify_called)

        self.notify_called = False
        self.obs_int -= ObservableValue(2)
        self.assertEqual(self.obs_int.value, 3)
        self.assertTrue(self.notify_called)

    def test_imul(self):
        """Test in-place multiplication."""
        self.notify_called = False
        self.obs_int *= 2
        self.assertEqual(self.obs_int.value, 20)
        self.assertTrue(self.notify_called)

        self.notify_called = False
        self.obs_int *= ObservableValue(2)
        self.assertEqual(self.obs_int.value, 40)
        self.assertTrue(self.notify_called)

    def test_idiv(self):
        """Test in-place division."""
        self.notify_called = False
        self.obs_int /= 2
        self.assertEqual(self.obs_int.value, 5)
        self.assertTrue(self.notify_called)

        self.notify_called = False
        self.obs_int /= ObservableValue(5)
        self.assertEqual(self.obs_int.value, 1)
        self.assertTrue(self.notify_called)

    def test_ifloordiv(self):
        """Test in-place floor division."""
        self.obs_int.value = 10
        self.notify_called = False
        self.obs_int //= 3
        self.assertEqual(self.obs_int.value, 3)
        self.assertTrue(self.notify_called)

        self.notify_called = False
        self.obs_int //= ObservableValue(3)
        self.assertEqual(self.obs_int.value, 1)
        self.assertTrue(self.notify_called)

    def test_imod(self):
        """Test in-place modulo."""
        self.obs_int.value = 10
        self.notify_called = False
        self.obs_int %= 3
        self.assertEqual(self.obs_int.value, 1)
        self.assertTrue(self.notify_called)

        self.notify_called = False
        self.obs_int %= ObservableValue(1)
        self.assertEqual(self.obs_int.value, 0)
        self.assertTrue(self.notify_called)

    def test_conversions(self):
        """Test conversion methods."""
        self.assertEqual(int(self.obs_int), 10)
        self.assertEqual(float(self.obs_int), 10.0)
        self.assertEqual(str(self.obs_int), "10")
        self.assertTrue(bool(self.obs_int))

        # Test with zero
        zero_obs = ObservableValue(0)
        self.assertFalse(bool(zero_obs))

    def test_container_methods(self):
        """Test container methods."""
        self.assertEqual(len(self.obs_list), 3)
        self.assertEqual(self.obs_list[0], 1)
        self.assertTrue(2 in self.obs_list)
        self.assertFalse(5 in self.obs_list)

    def test_notification(self):
        """Test notification callbacks."""
        self.notify_called = False

        # Should not notify if value doesn't change
        self.obs_int.value = 10
        self.assertFalse(self.notify_called)

        # Should notify when value changes
        self.obs_int.value = 20
        self.assertTrue(self.notify_called)
        self.assertEqual(self.notify_value, 20)

        # Reset notification flag
        self.notify_called = False

        # Should notify with in-place operators
        self.obs_int += 5
        self.assertTrue(self.notify_called)
        self.assertEqual(self.notify_value, 25)

    def test_string_concatenation(self):
        """Test string concatenation."""
        self.assertEqual(self.obs_str + " world", "hello world")
        self.assertEqual("world " + self.obs_str, "world hello")  # Reflected

        self.notify_called = False
        self.obs_str += " world"
        self.assertEqual(self.obs_str.value, "hello world")
        self.assertTrue(self.notify_called)


if __name__ == "__main__":
    unittest.main()