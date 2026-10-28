"""Generate a one-page PDF describing Copilot's contribution to the game."""

from pathlib import Path
import textwrap


REPORT_LINES = [
    "PYTHON ADVENTURE GAME",
    "GitHub Copilot Assistance Report",
    "",
    "Project: Assesment-PythonAdventureGame",
    "",
    "PROJECT SUMMARY",
    "A replayable command-line quest in which the player chooses between a dark",
    "forest and a mysterious cave, makes follow-up decisions, and seeks treasure.",
    "",
    "HOW COPILOT ASSISTED",
    "Copilot-assisted development helped shape the branching story, separate",
    "domain rules from CLI interaction, define the application port, and draft",
    "automated tests. Suggestions were reviewed against the requirements and",
    "verified by running the test suite; the implementation remains dependency-",
    "free and uses a lightweight Clean Architecture structure.",
    "",
    "IMPLEMENTATION PLAN",
    "1. Put outcomes, choice models, and pure path rules in the domain layer.",
    "2. Define a GameIO protocol in the application layer.",
    "3. Coordinate rounds, paths, and replay in a game application use case.",
    "4. Implement terminal prompts and validation in a console adapter.",
    "5. Wire the adapter and application in the root entry-point module.",
    "",
    "CHALLENGES AND RESOLUTIONS",
    "Branching scenarios can be difficult to test when story rules and terminal",
    "input/output are mixed together. The domain now decides outcomes without",
    "calling the CLI, while the application depends on a GameIO protocol and",
    "the console adapter owns input validation. A fake adapter exercises the",
    "use case without manual keyboard input.",
    "",
    "ENHANCEMENTS TO THE BASIC OUTLINE",
    "- Added a second decision in each route so choices have meaningful outcomes.",
    "- Added numbered and text-based selections, plus invalid-choice recovery.",
    "- Added a default name for blank input and replay after wins or losses.",
    "- Introduced domain, application, and adapter boundaries with dependency",
    "  direction pointing inward to the application/domain.",
    "- Added automated tests for pure rules, both winning paths, and replay.",
    "- Kept the project standard-library-only for simple setup and submission.",
    "",
    "VALIDATION AND RUNNING",
    "The project is tested with: python -m unittest -v",
    "Start the game with: python adventure_game.py",
    "The automated suite covers domain rules, application flows, and CLI input.",
    "",
    "Copilot was used as a development assistant; the player-facing story and",
    "final code were reviewed and verified by running the project's tests.",
]


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def create_pdf(lines: list[str]) -> bytes:
    commands = ["BT", "/F1 9 Tf", "50 755 Td"]
    for index, line in enumerate(lines):
        if index:
            commands.append("0 -13 Td")
        if line:
            commands.append(f"({escape_pdf_text(line)}) Tj")
    commands.append("ET")
    stream = "\n".join(commands).encode("latin-1")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n"
        + stream
        + b"\nendstream",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, body in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{number} 0 obj\n".encode("ascii"))
        pdf.extend(body)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(pdf)


def main() -> None:
    lines: list[str] = []
    for line in REPORT_LINES:
        if not line:
            lines.append("")
        else:
            lines.extend(textwrap.wrap(line, width=88) or [""])

    report_path = Path(__file__).parent / "reports" / "copilot_assistance_report.pdf"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_bytes(create_pdf(lines))
    print(f"PDF report saved to: {report_path}")


if __name__ == "__main__":
    main()
