"""
Example showing how to use the Swallow Framework in a simple application.
"""

from src.swallow_framework import Model, Command, Event, EventDispatcher, Context, View
from src.swallow_framework.state import state


# Define a model for a counter application
class CounterModel(Model):
    count = state(0)
    history = state([])

    def increment(self, amount=1):
        self.count.value += amount
        self.history.append(f"Incremented by {amount}")

    def decrement(self, amount=1):
        self.count.value -= amount
        self.history.append(f"Decremented by {amount}")

    def reset(self):
        self.count.value = 0
        self.history.append("Reset to 0")


# Define commands for the counter application
class IncrementCommand(Command):
    def execute(self, data):
        amount = data.get('amount', 1)
        self.model.increment(amount)


class DecrementCommand(Command):
    def execute(self, data):
        amount = data.get('amount', 1)
        self.model.decrement(amount)


class ResetCommand(Command):
    def execute(self, data):
        self.model.reset()


# Define a context for the counter application
class CounterContext(Context):
    def __init__(self, event_dispatcher, model):
        super().__init__(event_dispatcher)
        self.model = model

        # Map commands to events
        self.map_command("INCREMENT", IncrementCommand(model))
        self.map_command("DECREMENT", DecrementCommand(model))
        self.map_command("RESET", ResetCommand(model))


# Define a view for the counter application
class CounterView(View):
    def __init__(self, context, model):
        super().__init__(context)
        self.model = model

        # Register for model changes
        self.model.on_change('count', self.on_count_changed)
        self.model.on_change('history', self.on_history_changed)

    def on_count_changed(self, value):
        print(f"Count changed to: {value}")

    def on_history_changed(self, value):
        if value:
            print(f"Last action: {value[-1]}")

    def increment_clicked(self, amount=1):
        self.dispatch(Event("INCREMENT", {"amount": amount}))

    def decrement_clicked(self, amount=1):
        self.dispatch(Event("DECREMENT", {"amount": amount}))

    def reset_clicked(self):
        self.dispatch(Event("RESET"))


# Demo application
def main():
    # Create the model, event dispatcher, context, and view
    model = CounterModel()
    event_dispatcher = EventDispatcher()
    context = CounterContext(event_dispatcher, model)
    view = CounterView(context, model)

    # Simulate user interactions
    print("=== Counter Application Demo ===")
    view.increment_clicked()
    view.increment_clicked(5)
    view.decrement_clicked(2)
    view.reset_clicked()

    print("\nFinal history:")
    for i, entry in enumerate(model.history):
        print(f"{i + 1}. {entry}")


if __name__ == "__main__":
    main()
