import unittest
from collections.abc import Sequence
from unittest.mock import patch

from adventure.adapters.console import ConsoleGameIO
from adventure.application.game import GameApplication
from adventure.domain.models import GameResult, Outcome
from adventure.domain.rules import (
    CaveOpening,
    CavePassage,
    ForestCrossing,
    ForestOpening,
    begin_cave,
    begin_forest,
    finish_cave,
    finish_forest,
)


class FakeGameIO:
    def __init__(self, answers: list[str]) -> None:
        self._answers = iter(answers)
        self.messages: list[str] = []

    def write(self, message: str) -> None:
        self.messages.append(message)

    def read_text(self, _prompt: str) -> str:
        return next(self._answers)

    def choose(self, _prompt: str, choices: Sequence[str]) -> str:
        answer = next(self._answers)
        if answer not in choices:
            raise AssertionError(f"Unexpected answer {answer!r}; expected one of {choices!r}")
        return answer


class DomainRuleTests(unittest.TestCase):
    def test_forest_winning_and_losing_outcomes(self) -> None:
        self.assertEqual(
            begin_forest(ForestOpening.CLIMB_TREE).outcome,
            Outcome.LOST,
        )
        self.assertEqual(
            finish_forest(ForestCrossing.FOLLOW_MARKERS).outcome,
            Outcome.WON,
        )
        self.assertEqual(
            finish_forest(ForestCrossing.TAKE_SHORTCUT).outcome,
            Outcome.LOST,
        )

    def test_cave_winning_and_losing_outcomes(self) -> None:
        self.assertEqual(begin_cave(CaveOpening.PROCEED_DARK).outcome, Outcome.LOST)
        self.assertEqual(finish_cave(CavePassage.FOLLOW_SYMBOLS).outcome, Outcome.WON)
        self.assertEqual(finish_cave(CavePassage.FOLLOW_ECHO).outcome, Outcome.LOST)

    def test_safe_opening_choices_provide_a_follow_up_menu(self) -> None:
        self.assertIsNotNone(begin_forest(ForestOpening.FOLLOW_RIVER).next_choice)
        self.assertIsNotNone(begin_cave(CaveOpening.LIGHT_TORCH).next_choice)


class GameApplicationTests(unittest.TestCase):
    def play_with(self, answers: list[str]) -> FakeGameIO:
        game_io = FakeGameIO(answers)
        GameApplication(game_io).run()
        return game_io

    def test_forest_route_can_win(self) -> None:
        game_io = self.play_with(
            ["Rin", "Explore the dark forest", "Follow the river",
             "Follow the carved markers", "No"]
        )
        self.assertIn(
            "The markers guide you safely to the legendary treasure. You win!",
            game_io.messages,
        )

    def test_cave_route_can_win(self) -> None:
        game_io = self.play_with(
            ["Sam", "Enter the mysterious cave", "Light a torch",
             "Follow the symbols", "No"]
        )
        self.assertIn(
            "The symbols lead to the legendary treasure. You win!",
            game_io.messages,
        )

    def test_loss_can_be_followed_by_a_new_winning_round(self) -> None:
        game_io = self.play_with(
            ["Kai", "Enter the mysterious cave", "Proceed in the dark", "Yes",
             "Kai", "Explore the dark forest", "Follow the river",
             "Follow the carved markers", "No"]
        )
        self.assertIn(
            "You lose your way in the darkness. Your adventure ends.",
            game_io.messages,
        )
        self.assertIn(
            "The markers guide you safely to the legendary treasure. You win!",
            game_io.messages,
        )
        self.assertEqual(game_io.messages.count("=== The Lost Treasure ==="), 2)

    def test_empty_name_uses_explorer_default(self) -> None:
        game_io = self.play_with(
            ["", "Enter the mysterious cave", "Proceed in the dark", "No"]
        )
        self.assertIn(
            "\nWelcome, Explorer. Your quest begins now!",
            game_io.messages,
        )

    def test_application_returns_final_round_result(self) -> None:
        game_io = FakeGameIO(
            ["Rin", "Explore the dark forest", "Follow the river",
             "Follow the carved markers", "No"]
        )
        result = GameApplication(game_io).run()
        self.assertEqual(result, GameResult("Rin", Outcome.WON))

    def test_console_adapter_reprompts_invalid_choices(self) -> None:
        game_io = ConsoleGameIO()
        with (
            patch("builtins.input", side_effect=["invalid", "2"]),
            patch("builtins.print") as print_mock,
        ):
            result = game_io.choose("Choose a path", ("Forest", "Cave"))

        self.assertEqual(result, "Cave")
        self.assertTrue(
            any(
                call.args == ("That is not a valid choice. Try again.",)
                for call in print_mock.call_args_list
            )
        )


if __name__ == "__main__":
    unittest.main()
