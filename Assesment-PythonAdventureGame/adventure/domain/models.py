"""Domain values shared by the adventure game's rules and use cases."""

from dataclasses import dataclass
from enum import Enum


class Outcome(Enum):
    WON = "won"
    LOST = "lost"


@dataclass(frozen=True)
class ChoiceMenu:
    prompt: str
    choices: tuple[str, ...]


@dataclass(frozen=True)
class PathProgress:
    messages: tuple[str, ...]
    next_choice: ChoiceMenu | None
    outcome: Outcome | None


@dataclass(frozen=True)
class GameResult:
    player_name: str
    outcome: Outcome
