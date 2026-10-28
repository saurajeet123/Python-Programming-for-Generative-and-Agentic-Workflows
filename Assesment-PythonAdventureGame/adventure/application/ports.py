"""Interfaces required by the game use case."""

from collections.abc import Sequence
from typing import Protocol


class GameIO(Protocol):
    def write(self, message: str) -> None: ...

    def read_text(self, prompt: str) -> str: ...

    def choose(self, prompt: str, choices: Sequence[str]) -> str: ...
