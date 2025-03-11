from unittest.mock import Mock

from src.swallow_framework.state.observable import Observable, ObservableValue, ObservableList


class TestObservable:
    def test_init(self):
        value = "test_value"
        observable = Observable(value)
        assert observable._value == value

    def test_init_with_callback(self):
        callback = Mock()
        observable = Observable("test", callback)
        assert observable._notify_callback == callback

    def test_on_change(self):
        observable = Observable("test")
        callback = Mock()

        # Register callback
        result = observable.on_change(callback)

        # Verify callback is returned
        assert result == callback

        # Trigger notification
        observable._notify()

        # Verify callback was called with the value
        callback.assert_called_once_with("test")

    def test_multiple_callbacks(self):
        observable = Observable("test")
        callback1 = Mock()
        callback2 = Mock()

        # Register callbacks
        observable.on_change(callback1)
        observable.on_change(callback2)

        # Trigger notification
        observable._notify()

        # Verify both callbacks were called
        callback1.assert_called_once_with("test")
        callback2.assert_called_once_with("test")


class TestObservableValue:
    def test_init(self):
        value = "test_value"
        observable = ObservableValue(value)
        assert observable.value == value

    def test_value_getter(self):
        observable = ObservableValue("test")
        assert observable.value == "test"

    def test_value_setter(self):
        callback = Mock()
        observable = ObservableValue("test", callback)

        # Change value
        observable.value = "new_value"

        # Verify callback was called
        callback.assert_called_once_with("new_value")

        # Verify value was updated
        assert observable.value == "new_value"

    def test_value_setter_same_value(self):
        callback = Mock()
        observable = ObservableValue("test", callback)

        # Set same value
        observable.value = "test"

        # Verify callback was not called
        callback.assert_not_called()

    def test_equality(self):
        observable1 = ObservableValue("test")
        observable2 = ObservableValue("test")
        observable3 = ObservableValue("different")

        # Compare with other ObservableValue
        assert observable1 == observable2
        assert observable1 != observable3

        # Compare with raw value
        assert observable1 == "test"
        assert observable1 != "different"

    def test_repr(self):
        observable = ObservableValue("test")
        assert repr(observable) == "ObservableValue('test')"


class TestObservableList:
    def test_init_empty(self):
        observable = ObservableList()
        assert len(observable) == 0

    def test_init_with_data(self):
        data = [1, 2, 3]
        observable = ObservableList(data)
        assert list(observable) == data

    def test_getitem(self):
        observable = ObservableList([1, 2, 3])
        assert observable[0] == 1
        assert observable[1] == 2
        assert observable[2] == 3

    def test_setitem(self):
        callback = Mock()
        observable = ObservableList([1, 2, 3], callback)

        observable[1] = 5

        assert observable[1] == 5
        callback.assert_called_once_with([1, 5, 3])

    def test_delitem(self):
        callback = Mock()
        observable = ObservableList([1, 2, 3], callback)

        del observable[1]

        assert list(observable) == [1, 3]
        callback.assert_called_once_with([1, 3])

    def test_insert(self):
        callback = Mock()
        observable = ObservableList([1, 2, 3], callback)

        observable.insert(1, 5)

        assert list(observable) == [1, 5, 2, 3]
        callback.assert_called_once_with([1, 5, 2, 3])

    def test_append(self):
        callback = Mock()
        observable = ObservableList([1, 2, 3], callback)

        observable.append(4)

        assert list(observable) == [1, 2, 3, 4]
        callback.assert_called_once_with([1, 2, 3, 4])

    def test_remove(self):
        callback = Mock()
        observable = ObservableList([1, 2, 3], callback)

        observable.remove(2)

        assert list(observable) == [1, 3]
        callback.assert_called_once_with([1, 3])

    def test_extend(self):
        callback = Mock()
        observable = ObservableList([1, 2, 3], callback)

        observable.extend([4, 5])

        assert list(observable) == [1, 2, 3, 4, 5]
        callback.assert_called_once_with([1, 2, 3, 4, 5])

    def test_clear(self):
        callback = Mock()
        observable = ObservableList([1, 2, 3], callback)

        observable.clear()

        assert list(observable) == []
        callback.assert_called_once_with([])

    def test_pop(self):
        callback = Mock()
        observable = ObservableList([1, 2, 3], callback)

        value = observable.pop()

        assert value == 3
        assert list(observable) == [1, 2]
        callback.assert_called_once_with([1, 2])

    def test_pop_with_index(self):
        callback = Mock()
        observable = ObservableList([1, 2, 3], callback)

        value = observable.pop(1)

        assert value == 2
        assert list(observable) == [1, 3]
        callback.assert_called_once_with([1, 3])

    def test_batch_update(self):
        callback = Mock()
        observable = ObservableList([1, 2, 3], callback)

        observable.begin_batch_update()
        observable.append(4)
        observable.append(5)
        observable.remove(2)
        callback.assert_not_called()

        observable.end_batch_update()
        callback.assert_called_once_with([1, 3, 4, 5])

    def test_batch_update_no_changes(self):
        callback = Mock()
        observable = ObservableList([1, 2, 3], callback)

        observable.begin_batch_update()
        observable.end_batch_update()

        callback.assert_not_called()

    def test_len(self):
        observable = ObservableList([1, 2, 3])
        assert len(observable) == 3

    def test_repr(self):
        observable = ObservableList([1, 2, 3])
        assert repr(observable) == "ObservableList([1, 2, 3])"
