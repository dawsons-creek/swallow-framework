import pytest
from abc import ABC

from src.swallow_framework.mvcc.command import Command
from src.swallow_framework.mvcc.model import Model
from src.swallow_framework.exceptions import SwallowArgumentError


class MockModel(Model):
    def __init__(self):
        super().__init__()
        self.data = None


class MockCommand(Command):
    def execute(self, data):
        self.model.data = data


class TestCommand:
    @pytest.fixture
    def mock_model(self):
        return MockModel()

    def test_command_creation_success(self, mock_model):
        command = MockCommand(mock_model)
        assert command.model == mock_model

    def test_command_creation_invalid_model(self):
        with pytest.raises(SwallowArgumentError):
            MockCommand("not a model")

    def test_execute_success(self, mock_model):
        command = MockCommand(mock_model)
        command.execute("test data")
        assert mock_model.data == "test data"

    def test_abstract_command_cannot_be_instantiated(self, mock_model):
        class AbstractCommand(Command, ABC):
            pass

        with pytest.raises(TypeError):
            AbstractCommand(mock_model)

    def test_execute_must_be_implemented(self, mock_model):
        class InvalidCommand(Command):
            pass

        with pytest.raises(TypeError):
            InvalidCommand(mock_model)
