"""
Bridge of Death Quiz Example

A Monty Python-inspired application built with the Swallow Framework.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from swallow_framework import Model, Command, Event, EventDispatcher, Context, View, state


# ----- 1. Define Models -----
class QuestionsModel(Model):
    current_question = state(0)
    answers = state([])
    outcome = state("")

    QUESTIONS = [
        "What is your name?",
        "What is your quest?",
        "What is the airspeed velocity of an unladen swallow?"
    ]

    def get_current_question(self):
        if self.current_question < len(self.QUESTIONS):
            return self.QUESTIONS[int(self.current_question)]
        return None

    def ANSWER_QUESTION(self, answer):
        self.answers.append(answer)

        # Special logic for the swallow question
        if self.current_question == 2:
            if "african or european" in answer.lower():
                self.outcome = "PASS"
            else:
                self.outcome = "FAIL"

        # Move to next question if not at the end
        if self.current_question < len(self.QUESTIONS) - 1:
            self.current_question += 1

    def RESET_QUIZ(self):
        # Direct assignment
        self.current_question = 0
        self.answers = []
        self.outcome = ""


# ----- 2. Define Commands -----
class AnswerCommand(Command):
    def execute(self, data):
        self.model.ANSWER_QUESTION(data["answer"])


class ResetCommand(Command):
    def execute(self, data):
        self.model.RESET_QUIZ()


# ----- 3. Set up Context -----
class QuizContext(Context):
    def __init__(self, event_dispatcher: EventDispatcher, model: QuestionsModel):
        super().__init__(event_dispatcher)
        self.model = model

        # Map events to commands
        self.map_command("ANSWER_QUESTION", AnswerCommand(model))
        self.map_command("RESET_QUIZ", ResetCommand(model))


# ----- 4. Create Views -----
class TerminalView(View):
    def __init__(self, context, model):
        super().__init__(context)
        self.model = model

        # Listen for model changes
        self.model.on_change('current_question', self.on_question_change)
        self.model.on_change('outcome', self.on_outcome_change)

    def on_question_change(self, value):
        question = self.model.get_current_question()
        if question:
            print(f"\nBRIDGE KEEPER: {question}")

    def on_outcome_change(self, outcome):
        if outcome == "PASS":
            print("\nBRIDGE KEEPER: Right. Off you go.")
            print("*You cross the Bridge of Death successfully*")
        elif outcome == "FAIL":
            print("\nBRIDGE KEEPER: *launches you into the gorge*")
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHH!")

    def answer(self, text):
        print(f"YOU: {text}")
        self.dispatch(Event("ANSWER_QUESTION", {"answer": text}))

    def reset(self):
        self.dispatch(Event("RESET_QUIZ", None))
        print("\n--- NEW CHALLENGER APPROACHES ---")


# ----- 5. Usage Example -----
def run_example():
    # Initialize the application
    model = QuestionsModel()
    event_dispatcher = EventDispatcher()
    context = QuizContext(event_dispatcher, model)
    view = TerminalView(context, model)

    # First attempt - failure
    print("--- THE BRIDGE OF DEATH ---")
    print("BRIDGE KEEPER: STOP! Who would cross the Bridge of Death must answer me these questions three.")

    view.on_question_change(0)  # Trigger first question
    view.answer("Sir Lancelot of Camelot")
    view.answer("To seek the Holy Grail")
    view.answer("What? I don't know that!")

    # Reset and try again - success
    view.reset()

    view.on_question_change(0)  # Trigger first question
    view.answer("Sir Robin of Camelot")
    view.answer("To seek the Holy Grail")
    view.answer("What do you mean? African or European swallow?")


if __name__ == "__main__":
    run_example()