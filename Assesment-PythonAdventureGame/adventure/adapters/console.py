"""Command-line implementation of the game's input/output port."""

from collections.abc import Sequence


class ConsoleGameIO:
    def write(self, message: str) -> None:
        print(message)

    def read_text(self, prompt: str) -> str:
        return input(prompt)

    def choose(self, prompt: str, choices: Sequence[str]) -> str:
        while True:
            self.write(prompt)
            for index, choice in enumerate(choices, start=1):
                self.write(f"{index}. {choice}")

            answer = self.read_text("Enter a choice: ").strip().lower()
            for index, choice in enumerate(choices, start=1):
                if answer == str(index) or answer == choice.lower():
                    return choice

            self.write("That is not a valid choice. Try again.")
