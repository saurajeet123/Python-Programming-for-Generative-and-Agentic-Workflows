# Python Adventure Game

A replayable, choice-driven command-line game about exploring an ancient land
to find a legendary treasure. It uses Python functions, lists (choice menus),
loops, conditionals, input validation, and branching story paths.

The code follows a lightweight Clean Architecture approach: domain rules are
independent of CLI input/output, the application coordinates game sessions,
and a console adapter handles terminal interaction.

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for the architecture, game flow,
design decisions, and testing strategy.

## Requirements

- Python 3.10 or newer
- No third-party dependencies

## Play

From this directory, run:

```powershell
python adventure_game.py
```

The root `adventure_game.py` is the composition root that connects the console
adapter to the application. No package installation is needed.

Enter your name, select a forest or cave path, and enter a menu number or its
choice text. Invalid selections are explained and prompted again. Each route
contains additional decisions and can lead to victory or a failed attempt.
After either outcome, choose whether to restart.

## Test

```powershell
python -m unittest -v
```

## Architecture

```text
adventure_game.py                 Composition root / CLI entry point
adventure/
├── domain/
│   ├── models.py                 Game result and path value objects
│   └── rules.py                  Pure forest and cave decision rules
├── application/
│   ├── ports.py                  GameIO protocol required by the use case
│   └── game.py                   Game session orchestration
└── adapters/
    └── console.py                Terminal input, output, and validation
```

- **Domain** defines game outcomes, story menus, and the rules that resolve
  choices. It has no dependency on the terminal or application layer.
- **Application** coordinates a game round and replay loop through the
  `GameIO` protocol. It does not call `input()` or `print()` directly.
- **Adapters** implement the protocol for a command-line terminal, including
  numbered/text choice handling and invalid-input retries.
- **Composition root** wires the adapter into the application. A different
  interface can implement `GameIO` and be injected without changing game rules.

## Project files

- `adventure/` contains domain, application, and adapter layers.
- `adventure_game.py` wires the CLI and application together.
- `test_adventure_game.py` tests domain decisions, application flows, replay,
  and terminal input validation.
- `generate_copilot_report.py` creates the assignment's short PDF write-up
  using only the Python standard library.
- `reports/copilot_assistance_report.pdf` is the generated write-up.

Regenerate the PDF after changing its report content with:

```powershell
python generate_copilot_report.py
```
