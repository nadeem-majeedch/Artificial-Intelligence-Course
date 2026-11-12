"""Capability scoring for described AI systems.

Companion code for M01 (L01-01) and LAB-01-01. Standard library only.

Run directly to score the reference systems:

    python capability_check.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class System:
    """A described system, scored on four capability flags."""

    name: str
    perceives: bool
    decides: bool
    adapts: bool
    goal_directed: bool

    @property
    def score(self) -> int:
        """Number of capability flags set, an integer in 0..4."""
        return sum([self.perceives, self.decides, self.adapts, self.goal_directed])

    def verdict(self) -> str:
        """Short verdict derived from the score and the adaptation flag."""
        if self.score <= 1:
            return "automation, not really AI"
        if self.score == 2:
            return "borderline - often sold as AI"
        if self.adapts:
            return "AI: learning system"
        return "AI: hand-written rules"


REFERENCE_SYSTEMS = [
    System("thermostat", True, True, False, True),
    System("spreadsheet SUM", False, True, False, False),
    System("spam filter", True, True, True, True),
    System("chess engine", True, True, False, True),
]


def table(systems: list[System]) -> str:
    """Render systems as a fixed-width table."""
    lines = [f"{'system':16s} {'score':>5s}  verdict"]
    for system in systems:
        lines.append(f"{system.name:16s} {system.score:5d}  {system.verdict()}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(table(REFERENCE_SYSTEMS))
