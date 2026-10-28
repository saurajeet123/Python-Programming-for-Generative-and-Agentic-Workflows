"""Composition root for launching the command-line adventure game."""

from adventure.adapters.console import ConsoleGameIO
from adventure.application.game import GameApplication


def main() -> None:
    GameApplication(ConsoleGameIO()).run()


if __name__ == "__main__":
    main()
