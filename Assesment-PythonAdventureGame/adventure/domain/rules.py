"""Pure story decision rules for the forest and cave routes."""

from enum import Enum

from adventure.domain.models import ChoiceMenu, Outcome, PathProgress


class ForestOpening(str, Enum):
    FOLLOW_RIVER = "Follow the river"
    CLIMB_TREE = "Climb the tree"


class ForestCrossing(str, Enum):
    FOLLOW_MARKERS = "Follow the carved markers"
    TAKE_SHORTCUT = "Take a shortcut across the ravine"


class CaveOpening(str, Enum):
    LIGHT_TORCH = "Light a torch"
    PROCEED_DARK = "Proceed in the dark"


class CavePassage(str, Enum):
    FOLLOW_SYMBOLS = "Follow the symbols"
    FOLLOW_ECHO = "Follow a distant echo"


FOREST_OPENING_MENU = ChoiceMenu(
    "What will you do?",
    tuple(choice.value for choice in ForestOpening),
)
FOREST_CROSSING_MENU = ChoiceMenu(
    "How will you cross the clearing?",
    tuple(choice.value for choice in ForestCrossing),
)
CAVE_OPENING_MENU = ChoiceMenu(
    "How will you proceed?",
    tuple(choice.value for choice in CaveOpening),
)
CAVE_PASSAGE_MENU = ChoiceMenu(
    "Which way will you go?",
    tuple(choice.value for choice in CavePassage),
)


def begin_forest(choice: ForestOpening) -> PathProgress:
    if choice is ForestOpening.CLIMB_TREE:
        return PathProgress(
            ("A branch snaps beneath you. Your adventure ends in the forest.",),
            None,
            Outcome.LOST,
        )
    return PathProgress(
        ("The river leads to a clearing marked with ancient blue stones.",),
        FOREST_CROSSING_MENU,
        None,
    )


def finish_forest(choice: ForestCrossing) -> PathProgress:
    if choice is ForestCrossing.FOLLOW_MARKERS:
        return PathProgress(
            ("The markers guide you safely to the legendary treasure. You win!",),
            None,
            Outcome.WON,
        )
    return PathProgress(
        ("The loose path gives way, and you cannot reach the treasure.",),
        None,
        Outcome.LOST,
    )


def begin_cave(choice: CaveOpening) -> PathProgress:
    if choice is CaveOpening.PROCEED_DARK:
        return PathProgress(
            ("You lose your way in the darkness. Your adventure ends.",),
            None,
            Outcome.LOST,
        )
    return PathProgress(
        ("Torchlight reveals a wall covered in old symbols.",),
        CAVE_PASSAGE_MENU,
        None,
    )


def finish_cave(choice: CavePassage) -> PathProgress:
    if choice is CavePassage.FOLLOW_SYMBOLS:
        return PathProgress(
            ("The symbols lead to the legendary treasure. You win!",),
            None,
            Outcome.WON,
        )
    return PathProgress(
        ("The echo fades in a dead end. You leave the cave without the treasure.",),
        None,
        Outcome.LOST,
    )
