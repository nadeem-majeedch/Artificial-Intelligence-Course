"""rl_envs.py -- Markov decision processes and Gymnasium environments for M10.

Contents
--------
GridMDP                tabular gridworld as an *explicit* MDP (transition model known)
make_gridworld         teaching gridworld: start, goal, pit, optional slip and step cost
cliff_walk             Sutton & Barto's 4 x 12 cliff-walking task
MDPAdapter             exposes a GridMDP through the Gymnasium reset/step API
RobotNavEnv            2-D point-robot navigation with obstacles (continuous state)
TrafficSignalEnv       two-phase traffic-signal control at one intersection
ResourceAllocationEnv  water-budget allocation between two users (resource allocation)

Every environment is deterministic under a seed, runs on a CPU, and needs only
NumPy and Gymnasium. None of them renders with pygame: pictures are drawn from the
state by ``viz.py``, so ``render_mode`` is never required.

Run ``python rl_envs.py`` for a consistency check of all five environments.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

try:  # Gymnasium is only needed by the three continuous/queueing environments
    import gymnasium as gym
    from gymnasium import spaces
except ImportError:  # pragma: no cover - documented fallback
    gym = None
    spaces = None


# ---------------------------------------------------------------------------
# Explicit tabular MDP
# ---------------------------------------------------------------------------

#: action index -> (row delta, column delta, arrow)
ACTIONS: tuple[tuple[int, int, str], ...] = (
    (-1, 0, "^"),
    (0, 1, ">"),
    (1, 0, "v"),
    (0, -1, "<"),
)
ACTION_NAMES = ("up", "right", "down", "left")


@dataclass
class GridMDP:
    """A gridworld with an explicitly enumerable transition function.

    ``grid`` is a list of equal-length strings. Characters:

    ``.`` free cell, ``S`` start, ``G`` goal (+1, terminal),
    ``P`` pit (-1, terminal), ``#`` wall, ``C`` cliff (-100, terminal).
    """

    grid: list[str]
    slip: float = 0.0
    step_cost: float = 0.0
    goal_reward: float = 1.0
    pit_reward: float = -1.0
    cliff_reward: float = -100.0
    start: tuple[int, int] | None = None
    name: str = "gridworld"

    cells: dict[tuple[int, int], str] = field(init=False, repr=False)
    index: dict[tuple[int, int], int] = field(init=False, repr=False)
    coords: list[tuple[int, int]] = field(init=False)
    terminal: set[int] = field(init=False)

    def __post_init__(self) -> None:
        width = len(self.grid[0])
        if any(len(row) != width for row in self.grid):
            raise ValueError("all grid rows must have the same length")
        self.cells = {}
        for r, row in enumerate(self.grid):
            for c, ch in enumerate(row):
                if ch == "#":
                    continue
                self.cells[(r, c)] = ch
                if ch == "S" and self.start is None:
                    self.start = (r, c)
        if self.start is None:
            raise ValueError("grid needs an 'S' start cell")
        self.coords = sorted(self.cells)
        self.index = {rc: i for i, rc in enumerate(self.coords)}
        self.terminal = {
            self.index[rc] for rc, ch in self.cells.items() if ch in "GPC"
        }

    # -- basic MDP structure ------------------------------------------------
    @property
    def n_states(self) -> int:
        return len(self.coords)

    @property
    def n_actions(self) -> int:
        return len(ACTIONS)

    def is_terminal(self, s: int) -> bool:
        return s in self.terminal

    def state_coord(self, s: int) -> tuple[int, int]:
        return self.coords[s]

    def start_state(self) -> int:
        return self.index[self.start]

    def reward_of(self, s: int) -> float:
        ch = self.cells[self.coords[s]]
        if ch == "G":
            return self.goal_reward
        if ch == "P":
            return self.pit_reward
        if ch == "C":
            return self.cliff_reward
        return 0.0

    def _move(self, rc: tuple[int, int], action: int) -> tuple[int, int]:
        dr, dc, _ = ACTIONS[action]
        nr, nc = rc[0] + dr, rc[1] + dc
        return (nr, nc) if (nr, nc) in self.cells else rc  # walls block, no move

    def transitions(self, s: int, a: int) -> dict[int, float]:
        """Return ``{next_state: probability}`` for the given state and action.

        Terminal states have no outgoing actions; an empty dict is returned.
        """
        if self.is_terminal(s):
            return {}
        rc = self.coords[s]
        if self.slip == 0.0:
            return {self.index[self._move(rc, a)]: 1.0}
        left, right = (a - 1) % 4, (a + 1) % 4
        out: dict[int, float] = {}
        for act, p in ((a, 1.0 - self.slip), (left, self.slip / 2), (right, self.slip / 2)):
            s2 = self.index[self._move(rc, act)]
            out[s2] = out.get(s2, 0.0) + p
        return out

    def reward(self, s: int, a: int, s2: int) -> float:
        """Reward for one transition: entering a terminal cell pays its reward."""
        if self.is_terminal(s2):
            return self.reward_of(s2)
        return self.step_cost

    def sample(self, s: int, a: int, rng: np.random.Generator) -> tuple[int, float]:
        trans = self.transitions(s, a)
        states = list(trans)
        probs = np.array([trans[k] for k in states], dtype=float)
        s2 = int(rng.choice(states, p=probs / probs.sum()))
        return s2, self.reward(s, a, s2)

    # -- rendering ----------------------------------------------------------
    def ascii_map(self) -> str:
        return "\n".join("".join(self.cells.get((r, c), "#") for c in range(len(row)))
                         for r, row in enumerate(self.grid))

    def render_policy(self, policy: np.ndarray) -> str:
        """ASCII picture of a deterministic policy (arrows) with state values."""
        lines = []
        for r, row in enumerate(self.grid):
            parts = []
            for c in range(len(row)):
                if (r, c) not in self.index:
                    parts.append("  ##  ")
                    continue
                s = self.index[(r, c)]
                if self.is_terminal(s):
                    parts.append(f"  {self.cells[(r, c)]}   ")
                else:
                    parts.append(f"  {ACTIONS[int(policy[s])][2]}   ")
            lines.append("".join(parts))
        return "\n".join(lines)


def make_gridworld(
    kind: str = "open",
    slip: float = 0.0,
    step_cost: float = 0.0,
) -> GridMDP:
    """Return one of the module's teaching gridworlds.

    ``open``  5x5, start top-left, goal bottom-right, pit in the centre.
    ``maze``  5x5 with walls, so the shortest path needs three turns.
    """
    if kind == "open":
        grid = ["S....", ".....", "..P..", ".....", "....G"]
        return GridMDP(grid, slip=slip, step_cost=step_cost, name="open-5x5")
    if kind == "maze":
        grid = ["S.#..", ".#.#.", ".#..#", "...#.", "#...G"]
        return GridMDP(grid, slip=slip, step_cost=step_cost, name="maze-5x5")
    raise ValueError(f"unknown gridworld kind: {kind!r}")


def cliff_walk(step_cost: float = -1.0) -> GridMDP:
    """Sutton & Barto (2018) figure 6.4: 4 rows x 12 columns, cliff along the bottom.

    Start bottom-left, goal bottom-right. Every step costs -1 and stepping into
    the cliff costs -100 and ends the episode.
    """
    grid = [
        "............",
        "............",
        "............",
        "SCCCCCCCCCCG",
    ]
    return GridMDP(
        grid,
        slip=0.0,
        step_cost=step_cost,
        cliff_reward=-100.0,
        goal_reward=0.0,
        name="cliff-walking",
    )


# ---------------------------------------------------------------------------
# Gymnasium-compatible wrapper for a tabular MDP
# ---------------------------------------------------------------------------

class MDPAdapter:
    """Expose a :class:`GridMDP` through ``reset``/``step`` like a Gymnasium env."""

    def __init__(self, mdp: GridMDP, max_steps: int = 200):
        self.mdp = mdp
        self.max_steps = max_steps
        self.s = mdp.start_state()
        self.t = 0
        self.rng = np.random.default_rng(0)

    # Gymnasium-style metadata
    @property
    def observation_space(self):
        return spaces.Discrete(self.mdp.n_states) if spaces else None

    @property
    def action_space(self):
        return spaces.Discrete(self.mdp.n_actions) if spaces else None

    def reset(self, *, seed: int | None = None, options=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.s = self.mdp.start_state()
        self.t = 0
        return self.s, {}

    def step(self, action: int):
        s2, r = self.mdp.sample(self.s, action, self.rng)
        self.s = s2
        self.t += 1
        terminated = self.mdp.is_terminal(s2)
        truncated = self.t >= self.max_steps and not terminated
        return s2, r, terminated, truncated, {}


# ---------------------------------------------------------------------------
# Gymnasium environments
# ---------------------------------------------------------------------------

class RobotNavEnv(gym.Env if gym else object):
    """A point robot that must reach a goal while avoiding two rectangular obstacles.

    State: ``(x, y)`` position in ``[0, size]^2`` plus the vector to the goal, so the
    observation is 4-dimensional and *continuous*. Actions are the four compass
    moves plus a no-op. Sparse reward by default; ``shaping=True`` adds
    potential-based shaping ``F = gamma * phi(s') - phi(s)`` with
    ``phi(s) = -distance_to_goal``, which provably leaves the optimal policy
    unchanged (Ng, Harada & Russell, 1999).
    """

    metadata = {"render_modes": []}

    def __init__(self, size: float = 5.0, step_len: float = 0.4, shaping: bool = False,
                 gamma: float = 0.99, max_steps: int = 80):
        if not gym:
            raise ImportError("RobotNavEnv needs gymnasium: python -m pip install gymnasium")
        super().__init__()
        self.size = float(size)
        self.step_len = float(step_len)
        self.shaping = bool(shaping)
        self.gamma = float(gamma)
        self.max_steps = int(max_steps)
        self.goal = np.array([4.3, 4.3], dtype=np.float32)
        # obstacles as (x0, y0, x1, y1)
        self.obstacles = np.array(
            [[1.2, 0.0, 2.0, 2.8], [2.8, 2.2, 3.6, 5.0]], dtype=np.float32
        )
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(-10.0, 10.0, shape=(4,), dtype=np.float32)
        self._pos = np.zeros(2, dtype=np.float32)
        self._t = 0
        self._prev_potential = 0.0
        self._rng = np.random.default_rng(0)

    # -- helpers ------------------------------------------------------------
    def potential(self, pos=None) -> float:
        pos = self._pos if pos is None else pos
        return -float(np.linalg.norm(self.goal - pos))

    def _obs(self) -> np.ndarray:
        return np.concatenate([self._pos, self.goal - self._pos]).astype(np.float32)

    def _blocked(self, pos: np.ndarray) -> bool:
        if np.any(pos < 0.0) or np.any(pos > self.size):
            return True
        for x0, y0, x1, y1 in self.obstacles:
            if x0 <= pos[0] <= x1 and y0 <= pos[1] <= y1:
                return True
        return False

    # -- Gymnasium API ------------------------------------------------------
    def reset(self, *, seed: int | None = None, options=None):
        if seed is not None:
            self._rng = np.random.default_rng(seed)
        jitter = self._rng.uniform(0.0, 0.3, size=2)
        self._pos = np.array([0.3, 0.3], dtype=np.float32) + jitter.astype(np.float32)
        self._t = 0
        self._prev_potential = self.potential()
        return self._obs(), {}

    def step(self, action: int):
        delta = np.array([[0, 0], [0, self.step_len], [self.step_len, 0],
                          [0, -self.step_len], [-self.step_len, 0]], dtype=np.float32)[int(action)]
        candidate = self._pos + delta
        collision = self._blocked(candidate)
        if not collision:
            self._pos = candidate
        self._t += 1
        dist = float(np.linalg.norm(self.goal - self._pos))
        terminated = dist < 0.35
        truncated = self._t >= self.max_steps and not terminated
        reward = -0.02 + (10.0 if terminated else 0.0)
        if collision:
            reward -= 0.5
        if self.shaping:
            potential = self.potential()
            reward += self.gamma * potential - self._prev_potential
            self._prev_potential = potential
        return self._obs(), float(reward), bool(terminated), bool(truncated), {"dist": dist}


class TrafficSignalEnv(gym.Env if gym else object):
    """One four-way intersection, two competing directions, two signal phases.

    State ``(q_ns, q_ew, phase)`` with queues capped at ``max_queue`` and phase in
    ``{0: north-south green, 1: east-west green}``. Each step ``arrivals`` new
    vehicles join each queue, then the green direction discharges ``capacity``
    vehicles. Reward is the negative total queue, so maximising return maximises
    throughput per step. A sensible baseline is a fixed-time controller that
    switches phase every ``fixed_interval`` steps.
    """

    metadata = {"render_modes": []}

    def __init__(self, max_queue: int = 6, capacity: int = 2, arrival_mean: float = 1.2,
                 horizon: int = 200, switch_penalty: float = 0.0):
        if not gym:
            raise ImportError("TrafficSignalEnv needs gymnasium")
        super().__init__()
        self.max_queue = int(max_queue)
        self.capacity = int(capacity)
        self.arrival_mean = float(arrival_mean)
        self.horizon = int(horizon)
        self.switch_penalty = float(switch_penalty)
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.MultiDiscrete(
            [self.max_queue + 1, self.max_queue + 1, 2]
        )
        self._rng = np.random.default_rng(0)
        self.q = np.zeros(2, dtype=np.int64)
        self.phase = 0
        self._t = 0

    def _obs(self) -> np.ndarray:
        return np.array([self.q[0], self.q[1], self.phase], dtype=np.int64)

    def reset(self, *, seed: int | None = None, options=None):
        if seed is not None:
            self._rng = np.random.default_rng(seed)
        self.q = self._rng.integers(0, 4, size=2).astype(np.int64)
        self.phase = 0
        self._t = 0
        return self._obs(), {}

    def step(self, action: int):
        action = int(action)
        arrivals = self._rng.poisson(self.arrival_mean, size=2)
        self.q = np.minimum(self.q + arrivals, self.max_queue)
        served = min(self.q[action], self.capacity)
        self.q[action] -= served
        penalty = self.switch_penalty if action != self.phase else 0.0
        self.phase = action
        self._t += 1
        reward = -float(self.q.sum()) - penalty
        terminated = False
        truncated = self._t >= self.horizon
        return self._obs(), reward, terminated, truncated, {
            "served": served, "queue": int(self.q.sum())
        }


class ResourceAllocationEnv(gym.Env if gym else object):
    """Allocate a limited water budget between urban and agricultural users.

    State ``(level, season)``: reservoir level in ``0..4`` and season in
    ``{0: dry, 1: wet}``. The action is the share of the day's release given to
    urban users, in fifths (``0..4``). Demand is 2 units urban and 3 units
    agricultural per day in the dry season, 1 and 2 in the wet season. Urban
    shortfall is penalised 3x more than agricultural shortfall, and release is
    capped by the reservoir level. Inflow is 0 in the dry season and 2 in the wet
    season, so the trade-off is real: serve the city today and the farms tomorrow.
    """

    metadata = {"render_modes": []}

    def __init__(self, horizon: int = 60, max_level: int = 4, seed_level: int = 3):
        if not gym:
            raise ImportError("ResourceAllocationEnv needs gymnasium")
        super().__init__()
        self.horizon = int(horizon)
        self.max_level = int(max_level)
        self.seed_level = int(seed_level)
        self.urban_demand = {0: 2, 1: 1}
        self.agri_demand = {0: 3, 1: 2}
        self.urban_penalty = 3.0
        self.agri_penalty = 1.0
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.MultiDiscrete([self.max_level + 1, 2])
        self._rng = np.random.default_rng(0)
        self.level = self.seed_level
        self.season = 0
        self._t = 0

    def _obs(self) -> np.ndarray:
        return np.array([self.level, self.season], dtype=np.int64)

    def reset(self, *, seed: int | None = None, options=None):
        if seed is not None:
            self._rng = np.random.default_rng(seed)
        self.level = int(self._rng.integers(2, self.max_level + 1))
        self.season = int(self._rng.integers(0, 2))
        self._t = 0
        return self._obs(), {}

    def step(self, action: int):
        release = min(self.level, 4)
        urban_share = int(action) / 4.0
        urban_supply = release * urban_share
        agri_supply = release - urban_supply
        urban_short = max(0.0, self.urban_demand[self.season] - urban_supply)
        agri_short = max(0.0, self.agri_demand[self.season] - agri_supply)
        reward = -(self.urban_penalty * urban_short + self.agri_penalty * agri_short)
        inflow = 0 if self.season == 0 else 2
        self.level = int(min(self.max_level, self.level - release + inflow))
        self.season = int(self._rng.integers(0, 2))
        self._t += 1
        return self._obs(), float(reward), False, self._t >= self.horizon, {
            "urban_short": urban_short, "agri_short": agri_short
        }


# ---------------------------------------------------------------------------
# Consistency check
# ---------------------------------------------------------------------------

def _check() -> None:
    print("== GridMDP transitions ==")
    mdp = make_gridworld("open", slip=0.1, step_cost=-0.04)
    print(mdp.ascii_map())
    s = mdp.start_state()
    for a in range(4):
        trans = mdp.transitions(s, a)
        print(ACTION_NAMES[a], {mdp.state_coord(k): round(v, 3) for k, v in trans.items()},
              "reward", round(mdp.reward(s, a, next(iter(trans))), 2))
    total = sum(sum(mdp.transitions(s, a).values()) for s in range(mdp.n_states)
                for a in range(mdp.n_actions))
    print(f"states={mdp.n_states} actions={mdp.n_actions} transition mass={total:.3f}")

    print("\n== cliff-walking map ==")
    print(cliff_walk().ascii_map())

    print("\n== Gymnasium environments ==")
    envs = {
        "RobotNav": RobotNavEnv(),
        "RobotNav+shaping": RobotNavEnv(shaping=True),
        "TrafficSignal": TrafficSignalEnv(),
        "ResourceAllocation": ResourceAllocationEnv(),
    }
    for name, env in envs.items():
        obs, _ = env.reset(seed=0)
        total_r, steps = 0.0, 0
        for _ in range(200):
            obs, r, term, trunc, info = env.step(env.action_space.sample())
            total_r += r
            steps += 1
            if term or trunc:
                break
        print(f"{name:20s} obs={np.asarray(obs)} random-policy return={total_r:8.2f} "
              f"steps={steps} info={info}")

    print("\n== Gymnasium registry ==")
    ids = ["CartPole-v1", "FrozenLake-v1", "Blackjack-v1", "MountainCar-v0"]
    for env_id in ids:
        print(f"{env_id:16s} available={env_id in gym.registry}")


if __name__ == "__main__":
    _check()
