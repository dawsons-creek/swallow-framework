"""
Example showing how to use the Swallow Framework in a simple application.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from swallow_framework import Model, Command, View, Context, EventDispatcher, Event, state


# Define a model for a counter application
class CounterModel(Model):
    count = state(0)
    history = state([])

    def increment(self, amount=1):
        # With operator overloading, we can do this directly
        self.count += amount
        self.history.append(f"Incremented by {amount}")

    def decrement(self, amount=1):
        # With operator overloading, we can do this directly
        self.count -= amount
        self.history.append(f"Decremented by {amount}")

    def reset(self):
        # Can still use .value explicitly if we want
        self.count.value = 0
        self.history.append("Reset to 0")

    def is_positive(self):
        # Direct comparison with integers
        return self.count > 0

    def double(self):
        # Direct multiplication
        self.count *= 2
        self.history.append("Doubled")


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


class DoubleCommand(Command):
    def execute(self, data):
        self.model.double()


# Define a context for the counter application
class CounterContext(Context):
    def __init__(self, event_dispatcher, model):
        super().__init__(event_dispatcher)
        self.model = model

        # Map commands to events
        self.map_command("INCREMENT", IncrementCommand(model))
        self.map_command("DECREMENT", DecrementCommand(model))
        self.map_command("RESET", ResetCommand(model))
        self.map_command("DOUBLE", DoubleCommand(model))


# Define a view for the counter application
class CounterView(View):
    def __init__(self, context, model):
        super().__init__(context)
        self.model = model

        # Register for model changes
        self.model.on_change('count', self.on_count_changed)
        self.model.on_change('history', self.on_history_changed)

    def on_count_changed(self, value):
        status = "positive" if self.model.is_positive() else "non-positive"
        print(f"Count changed to: {value} ({status})")

    def on_history_changed(self, value):
        if value:
            print(f"Last action: {value[-1]}")

    def increment_clicked(self, amount=1):
        self.dispatch(Event("INCREMENT", {"amount": amount}))

    def decrement_clicked(self, amount=1):
        self.dispatch(Event("DECREMENT", {"amount": amount}))

    def reset_clicked(self):
        self.dispatch(Event("RESET"))

    def double_clicked(self):
        self.dispatch(Event("DOUBLE"))


# Demo application
def main():
    # Create the model, event dispatcher, context, and view
    model = CounterModel()
    event_dispatcher = EventDispatcher()
    context = CounterContext(event_dispatcher, model)
    view = CounterView(context, model)

    # Simulate user interactions
    print("=== Counter Application Demo ===")
    print("Initial count:", model.count)  # Direct access, no .value needed

    view.increment_clicked()
    view.increment_clicked(5)
    view.decrement_clicked(2)
    view.double_clicked()
    view.reset_clicked()

    print("\nFinal history:")
    for i, entry in enumerate(model.history):
        print(f"{i + 1}. {entry}")

    # Example with direct numeric operations
    print("\nDemonstrating direct operations:")
    model.count = 5
    print(f"Set count to: {model.count}")

    result = model.count * 2
    print(f"count * 2 = {result}")

    model.count += 3
    print(f"After count += 3: {model.count}")

    # Boolean conditions
    if model.count > 7:
        print("Count is greater than 7")
    else:
        print("Count is not greater than 7")


if __name__ == "__main__":
    main()