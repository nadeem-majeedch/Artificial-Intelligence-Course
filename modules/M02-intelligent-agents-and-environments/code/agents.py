"""Five agent architectures for M02.

Each agent exposes ``program(percept) -> action``, the agent function from the
textbook. Everything else - the environment, the performance measure, the
episode loop - is outside the agent, which is the point of the architecture
diagram in L02-01.

* ``RandomAgent``          - baseline; ignores the percept
* ``ReflexAgent``          - condition-action rules on the current percept
* ``ModelBasedAgent``      - keeps internal state and an explored map
* ``GoalBasedAgent``       - searches its map for the nearest known dirt
* ``UtilityBasedAgent``    - one-step lookahead scored by expected utility
* ``LearningAgent``        - improves a policy table from reward feedback

Standard library only. Run ``python agents.py`` for a comparison episode.
"""

from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass, field

from environments import ACTIONS, MOVES, GridWorld

Position = tuple[int, int]


def _neighbours(position: Position) -> dict[str, Position]:
    """Map each movement action to the adjacent cell."""
    return {action: (position[0] + delta[0], position[1] + delta[1]) for action, delta in MOVES.items()}


class RandomAgent:
    """Ignores everything and picks an action uniformly at random."""

    name = "random"

    def __init__(self, seed: int = 0) -> None:
        self._rng = random.Random(seed)

    def program(self, percept: tuple) -> str:
        return self._rng.choice(ACTIONS)


class ReflexAgent:
    """Condition-action rules that use only the current percept.

    With a local percept the rules cannot know where the agent is, so the policy
    is: suck when the current cell is dirty, otherwise sweep in a fixed cycle.
    This is the architecture's defining weakness - no memory, no map.
    """

    name = "reflex"

    def __init__(self) -> None:
        self._cycle = ("right", "down", "left", "up")
        self._index = 0

    def program(self, percept: tuple) -> str:
        kind = percept[0]
        if kind == "local":
            _, _position, dirty, _walls, _bump = percept
        else:  # full observability: the agent can see whether its cell is dirty
            _, position, dirt, _obstacles = percept
            dirty = position in dirt
        if dirty:
            return "suck"
        action = self._cycle[self._index % len(self._cycle)]
        self._index += 1
        return action


class ModelBasedAgent:
    """Keeps internal state: where it is, what it has seen, what it has cleaned.

    The agent maintains a belief map built only from percepts. It moves toward the
    nearest cell it has not yet visited, which is a simple exploration policy -
    not a planner, and deliberately so.
    """

    name = "model-based"

    def __init__(self, width: int = 4, height: int = 4) -> None:
        self.width, self.height = width, height
        self.position: Position = (0, 0)
        self.visited: set[Position] = {(0, 0)}
        self.known_dirt: set[Position] = set()
        self.obstacles: set[Position] = set()
        self.walls: dict[Position, tuple[bool, bool, bool, bool]] = {}

    def update(self, percept: tuple) -> None:
        """Fold a percept into the agent's internal state."""
        if percept[0] == "full":
            _, position, dirt, obstacles = percept
            self.position = position
            self.visited.add(position)
            self.known_dirt = set(dirt)
            self.obstacles = set(obstacles)
            return
        _, position, dirty, walls, _bump = percept
        self.position = position
        self.visited.add(position)
        self.walls[position] = walls
        if dirty:
            self.known_dirt.add(position)
        else:
            self.known_dirt.discard(position)

    def _free(self, cell: Position) -> bool:
        """True when `cell` is inside the grid."""
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def _can_move(self, cell: Position, neighbour: Position) -> bool:
        """True when the believed map allows a move from `cell` to `neighbour`.

        Unknown cells are assumed passable: the agent corrects the belief when a
        bump tells it otherwise, which is what makes the internal state useful.
        """
        if not self._free(neighbour) or neighbour in self.obstacles:
            return False
        walls = self.walls.get(cell)
        if walls is None:
            return True
        delta = (neighbour[0] - cell[0], neighbour[1] - cell[1])
        index = {(0, -1): 0, (0, 1): 1, (-1, 0): 2, (1, 0): 3}.get(delta)
        return True if index is None else not walls[index]

    def program(self, percept: tuple) -> str:
        self.update(percept)
        if self.position in self.known_dirt:
            return "suck"
        return self._towards_unvisited()

    def _towards_unvisited(self) -> str:
        """Breadth-first search over the believed map to the nearest unvisited cell."""
        start = self.position
        queue: deque[tuple[Position, str]] = deque()
        seen = {start}
        for action, neighbour in _neighbours(start).items():
            if neighbour not in seen and self._can_move(start, neighbour):
                queue.append((neighbour, action))
                seen.add(neighbour)
        while queue:
            cell, first_action = queue.popleft()
            if cell not in self.visited:
                return first_action
            for action, neighbour in _neighbours(cell).items():
                if neighbour not in seen and self._can_move(cell, neighbour):
                    seen.add(neighbour)
                    queue.append((neighbour, first_action))
        return "noop"


class GoalBasedAgent(ModelBasedAgent):
    """Plans to the nearest *known* dirty cell, then cleans it.

    The goal is explicit - remove all dirt - and the agent searches for a path to
    the subgoal. With full observability the map is given, which isolates the
    planning behaviour from the exploration behaviour.
    """

    name = "goal-based"

    def program(self, percept: tuple) -> str:
        if percept[0] == "full":
            _, position, dirt, obstacles = percept
            self.position = position
            self.walls = {}
            self.known_dirt = set(dirt)
            self.obstacles = set(obstacles)
        else:
            self.update(percept)
            self.obstacles = set()
        if self.position in self.known_dirt:
            return "suck"
        if not self.known_dirt:
            # No goal is known yet: explore, exactly as the model-based agent does.
            return self._towards_unvisited()
        return self._towards_nearest_dirt()

    def _towards_nearest_dirt(self) -> str:
        if not self.known_dirt:
            return "noop"
        start = self.position
        queue: deque[tuple[Position, str]] = deque()
        seen = {start}
        for action, neighbour in _neighbours(start).items():
            if self._passable(neighbour):
                queue.append((neighbour, action))
                seen.add(neighbour)
        while queue:
            cell, first_action = queue.popleft()
            if cell in self.known_dirt:
                return first_action
            for action, neighbour in _neighbours(cell).items():
                if neighbour not in seen and self._passable(neighbour):
                    seen.add(neighbour)
                    queue.append((neighbour, first_action))
        return "noop"

    def _passable(self, position: Position) -> bool:
        x, y = position
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return position not in getattr(self, "obstacles", set())


class UtilityBasedAgent(GoalBasedAgent):
    """Chooses the action with the highest expected utility one step ahead.

    Utility combines the immediate reward with a distance penalty, so the agent
    prefers cleaning now over travelling, and prefers short journeys over long
    ones. Weights are explicit because a utility function that is not written
    down cannot be argued with.
    """

    name = "utility-based"

    def __init__(self, width: int = 4, height: int = 4, travel_cost: float = 0.4) -> None:
        super().__init__(width, height)
        self.travel_cost = travel_cost

    def program(self, percept: tuple) -> str:
        if percept[0] == "full":
            _, position, dirt, obstacles = percept
            self.position, self.known_dirt, self.obstacles = position, set(dirt), set(obstacles)
        else:
            self.update(percept)
            self.obstacles = set()

        if not self.known_dirt:
            return self._towards_unvisited()

        best_action, best_utility = "noop", float("-inf")
        for action, neighbour in _neighbours(self.position).items():
            if not self._passable(neighbour):
                continue
            utility = 10.0 if neighbour in self.known_dirt else 0.0
            distance = self._distance_to_dirt(neighbour)
            utility -= self.travel_cost * distance
            if utility > best_utility:
                best_action, best_utility = action, utility

        if self.position in self.known_dirt and best_utility < 10.0:
            return "suck"
        return best_action

    def _distance_to_dirt(self, start: Position) -> float:
        """Manhattan distance to the nearest known dirt cell (or 0 if none)."""
        if not self.known_dirt:
            return 0.0
        return min(abs(start[0] - p[0]) + abs(start[1] - p[1]) for p in self.known_dirt)


class LearningAgent:
    """A performance element plus a learning element, sharing one table.

    The table maps a state key to action values. After each step the critic turns
    the reward into an update, and the learning element revises the table. With
    ``epsilon=0`` the agent exploits what it has learned; the comparison in
    L02-05 shows the improvement across episodes.
    """

    name = "learning"

    def __init__(self, alpha: float = 0.3, gamma: float = 0.9, epsilon: float = 0.2, seed: int = 0) -> None:
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q: dict[tuple, dict[str, float]] = {}
        self._rng = random.Random(seed)
        self._last: tuple[tuple, str] | None = None

    # ---------------------------------------------------------------- learning
    def _values(self, state: tuple) -> dict[str, float]:
        if state not in self.q:
            self.q[state] = {action: 0.0 for action in ("up", "down", "left", "right", "suck")}
        return self.q[state]

    def _state(self, percept: tuple) -> tuple:
        """A compact state key the table can generalise over."""
        return (percept[0], percept[1], percept[2] if percept[0] == "local" else None)

    def observe(self, percept: tuple, reward: float) -> None:
        """Critic + learning element: revise the last decision using the new percept."""
        if self._last is None:
            return
        state, action = self._last
        next_state = self._state(percept)
        target = reward + self.gamma * max(self._values(next_state).values())
        values = self._values(state)
        values[action] += self.alpha * (target - values[action])

    # -------------------------------------------------------------- behaviour
    def program(self, percept: tuple) -> str:
        state = self._state(percept)
        values = self._values(state)
        if self._rng.random() < self.epsilon:
            action = self._rng.choice(list(values))
        else:
            action = max(values, key=values.get)
        self._last = (state, action)
        return action


def run_episode(agent, world: GridWorld, max_steps: int = 60, learn: bool = False) -> dict:
    """Run one episode and return a small performance record."""
    world.reset()
    for _ in range(max_steps):
        percept = world.percept()
        action = agent.program(percept)
        reward = world.step(action)
        if learn:
            agent.observe(world.percept(), reward)
        if world.done:
            break
    return {
        "agent": getattr(agent, "name", type(agent).__name__),
        "steps": world.steps,
        "cleaned": world.cleaned,
        "performance": world.performance,
    }


if __name__ == "__main__":
    world = GridWorld(width=4, height=4, dirt={(1, 1), (3, 2)}, seed=1)
    for factory in (RandomAgent, ReflexAgent, ModelBasedAgent, GoalBasedAgent, UtilityBasedAgent):
        world.reset(dirt={(1, 1), (3, 2)})
        result = run_episode(factory(), world)
        print(f"{result['agent']:14s} steps={result['steps']:3d} cleaned={result['cleaned']} score={result['performance']}")
