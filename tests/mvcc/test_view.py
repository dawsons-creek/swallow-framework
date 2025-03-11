import pytest
from unittest.mock import Mock, patch

from src.swallow_framework.core.events import Event, EventDispatcher
from src.swallow_framework.exceptions import SwallowArgumentError
from src.swallow_framework.mvcc.context import Context
from src.swallow_framework.mvcc.view import View


class MockContext(Context):
    def __init__(self):
        self.event_dispatcher = EventDispatcher()
        super().__init__(self.event_dispatcher)
        # Only mock the event_dispatcher.dispatch method, not the context.dispatch method
        self.event_dispatcher.dispatch = Mock()


class MockView(View):
    def __init__(self, context):
        super().__init__(context)


class TestView:
    @pytest.fixture
    def context(self):
        return MockContext()

    @pytest.fixture
    def view(self, context):
        return MockView(context)

    def test_init_success(self, context):
        view = MockView(context)
        assert view._context == context

    def test_init_invalid_context(self):
        with pytest.raises(SwallowArgumentError):
            MockView("not_a_context")

    def test_context_property(self, view, context):
        assert view.context == context

    def test_dispatch(self, view, context):
        event = Event("test_event", {"data": 123})
        view.dispatch(event)
        context.event_dispatcher.dispatch.assert_called_once_with(event)

    def test_dispatch_invalid_event(self, view):
        with pytest.raises(SwallowArgumentError):
            view.dispatch("not_an_event")

    def test_context_property_immutable(self, view):
        with pytest.raises(AttributeError):
            view.context = MockContext()
