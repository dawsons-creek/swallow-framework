"""
Todo Application Example using the Swallow Framework
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import datetime
import sys
import uuid
from typing import Dict, List, Optional

from swallow_framework import Model, Command, Event, EventDispatcher, Context, View, state


class TodoItem:
    """Represents a single todo item."""

    def __init__(self, text: str):
        self.id = str(uuid.uuid4())
        self.text = text
        self.completed = False
        self.created_at = datetime.datetime.now()
        self.completed_at = None

    def toggle(self) -> None:
        """Toggle completion status."""
        self.completed = not self.completed
        self.completed_at = datetime.datetime.now() if self.completed else None

    def __str__(self) -> str:
        return f"[{'✓' if self.completed else ' '}] {self.text}"


class TodoModel(Model):
    """Model for the todo application."""
    items = state([])
    filter_completed = state(False)

    def add_item(self, text: str) -> None:
        if text.strip():
            self.items.append(TodoItem(text))

    def remove_item(self, item_id: str) -> None:
        self.items = [item for item in self.items if item.id != item_id]

    def toggle_item(self, item_id: str) -> None:
        for item in self.items:
            if item.id == item_id:
                item.toggle()
                self.items = list(self.items)
                break

    def toggle_filter(self) -> None:
        self.filter_completed = not self.filter_completed

    def get_filtered_items(self) -> List[TodoItem]:
        if self.filter_completed:
            return [item for item in self.items if not item.completed]
        return self.items

    def get_stats(self) -> Dict[str, int]:
        total = len(self.items)
        completed = sum(1 for item in self.items if item.completed)
        return {
            "total": total,
            "active": total - completed,
            "completed": completed
        }

    def get_item_by_id(self, item_id: str) -> Optional[TodoItem]:
        for item in self.items:
            if item.id == item_id:
                return item
        return None


# ----- Commands -----

class AddTodoCommand(Command):
    def execute(self, data: Dict) -> None:
        text = data.get("text", "").strip()
        if text:
            self.model.add_item(text)


class RemoveTodoCommand(Command):
    def execute(self, data: Dict) -> None:
        if item_id := data.get("id"):
            self.model.remove_item(item_id)


class ToggleTodoCommand(Command):
    def execute(self, data: Dict) -> None:
        if item_id := data.get("id"):
            self.model.toggle_item(item_id)


class ToggleFilterCommand(Command):
    def execute(self, data: Dict) -> None:
        self.model.toggle_filter()


# ----- Context -----

class TodoContext(Context):
    def __init__(self, event_dispatcher: EventDispatcher, model: TodoModel):
        super().__init__(event_dispatcher)
        self.model = model

        # Map commands to events
        commands = {
            "ADD_TODO": AddTodoCommand(model),
            "REMOVE_TODO": RemoveTodoCommand(model),
            "TOGGLE_TODO": ToggleTodoCommand(model),
            "TOGGLE_FILTER": ToggleFilterCommand(model),
        }

        for event, command in commands.items():
            self.map_command(event, command)


# ----- View -----

class TodoView(View):
    def __init__(self, context: TodoContext, model: TodoModel):
        super().__init__(context)
        self.model = model

        # Register for model changes
        self.model.on_change('items', self.render)
        self.model.on_change('filter_completed', self.render)

    def render(self, *args) -> None:
        """Render the current state of the todo list."""
        print("\033c", end="")  # Clear console
        print("\n===== SWALLOW TODO APP =====\n")

        # Print filter status
        filter_status = "Active items only" if self.model.filter_completed else "All items"
        print(f"Showing: {filter_status}")

        # Print items
        items = self.model.get_filtered_items()
        if items:
            for i, item in enumerate(items):
                print(f"{i + 1}. {item}")
        else:
            print("No items to display.")

        # Print stats
        stats = self.model.get_stats()
        print(f"\nTotal: {stats['total']} | Active: {stats['active']} | Completed: {stats['completed']}")
        print("\nTIP: You can use one-letter shortcuts (a, t, r, f, q) for commands")

        # Print commands
        print("\nCommands:")
        print("  add, a <text>       - Add a new todo item")
        print("  toggle, t <number>  - Toggle completion status")
        print("  remove, r <number>  - Remove a todo item")
        print("  filter, f           - Toggle filter (all/active only)")
        print("  exit, e, q          - Exit the application")
        print("\n> ", end="")
        sys.stdout.flush()

    def process_command(self, command_line: str) -> bool:
        """Process a command from the user."""
        command_line = command_line.strip()
        if not command_line:
            return True

        parts = command_line.split(maxsplit=1)
        command = parts[0].lower()
        param = parts[1] if len(parts) > 1 else None

        # Handle exit commands
        if command in ("exit", "e", "q"):
            return False

        # Command handling lookup table
        handlers = {
            ("add", "a"): self._handle_add,
            ("toggle", "t"): self._handle_toggle,
            ("remove", "r"): self._handle_remove,
            ("filter", "f"): self._handle_filter,
            ("help", "h"): self._handle_help
        }

        # Find and execute the appropriate handler
        for cmds, handler in handlers.items():
            if command in cmds:
                return handler(param)

        print("\nUnknown command. Type 'help' for assistance.")
        return True

    def _handle_add(self, text) -> bool:
        if text:
            self.dispatch(Event("ADD_TODO", {"text": text}))
        return True

    def _handle_toggle(self, number) -> bool:
        try:
            index = int(number) - 1
            items = self.model.get_filtered_items()
            if 0 <= index < len(items):
                self.dispatch(Event("TOGGLE_TODO", {"id": items[index].id}))
            else:
                print("\nInvalid item number.")
        except (ValueError, TypeError):
            print("\nPlease enter a valid number.")
        return True

    def _handle_remove(self, number) -> bool:
        try:
            index = int(number) - 1
            items = self.model.get_filtered_items()
            if 0 <= index < len(items):
                self.dispatch(Event("REMOVE_TODO", {"id": items[index].id}))
            else:
                print("\nInvalid item number.")
        except (ValueError, TypeError):
            print("\nPlease enter a valid number.")
        return True

    def _handle_filter(self, _) -> bool:
        self.dispatch(Event("TOGGLE_FILTER"))
        return True

    def _handle_help(self, _) -> bool:
        print("\nAvailable commands:")
        print("  a, add <text>          - Add a new todo item")
        print("  t, toggle <number>     - Toggle completion status")
        print("  r, remove <number>     - Remove a todo item")
        print("  f, filter              - Toggle filter (all/active only)")
        print("  e, q, exit             - Exit the application")
        print("  h, help                - Show this help message")
        input("\nPress Enter to continue...")
        return True

    def run(self) -> None:
        """Run the main application loop."""
        self.render()
        running = True

        while running:
            try:
                command = input()
                running = self.process_command(command)
                if running:
                    self.render()
            except KeyboardInterrupt:
                print("\nExiting...")
                running = False
            except Exception as e:
                print(f"\nError: {e}")
                input("Press Enter to continue...")
                self.render()


def main():
    """Main entry point for the todo application."""
    try:
        model = TodoModel()
        event_dispatcher = EventDispatcher()
        context = TodoContext(event_dispatcher, model)
        view = TodoView(context, model)

        # Add example items
        model.add_item("Learn Swallow Framework")
        model.add_item("Build a todo application")
        model.add_item("Implement MVC pattern")

        view.run()
    except Exception as e:
        print(f"Unhandled error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())