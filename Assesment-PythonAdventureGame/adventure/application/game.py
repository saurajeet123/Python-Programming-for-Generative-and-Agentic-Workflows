"""Use case coordinating a player's game session."""

from adventure.application.ports import GameIO
from adventure.domain.models import ChoiceMenu, GameResult, PathProgress
from adventure.domain.rules import (
    CAVE_OPENING_MENU,
    FOREST_OPENING_MENU,
    CaveOpening,
    CavePassage,
    ForestCrossing,
    ForestOpening,
    begin_cave,
    begin_forest,
    finish_cave,
    finish_forest,
)


class GameApplication:
    def __init__(self, game_io: GameIO) -> None:
        self._io = game_io

    def run(self) -> GameResult:
        while True:
            result = self._play_round()
            replay = self._io.choose(
                "\nWould you like to play again?",
                ("Yes", "No"),
            )
            if replay == "No":
                self._io.write("Thanks for playing. Farewell, explorer!")
                return result

    def _play_round(self) -> GameResult:
        self._io.write("=== The Lost Treasure ===")
        self._io.write(
            "Explore an ancient land, make wise choices, and find the legendary treasure."
        )
        player_name = self._io.read_text("What is your name? ").strip() or "Explorer"
        self._io.write(f"\nWelcome, {player_name}. Your quest begins now!")

        path = self._io.choose(
            "Where will you begin?",
            ("Explore the dark forest", "Enter the mysterious cave"),
        )
        if path == "Explore the dark forest":
            progress = self._play_forest()
        else:
            progress = self._play_cave()
        if progress.outcome is None:
            raise RuntimeError("A completed path must have a final outcome.")
        return GameResult(player_name, progress.outcome)

    def _play_forest(self) -> PathProgress:
        self._io.write("\nYou enter the dark forest. A river rushes past an old tree.")
        opening = ForestOpening(self._choose_menu(FOREST_OPENING_MENU))
        progress = begin_forest(opening)
        if progress.next_choice is None:
            return self._show_progress(progress)

        crossing = ForestCrossing(self._choose_menu(progress.next_choice))
        return self._show_progress(finish_forest(crossing))

    def _play_cave(self) -> PathProgress:
        self._io.write("\nYou step into a mysterious cave. The passage is pitch-black.")
        opening = CaveOpening(self._choose_menu(CAVE_OPENING_MENU))
        progress = begin_cave(opening)
        if progress.next_choice is None:
            return self._show_progress(progress)

        passage = CavePassage(self._choose_menu(progress.next_choice))
        return self._show_progress(finish_cave(passage))

    def _choose_menu(self, menu: ChoiceMenu) -> str:
        return self._io.choose(menu.prompt, menu.choices)

    def _show_progress(self, progress: PathProgress) -> PathProgress:
        for message in progress.messages:
            self._io.write(message)
        return progress
