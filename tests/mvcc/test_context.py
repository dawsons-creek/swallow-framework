import unittest
from unittest.mock import patch

from swallow_framework.core.events import Event, EventDispatcher
from swallow_framework.exceptions import SwallowArgumentError
from swallow_framework.mvcc.command import Command
from swallow_framework.mvcc.context import Context
from swallow_framework.mvcc.model import Model


class MockCommand(Command):
    def __init__(self, model):
        super().__init__(model)
        self.execute_called = False
        self.last_data = None

    def execute(self, data):
        self.execute_called = True
        self.last_data = data


class MockModel(Model):
    pass


class MockContext(Context):
    pass


class ContextTests(unittest.TestCase):

    def setUp(self):
        self.event_dispatcher = EventDispatcher()
        self.context = MockContext(self.event_dispatcher)
        self.model = MockModel()
        self.command = MockCommand(self.model)

    def test_init_with_invalid_dispatcher_type(self):
        with self.assertRaises(SwallowArgumentError):
            MockContext("not_a_dispatcher")

    def test_map_command_with_invalid_command_type(self):
        with self.assertRaises(SwallowArgumentError):
            self.context.map_command("test_event", "not_a_command")

    def test_dispatch_with_invalid_event_type(self):
        with self.assertRaises(SwallowArgumentError):
            self.context.dispatch("not_an_event")

    def test_map_command_adds_listener(self):
        with patch.object(self.event_dispatcher, 'add_listener') as mock_add_listener:
            self.context.map_command("test_event", self.command)
            mock_add_listener.assert_called_once()
            # First argument should be the event name
            self.assertEqual(mock_add_listener.call_args[0][0], "test_event")
            # Second argument should be a callable (the wrapper function)
            self.assertTrue(callable(mock_add_listener.call_args[0][1]))

    def test_dispatch_calls_event_dispatcher(self):
        event = Event("test_event", "test_data")
        with patch.object(self.event_dispatcher, 'dispatch') as mock_dispatch:
            self.context.dispatch(event)
            mock_dispatch.assert_called_once_with(event)

    def test_command_executes_when_event_dispatched(self):
        # Map the command to an event
        self.context.map_command("test_event", self.command)

        # Dispatch the event
        event = Event("test_event", "test_data")
        self.context.dispatch(event)

        # Verify the command was executed with the correct data
        self.assertTrue(self.command.execute_called)
        self.assertEqual(self.command.last_data, "test_data")

    def test_command_not_executed_for_unmapped_event(self):
        # Map the command to a specific event
        self.context.map_command("test_event", self.command)

        # Dispatch a different event
        event = Event("different_event", "test_data")
        self.context.dispatch(event)

        # Verify the command was not executed
        self.assertFalse(self.command.execute_called)

    def test_multiple_commands_for_same_event(self):
        # Create a second command
        command2 = MockCommand(self.model)

        # Map both commands to the same event
        self.context.map_command("test_event", self.command)
        self.context.map_command("test_event", command2)

        # Dispatch the event
        event = Event("test_event", "test_data")
        self.context.dispatch(event)

        # Verify both commands were executed
        self.assertTrue(self.command.execute_called)
        self.assertTrue(command2.execute_called)
        self.assertEqual(self.command.last_data, "test_data")
        self.assertEqual(command2.last_data, "test_data")

    def test_same_command_for_multiple_events(self):
        # Map the command to two different events
        self.context.map_command("event1", self.command)
        self.context.map_command("event2", self.command)

        # Dispatch the first event
        event1 = Event("event1", "data1")
        self.context.dispatch(event1)

        # Verify the command was executed with the first event's data
        self.assertTrue(self.command.execute_called)
        self.assertEqual(self.command.last_data, "data1")

        # Reset the command's state
        self.command.execute_called = False
        self.command.last_data = None

        # Dispatch the second event
        event2 = Event("event2", "data2")
        self.context.dispatch(event2)

        # Verify the command was executed with the second event's data
        self.assertTrue(self.command.execute_called)
        self.assertEqual(self.command.last_data, "data2")


if __name__ == '__main__':
    unittest.main()
