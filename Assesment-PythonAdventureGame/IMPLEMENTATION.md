# Python Adventure Game — Project Write-Up

## 1. Project overview

This project is a replayable command-line adventure in which a player explores
an ancient land in search of a legendary treasure. The player chooses a forest
or cave route, makes decisions that lead to success or failure, and can restart
after a round.

The implementation uses a lightweight Clean Architecture structure. Story
rules are separated from the game-session workflow and from terminal input and
output. The project is intended as a small learning example, not as a
production-scale game framework.

## 2. Goals and requirements

The implementation is designed to:

- Introduce the quest and ask for the player's name.
- Offer forest and cave starting routes.
- Present meaningful decisions with both winning and losing outcomes.
- Retry invalid menu input rather than treating it as a valid story choice.
- Let the player replay after either outcome.
- Keep core story decisions testable without running an interactive terminal.
- Use only the Python standard library.

## 3. Architecture

```text
Assesment-PythonAdventureGame/
├── adventure_game.py                 Composition root / executable entry point
├── adventure/
│   ├── domain/
│   │   ├── models.py                 Domain value objects and outcomes
│   │   └── rules.py                  Forest and cave story rules
│   ├── application/
│   │   ├── ports.py                  GameIO interface
│   │   └── game.py                   Game-session use case
│   └── adapters/
│       └── console.py                CLI implementation of GameIO
├── test_adventure_game.py            Domain, application, and adapter tests
├── generate_copilot_report.py        Standard-library PDF report generator
└── reports/
    └── copilot_assistance_report.pdf Assignment report about Copilot assistance
```

### Dependency direction

The domain layer contains the story model and rules and does not depend on the
terminal or application layer. The application layer uses those domain rules
and depends on the `GameIO` protocol, not on `input()` or `print()`. The
console adapter implements that protocol. The root entry point constructs the
adapter and injects it into the application.

This makes the game rules independently testable and allows another interface
to be added by implementing `GameIO`, without changing the domain rules.

## 4. Domain model

`adventure/domain/models.py` defines immutable data objects:

- `Outcome` represents a completed round as `WON` or `LOST`.
- `ChoiceMenu` groups a prompt with its available choices.
- `PathProgress` carries story messages, an optional next menu, and an
  optional final outcome.
- `GameResult` records the player's name and the completed round's outcome.

`adventure/domain/rules.py` defines string enums for the forest and cave
choices and pure functions that map choices to `PathProgress` values. These
functions do not prompt players or print messages.

### Story outcomes

| Route | Choice | Result |
|---|---|---|
| Forest opening | Climb the tree | Lose |
| Forest opening | Follow the river | Continue to the clearing |
| Forest crossing | Follow the carved markers | Win |
| Forest crossing | Take a shortcut across the ravine | Lose |
| Cave opening | Proceed in the dark | Lose |
| Cave opening | Light a torch | Continue to the symbols |
| Cave passage | Follow the symbols | Win |
| Cave passage | Follow a distant echo | Lose |

## 5. Application workflow

`GameApplication` in `adventure/application/game.py` coordinates the
interaction:

1. Display the game introduction.
2. Read and normalize the player's name; use `Explorer` if it is blank.
3. Ask the player to choose the forest or cave.
4. Ask that route's opening decision and, when appropriate, its follow-up.
5. Apply domain rules and display their returned story messages.
6. Require the completed path to have a final outcome and return a
   `GameResult`.
7. Ask whether to replay; repeat the round for `Yes` or finish for `No`.

The result returned by `run()` represents the final round played in the
session. The application expects its `GameIO` adapter to return one of the
choices it was given; the console adapter guarantees this by validating and
re-prompting.

## 6. Console adapter and input handling

`ConsoleGameIO` in `adventure/adapters/console.py` implements the application
port with terminal input and output. For choice menus it:

- Displays choices with one-based numbers.
- Accepts either a menu number or the matching choice text, ignoring
  surrounding whitespace and case.
- Prints an error and repeats the menu when the input is invalid.

Keeping this behavior in the adapter avoids mixing terminal concerns into
story rules.

## 7. Running the project

Python 3.10 or later is required. No package installation is necessary.

From the project directory:

```powershell
python adventure_game.py
```

Run the automated tests with:

```powershell
python -m unittest -v
```

Regenerate the Copilot assistance PDF with:

```powershell
python generate_copilot_report.py
```

## 8. Testing strategy

`test_adventure_game.py` uses Python's built-in `unittest` and focuses on
behavior at the architecture boundaries:

- **Domain rules:** check the forest and cave winning/losing outcomes and
  confirm safe opening choices produce follow-up menus.
- **Application flows:** use a fake `GameIO` to test winning paths, replay
  after a loss, blank-name handling, and the final returned `GameResult`.
- **Console adapter:** mock terminal input/output to verify invalid input is
  rejected and the next valid choice is returned.

This split helps identify whether a failure is in story logic, orchestration,
or terminal interaction.

## 9. Design decisions and trade-offs

- **Small layers over a framework:** the project uses modules and a `Protocol`
  rather than external architecture libraries or dependency-injection
  packages.
- **Enums for story decisions:** enums make the accepted story branches
  explicit and avoid scattering the canonical choice strings throughout the
  domain logic.
- **Immutable value objects:** frozen dataclasses make the domain results
  simple to pass between layers without later mutation.
- **Terminal-specific validation:** retry behavior is implemented where raw
  user input enters the system, so the use case receives a valid menu choice.
- **Simple replay loop:** replay starts a fresh round and asks for the name
  again; there is no persistent player state between rounds.
- **Standard-library PDF generation:** the assignment report is generated
  without adding third-party dependencies.

## 10. Scope and future enhancements

The current application is deliberately small. It has no persistent saves,
inventory, health, random events, external configuration, localization, or
graphical interface. The `GameIO` port provides a seam for a future interface,
and new paths can be introduced by adding domain choices/rules and wiring them
through the application.

Potential follow-up work could include branching story data, player inventory,
save/load support, richer result reporting, and more exhaustive tests for
every menu and route transition.
