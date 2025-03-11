# Swallow Framework

A lightweight, reactive Model-View-Command-Context (MVCC) framework for building structured applications with event-driven architecture.

## Overview

Swallow Framework provides a modern approach to application architecture by combining the best aspects of MVC with reactive state management and the command pattern. It's designed to create maintainable, testable applications with clear separation of concerns.

### Key Features

- **Model-View-Command-Context Pattern**: A structured approach to application architecture
- **Reactive State Management**: Observable properties with automatic change detection and notification
- **Event-Driven Communication**: Components communicate through events rather than direct references
- **Command Pattern Implementation**: Actions encapsulated as commands for better testability
- **Lightweight and Flexible**: Minimal dependencies and adaptable to different application types



## Installation

```bash
pip install git+https://github.com/rocket-tycoon/swallow-framework.git
```

You can also clone the repository and install it locally:

```bash
git clone https://github.com/rocket-tycoon/swallow-framework.git
cd swallow-framework
pip install -e .
```

## Getting Started

Here's a complete example to help you get started with the Swallow Framework:

### 1. Define your Model

```python
from swallow_framework.mvcc.model import Model
from swallow_framework.state.property import state

class UserModel(Model):
    name = state("")
    email = state("")
    
    def update_user(self, name, email):
        self.name = name
        self.email = email
        
    def reset(self):
        self.name = ""
        self.email = ""
```

### 2. Create Commands

```python
from swallow_framework.mvcc.command import Command

class UpdateUserCommand(Command):
    def execute(self, data):
        self.model.update_user(data["name"], data["email"])

class ResetUserCommand(Command):
    def execute(self, data):
        self.model.reset()
```

### 3. Set up the Context

```python
from swallow_framework.mvcc.context import Context
from swallow_framework.core.events import EventDispatcher

class AppContext(Context):
    def __init__(self):
        # Create event dispatcher
        event_dispatcher = EventDispatcher()
        super().__init__(event_dispatcher)
        
        # Create model
        self.user_model = UserModel()
        
        # Map events to commands
        self.map_command("update_user", UpdateUserCommand(self.user_model))
        self.map_command("reset_user", ResetUserCommand(self.user_model))
```

### 4. Create a View

```python
from swallow_framework.mvcc.view import View
from swallow_framework.core.events import Event

class UserFormView(View):
    def __init__(self, context):
        super().__init__(context)
        
        # Listen for model changes
        self.context.user_model.on_change('name', self.on_name_changed)
        self.context.user_model.on_change('email', self.on_email_changed)
    
    def on_name_changed(self, value):
        print(f"Name updated to: {value}")
    
    def on_email_changed(self, value):
        print(f"Email updated to: {value}")
    
    def submit_form(self, name, email):
        print("Form submitted, dispatching update_user event")
        self.dispatch(Event("update_user", {"name": name, "email": email}))
    
    def reset_form(self):
        print("Reset button clicked, dispatching reset_user event")
        self.dispatch(Event("reset_user", None))
```

### 5. Putting it all together

```python
# Create the application context
context = AppContext()

# Create a view with the context
view = UserFormView(context)

# Handle user interactions
view.submit_form("Alice", "alice@example.com")
# Output:
# Form submitted, dispatching update_user event
# Name updated to: Alice
# Email updated to: alice@example.com

# Reset the form
view.reset_form()
# Output:
# Reset button clicked, dispatching reset_user event
# Name updated to: 
# Email updated to: 
```

This example demonstrates the core concepts of the Swallow Framework:
- Models with reactive state properties
- Commands that encapsulate actions
- A context that connects events to commands
- Views that dispatch events and react to model changes

## Examples

Check the `examples/` directory for complete application examples using the Swallow Framework.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
