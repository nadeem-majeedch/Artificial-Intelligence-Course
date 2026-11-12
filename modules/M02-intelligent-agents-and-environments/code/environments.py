"""Grid environments for M02.

Two environments, one interface:

* ``GridWorld`` - a vacuum-style grid with dirt, obstacles and an optional goal.
* ``BanditWorld`` - four levers with fixed expected payoffs, used for the
  learning-agent lesson.

Both expose ``percept()``, ``step(action)`` and ``performance``. The point of the
module is that an agent can be written against this interface without knowing
which implementation it is talking to.

Standard library only. Run ``python environments.py`` for a demonstration.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Iterable

ACTIONS = ("up", "down", "left", "right", "suck", "noop")
MOVES = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


@dataclass
class GridWorld:
    """A vacuum-style grid world.

    Attributes
    ----------
    width, height:
        Grid dimensions; coordinates are ``(x, y)`` with ``(0, 0)`` top-left.
    dirt:
        Cells that currently contain dirt. Mutated as the agent cleans.
    obstacles:
        Cells the agent cannot enter.
    goal:
        Optional target cell, used by goal-based agents.
    observable:
        ``"full"`` gives the agent the whole grid; ``"local"`` gives only the
        current cell, the walls around it, and a bump flag.
    stochastic:
        When True, each move slips with probability ``slip`` and dirt appears
        with probability ``dirt_spawn`` after each action.
    """

    width: int = 4
    height: int = 4
    dirt: set[tuple[int, int]] = field(default_factory=lambda: {(1, 1), (3, 2)})
    obstacles: set[tuple[int, int]] = field(default_factory=set)
    goal: tuple[int, int] | None = None
    observable: str = "full"
    stochastic: bool = False
    slip: float = 0.2
    dirt_spawn: float = 0.05
    seed: int = 0

    position: tuple[int, int] = (0, 0)
    cleaned: int = 0
    moves_made: int = 0
    bumps: int = 0
    steps: int = 0
    last_bump: bool = False
    _rng: random.Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)
        self.dirt = set(self.dirt)

    # ------------------------------------------------------------------ sensing
    def _walls(self) -> tuple[bool, bool, bool, bool]:
        """Return (north, south, west, east) wall flags for the current cell."""
        x, y = self.position
        blocked = lambda p: p in self.obstacles or not (0 <= p[0] < self.width and 0 <= p[1] < self.height)
        return (
            blocked((x, y - 1)),
            blocked((x, y + 1)),
            blocked((x - 1, y)),
            blocked((x + 1, y)),
        )

    def percept(self) -> tuple:
        """Return the current percept for the agent."""
        if self.observable == "full":
            return ("full", self.position, frozenset(self.dirt), frozenset(self.obstacles))
        return ("local", self.position, self.position in self.dirt, self._walls(), self.last_bump)

    @property
    def done(self) -> bool:
        """True when no dirt remains."""
        return not self.dirt

    @property
    def performance(self) -> int:
        """Cumulative score: +10 per cleaned cell, -1 per move, -2 per bump."""
        return 10 * self.cleaned - self.moves_made - 2 * self.bumps

    # ------------------------------------------------------------------ acting
    def step(self, action: str) -> int:
        """Apply `action`, return the immediate reward, and advance one step."""
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action!r}")
        self.steps += 1
        self.last_bump = False
        reward = 0

        if action == "suck":
            if self.position in self.dirt:
                self.dirt.remove(self.position)
                self.cleaned += 1
                reward += 10
        elif action == "noop":
            pass
        else:
            move = MOVES[action]
            if self.stochastic and self._rng.random() < self.slip:
                move = MOVES[self._rng.choice(("up", "down", "left", "right"))]
            target = (self.position[0] + move[0], self.position[1] + move[1])
            if target in self.obstacles or not (0 <= target[0] < self.width and 0 <= target[1] < self.height):
                self.bumps += 1
                self.last_bump = True
                reward -= 2
            else:
                self.position = target
                self.moves_made += 1
                reward -= 1

        if self.stochastic and self._rng.random() < self.dirt_spawn:
            free = [
                (x, y)
                for x in range(self.width)
                for y in range(self.height)
                if (x, y) not in self.obstacles and (x, y) != self.position
            ]
            if free:
                self.dirt.add(self._rng.choice(free))

        return reward

    def reset(self, dirt: Iterable[tuple[int, int]] | None = None) -> None:
        """Return to the start state, restoring `dirt` if given."""
        self.position = (0, 0)
        self.cleaned = 0
        self.moves_made = 0
        self.bumps = 0
        self.steps = 0
        self.last_bump = False
        if dirt is not None:
            self.dirt = set(dirt)


@dataclass
class BanditWorld:
    """Four levers with fixed expected payoffs and Gaussian noise.

    Used in L02-05 to show what a learning element does: the agent does not know
    the payoffs, only what it has observed.
    """

    payoffs: tuple[float, ...] = (1.0, 3.0, 0.5, 2.0)
    noise: float = 0.5
    seed: int = 0
    pulls: list[int] = field(default_factory=list)
    total: float = 0.0
    _rng: random.Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def pull(self, lever: int) -> float:
        """Pull `lever` and return the noisy reward."""
        if not 0 <= lever < len(self.payoffs):
            raise ValueError("lever out of range")
        reward = self._rng.gauss(self.payoffs[lever], self.noise)
        self.pulls.append(lever)
        self.total += reward
        return reward

    @property
    def performance(self) -> float:
        """Total reward accumulated so far."""
        return self.total


if __name__ == "__main__":
    world = GridWorld(width=3, height=3, dirt={(1, 1), (2, 2)}, seed=1)
    print("start:", world.percept())
    total = 0
    for action in ("right", "down", "suck", "right", "down", "suck"):
        reward = world.step(action)
        total += reward
        print(f"{action:6s} reward={reward:3d} total={total:3d} dirt_left={len(world.dirt)}")
    print("final performance:", world.performance)
