<img src="assets/swallow_illustration.jpg" alt="Swallow Framework" width="740px"/>

# Swallow Framework 🐦

*A lightweight, reactive Model-View-Command-Context (MVCC) framework for building
structured applications with event-driven architecture.*

## Overview

Swallow Framework brings the speed and agility of a laden—or perhaps unladen—swallow 
to your Python applications. It's built around the Model-View-Command-Context pattern, 
ensuring clean separation of concerns, observability, and reactive state management.

## Key Features

- **Model-View-Command-Context Pattern**: A structured approach to application architecture
- **Reactive State Management**: Observable properties with automatic change detection and notification
- **Event-Driven Communication**: Components communicate through events rather than direct references
- **Command Pattern Implementation**: Actions encapsulated as commands for better testability
- **Lightweight and Flexible**: Minimal dependencies and adaptable to different application types

## Installation

```bash
pip install git+https://github.com/dawsons-creek/swallow-framework.git@v1.0.2
```

You can also clone the repository and install it locally:

```bash
git clone https://github.com/dawsons-creek/swallow-framework.git
cd swallow-framework
pip install -e .
```

## Running the Examples

The repository includes several example applications that demonstrate how to use the Swallow Framework:

```bash
# Run the counter example (simple state management)
python examples/counter.py

# Run the todo list application (complete MVCC example)
python examples/todo.py

# Run the Bridge of Death quiz (Monty Python inspired)
python examples/quiz.py
```

## Architecture

Swallow Framework is built on four main components:

### Model

Models manage application state using reactive properties. Any changes to these properties 
automatically notify registered listeners.

```python
from swallow_framework import Model, state

class UserModel(Model):
    name = state("")
    age = state(0)
    
    def update_user(self, name, age):
        self.name = name
        self.age = age

# Listen for changes
user = UserModel()
user.on_change('name', lambda value: print(f"Name changed to: {value}"))
```

#### Working with State Properties

State properties in Swallow Framework are reactive - they automatically notify listeners when their values change.

```python
# Define state properties
class UserModel(Model):
    name = state("")
    age = state(0)
    items = state([])
    
# Use them like regular properties
model = UserModel()
model.name = "Alice"            # Set a value
model.age += 1                  # Increment directly
if model.age >= 18:             # Compare directly
    print(f"{model.name} is an adult")

# List operations work as expected
model.items.append("Item 1")    # Add to list
model.items.clear()             # Clear list
model.items = ["A", "B", "C"]   # Replace entire list
```

**Key features:**

- Use arithmetic operators: `+=`, `-=`, `*=`, etc.
- Compare directly with other values: `<`, `>`, `==`, etc.
- Use numeric values as list indices: `list[model.index]` 
- Call methods on the wrapped value: `model.name.upper()`
- All changes to state values trigger registered listeners

**Registering for changes:**

```python
# Listen for state changes using callbacks
def on_name_changed(new_name):
    print(f"Name changed to: {new_name}")
    
model.on_change('name', on_name_changed)

# Or use as a decorator
@model.on_change('age')
def handle_age_change(new_age):
    print(f"Age is now: {new_age}")
```

The reactive state system ensures your UI or other components stay in sync with your model's data, automatically notifying listeners whenever state values change.

### View

Views handle user interaction and dispatch events through the context.

```python
from swallow_framework import View, Event

class UserFormView(View):
    def submit_form(self, name, age):
        self.dispatch(Event("update_user", {"name": name, "age": age}))
```

### Command

Commands encapsulate actions to be performed on models.

```python
from swallow_framework import Command

class UpdateUserCommand(Command):
    def execute(self, data):
        self.model.update_user(data["name"], data["age"])
```

### Context

The context maps events to commands and facilitates event dispatching.

```python
from swallow_framework import Context, EventDispatcher

class AppContext(Context):
    def __init__(self):
        super().__init__(EventDispatcher())
        
        # Map events to commands
        user_model = UserModel()
        self.map_command("update_user", UpdateUserCommand(user_model))
```

## Getting Started

1. Create your models with reactive state properties
2. Define commands to encapsulate actions on models
3. Create a context that maps events to commands
4. Build views that dispatch events through the context

```python
# Create the application context
context = AppContext()
# Create a view with the context
view = UserFormView(context)
# Handle user interactions
view.submit_form("Alice", 30)
```

## Complete Application Example

Here's a simple counter application using the Swallow Framework:

```python
from swallow_framework import Model, Command, View, Context, EventDispatcher, Event, state

# Define a model
class CounterModel(Model):
    count = state(0)
    
    def increment(self, amount=1):
        self.count += amount  # Direct operation
    
    def reset(self):
        self.count = 0  # Direct assignment

# Define commands
class IncrementCommand(Command):
    def execute(self, data):
        amount = data.get('amount', 1)
        self.model.increment(amount)

class ResetCommand(Command):
    def execute(self, data):
        self.model.reset()

# Define context
class CounterContext(Context):
    def __init__(self, event_dispatcher, model):
        super().__init__(event_dispatcher)
        
        # Map commands to events
        self.map_command("INCREMENT", IncrementCommand(model))
        self.map_command("RESET", ResetCommand(model))

# Define view
class CounterView(View):
    def __init__(self, context, model):
        super().__init__(context)
        self.model = model
        
        # Register for model changes
        self.model.on_change('count', self.on_count_changed)
    
    def on_count_changed(self, value):
        print(f"Count is now: {value}")
        
    def increment_button_click(self, amount=1):
        self.dispatch(Event("INCREMENT", {"amount": amount}))
        
    def reset_button_click(self):
        self.dispatch(Event("RESET"))

# Create application components
model = CounterModel()
event_dispatcher = EventDispatcher()
context = CounterContext(event_dispatcher, model)
view = CounterView(context, model)

# Simulate user interaction
view.increment_button_click()  # Count is now: 1
view.increment_button_click(5)  # Count is now: 6
view.reset_button_click()  # Count is now: 0
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
