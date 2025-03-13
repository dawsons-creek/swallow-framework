import pytest
from swallow_framework.core.events import Event, EventDispatcher
from swallow_framework.exceptions import SwallowArgumentError


class TestEvent:
    def test_event_creation_success(self):
        event = Event("test_event")
        assert event.name == "test_event"
        assert event.data is None

        event = Event("test_event", {"data": 123})
        assert event.data == {"data": 123}

    def test_event_creation_invalid_name(self):
        with pytest.raises(SwallowArgumentError):
            Event("")

        with pytest.raises(SwallowArgumentError):
            Event(None)

        with pytest.raises(SwallowArgumentError):
            Event(123)


class TestEventDispatcher:
    @pytest.fixture
    def dispatcher(self):
        return EventDispatcher()

    def test_add_listener_success(self, dispatcher):
        def callback(event):
            pass

        dispatcher.add_listener("test_event", callback)
        assert "test_event" in dispatcher._listeners
        assert callback in dispatcher._listeners["test_event"]

    def test_add_listener_invalid_event_name(self, dispatcher):
        def callback(event):
            pass

        with pytest.raises(SwallowArgumentError):
            dispatcher.add_listener("", callback)

        with pytest.raises(SwallowArgumentError):
            dispatcher.add_listener(None, callback)

        with pytest.raises(SwallowArgumentError):
            dispatcher.add_listener(123, callback)

    def test_add_listener_invalid_callback(self, dispatcher):
        with pytest.raises(SwallowArgumentError):
            dispatcher.add_listener("test_event", "not callable")

    def test_remove_listener_success(self, dispatcher):
        def callback(event):
            pass

        dispatcher.add_listener("test_event", callback)
        dispatcher.remove_listener("test_event", callback)
        assert "test_event" not in dispatcher._listeners

    def test_remove_listener_nonexistent_event(self, dispatcher):
        def callback(event):
            pass

        dispatcher.remove_listener("test_event", callback)

    def test_remove_listener_nonexistent_callback(self, dispatcher):
        def callback1(event):
            pass

        def callback2(event):
            pass

        dispatcher.add_listener("test_event", callback1)
        dispatcher.remove_listener("test_event", callback2)
        assert callback1 in dispatcher._listeners["test_event"]

    def test_remove_listener_invalid_event_name(self, dispatcher):
        def callback(event):
            pass

        with pytest.raises(SwallowArgumentError):
            dispatcher.remove_listener("", callback)

        with pytest.raises(SwallowArgumentError):
            dispatcher.remove_listener(None, callback)

        with pytest.raises(SwallowArgumentError):
            dispatcher.remove_listener(123, callback)

    def test_remove_listener_invalid_callback(self, dispatcher):
        with pytest.raises(SwallowArgumentError):
            dispatcher.remove_listener("test_event", "not callable")

    def test_dispatch_success(self, dispatcher, caplog):
        def callback(event):
            callback.called = True
            callback.event = event

        callback.called = False
        dispatcher.add_listener("test_event", callback)
        event = Event("test_event", {"data": 123})
        dispatcher.dispatch(event)
        assert callback.called
        assert callback.event == event

    def test_dispatch_no_listeners(self, dispatcher, caplog):
        event = Event("test_event")
        dispatcher.dispatch(event)
        assert "Event 'test_event' was dispatched but has no listeners" in caplog.text

    def test_dispatch_invalid_event(self, dispatcher):
        with pytest.raises(SwallowArgumentError):
            dispatcher.dispatch("not an event")

    def test_dispatch_callback_exception(self, dispatcher, caplog):
        def callback(event):
            raise ValueError("Callback failed")

        dispatcher.add_listener("test_event", callback)
        event = Event("test_event")
        dispatcher.dispatch(event)
        assert "Error in event 'test_event' listener: Callback failed" in caplog.text
