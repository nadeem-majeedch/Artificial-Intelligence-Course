"""dqn.py -- deep reinforcement learning on CartPole (M10, L10-05 and L10-06).

Four agents, all small enough to train on a CPU in a few minutes:

    train_dqn        Deep Q-Network with a replay buffer and a target network
    reinforce        vanilla policy gradient with returns-to-go
    actor_critic     one-step/n-step advantage actor-critic (A2C with GAE-lite)
    ppo              proximal policy optimisation with a clipped surrogate

Shared helpers: ``QNet``/``PolicyNet``/``ActorCritic``, ``ReplayBuffer``,
``epsilon_schedule``, ``evaluate``, ``episodes_to``, ``smooth``.

Run ``python dqn.py`` for the timings and learning curves quoted in the lessons
and in LAB-10-03. It prints, for every agent, the return curve summary, the
number of environment steps used and the episodes needed to reach the CartPole
solved threshold (mean return 195 over 20 episodes).
"""

from __future__ import annotations

import copy
import time
from collections import deque

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------------------------------------------------------------------------
# Networks
# ---------------------------------------------------------------------------

class QNet(nn.Module):
    """Action-value network: observation -> one Q value per action."""

    def __init__(self, obs_dim: int, n_actions: int, hidden: int = 64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, n_actions),
        )

    def forward(self, x):
        return self.net(x)


class PolicyNet(nn.Module):
    """Categorical policy: observation -> action logits."""

    def __init__(self, obs_dim: int, n_actions: int, hidden: int = 64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
            nn.Linear(hidden, n_actions),
        )

    def forward(self, x):
        return self.net(x)

    def act(self, obs: np.ndarray, generator: torch.Generator | None = None):
        logits = self(torch.as_tensor(obs, dtype=torch.float32))
        dist = torch.distributions.Categorical(logits=logits)
        a = dist.sample() if generator is None else torch.multinomial(
            torch.softmax(logits, -1), 1, generator=generator).squeeze(-1)
        return int(a.item()), float(dist.log_prob(a).item())


class ActorCritic(nn.Module):
    """Shared trunk with a policy head and a value head."""

    def __init__(self, obs_dim: int, n_actions: int, hidden: int = 64):
        super().__init__()
        self.trunk = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
        )
        self.pi = nn.Linear(hidden, n_actions)
        self.v = nn.Linear(hidden, 1)

    def forward(self, x):
        h = self.trunk(x)
        return self.pi(h), self.v(h).squeeze(-1)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

class ReplayBuffer:
    """Fixed-size experience buffer."""

    def __init__(self, capacity: int = 50_000, obs_dim: int = 4):
        self.capacity = capacity
        self.obs = np.zeros((capacity, obs_dim), dtype=np.float32)
        self.next_obs = np.zeros((capacity, obs_dim), dtype=np.float32)
        self.action = np.zeros(capacity, dtype=np.int64)
        self.reward = np.zeros(capacity, dtype=np.float32)
        self.done = np.zeros(capacity, dtype=np.float32)
        self.pos = 0
        self.size = 0

    def add(self, obs, action, reward, next_obs, done):
        i = self.pos
        self.obs[i] = obs
        self.action[i] = action
        self.reward[i] = reward
        self.next_obs[i] = next_obs
        self.done[i] = float(done)
        self.pos = (self.pos + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)

    def sample(self, batch: int, rng: np.random.Generator):
        idx = rng.integers(0, self.size, size=batch)
        return (
            torch.as_tensor(self.obs[idx]),
            torch.as_tensor(self.action[idx]),
            torch.as_tensor(self.reward[idx]),
            torch.as_tensor(self.next_obs[idx]),
            torch.as_tensor(self.done[idx]),
        )


def epsilon_schedule(step: int, start: float = 1.0, end: float = 0.05,
                     decay_steps: int = 5_000) -> float:
    """Linear decay from ``start`` to ``end`` over ``decay_steps`` environment steps."""
    if step >= decay_steps:
        return float(end)
    frac = step / max(1, decay_steps)
    return float(start + frac * (end - start))


def smooth(x, window: int = 20) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if len(x) < window:
        return x.copy()
    return np.convolve(x, np.ones(window) / window, mode="valid")


def episodes_to(curve, threshold: float = 195.0, window: int = 20) -> int | None:
    """First episode whose trailing-window mean reaches ``threshold``."""
    c = np.asarray(curve, dtype=float)
    for i in range(window, len(c) + 1):
        if np.mean(c[max(0, i - window):i]) >= threshold:
            return i
    return None


def evaluate(net, env_id: str = "CartPole-v1", episodes: int = 20, seed: int = 10_000,
             greedy_actions: bool = True, max_steps: int = 500) -> float:
    """Mean return of a trained network (greedy for Q nets, sampled for policies)."""
    env = gym.make(env_id)
    returns = []
    for k in range(episodes):
        obs, _ = env.reset(seed=seed + k)
        total = 0.0
        for _ in range(max_steps):
            with torch.no_grad():
                out = net(torch.as_tensor(obs, dtype=torch.float32))
            if isinstance(out, tuple):        # actor-critic
                logits = out[0]
            else:
                logits = out
            if greedy_actions:
                a = int(torch.argmax(logits).item())
            else:
                a = int(torch.distributions.Categorical(logits=logits).sample().item())
            obs, r, term, trunc, _ = env.step(a)
            total += float(r)
            if term or trunc:
                break
        returns.append(total)
    env.close()
    return float(np.mean(returns))


# ---------------------------------------------------------------------------
# Deep Q-learning
# ---------------------------------------------------------------------------

def train_dqn(
    env_id: str = "CartPole-v1",
    episodes: int = 400,
    gamma: float = 0.99,
    lr: float = 1e-3,
    batch_size: int = 64,
    capacity: int = 50_000,
    target_update: int = 250,
    eps_start: float = 1.0,
    eps_end: float = 0.05,
    eps_decay_steps: int = 4_000,
    hidden: int = 64,
    double: bool = False,
    seed: int = 0,
    max_steps: int = 500,
    learn_start: int = 500,
    update_every: int = 2,
) -> dict:
    """Train a DQN (or Double DQN) and return its curves and network.

    The update is ``Q(s,a) <- r + gamma * max_a' Q_target(s',a')`` for DQN and
    ``r + gamma * Q_target(s', argmax_a' Q(s',a'))`` for Double DQN. Targets are
    cut at terminal transitions only: a truncated episode still bootstraps.
    """
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    env = gym.make(env_id)
    obs_dim = int(np.prod(env.observation_space.shape))
    n_actions = int(env.action_space.n)

    net = QNet(obs_dim, n_actions, hidden)
    target = copy.deepcopy(net)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    buffer = ReplayBuffer(capacity, obs_dim)

    returns, losses, eps_hist = [], [], []
    step = 0
    for ep in range(episodes):
        obs, _ = env.reset(seed=seed * 10_000 + ep)
        total = 0.0
        for _ in range(max_steps):
            eps = epsilon_schedule(step, eps_start, eps_end, eps_decay_steps)
            if rng.random() < eps:
                a = int(rng.integers(n_actions))
            else:
                with torch.no_grad():
                    a = int(torch.argmax(net(torch.as_tensor(obs, dtype=torch.float32))).item())
            obs2, r, term, trunc, _ = env.step(a)
            buffer.add(obs, a, r, obs2, term)
            obs = obs2
            total += float(r)
            step += 1
            eps_hist.append(eps)

            if buffer.size >= max(learn_start, batch_size) and step % update_every == 0:
                b_obs, b_act, b_rew, b_next, b_done = buffer.sample(batch_size, rng)
                with torch.no_grad():
                    if double:
                        next_q_online = net(b_next).argmax(dim=1, keepdim=True)
                        next_q = target(b_next).gather(1, next_q_online).squeeze(1)
                    else:
                        next_q = target(b_next).max(dim=1).values
                    y = b_rew + gamma * (1.0 - b_done) * next_q
                q = net(b_obs).gather(1, b_act.unsqueeze(1)).squeeze(1)
                loss = F.smooth_l1_loss(q, y)
                opt.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(net.parameters(), 10.0)
                opt.step()
                losses.append(float(loss.item()))
                if step % target_update == 0:
                    target.load_state_dict(net.state_dict())
            if term or trunc:
                break
        returns.append(total)
    env.close()
    return {
        "returns": np.array(returns),
        "losses": np.array(losses),
        "eps": np.array(eps_hist),
        "net": net,
        "steps": step,
        "final_eval": evaluate(net, env_id),
    }


# ---------------------------------------------------------------------------
# Policy gradients
# ---------------------------------------------------------------------------

def reinforce(
    env_id: str = "CartPole-v1",
    episodes: int = 800,
    gamma: float = 0.99,
    lr: float = 1e-2,
    hidden: int = 64,
    entropy_coef: float = 0.01,
    normalize: bool = True,
    seed: int = 0,
    max_steps: int = 500,
) -> dict:
    """Vanilla policy gradient: ``grad J = E[sum_t grad log pi(a_t|s_t) * G_t]``."""
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(seed)
    env = gym.make(env_id)
    obs_dim = int(np.prod(env.observation_space.shape))
    n_actions = int(env.action_space.n)
    policy = PolicyNet(obs_dim, n_actions, hidden)
    opt = torch.optim.Adam(policy.parameters(), lr=lr)

    returns = []
    for ep in range(episodes):
        obs, _ = env.reset(seed=seed * 10_000 + ep)
        log_probs, rewards, entropies = [], [], []
        for _ in range(max_steps):
            a, logp = policy.act(obs, gen)
            logits = policy(torch.as_tensor(obs, dtype=torch.float32))
            entropies.append(torch.distributions.Categorical(logits=logits).entropy())
            obs, r, term, trunc, _ = env.step(a)
            log_probs.append(logp)
            rewards.append(float(r))
            if term or trunc:
                break
        returns.append(sum(rewards))

        G, returns_to_go = 0.0, []
        for r in reversed(rewards):
            G = r + gamma * G
            returns_to_go.append(G)
        returns_to_go.reverse()
        G_t = torch.as_tensor(returns_to_go, dtype=torch.float32)
        if normalize and len(G_t) > 1:
            G_t = (G_t - G_t.mean()) / (G_t.std() + 1e-8)
        logp = torch.as_tensor(log_probs, dtype=torch.float32)
        ent = torch.stack(entropies).mean()
        loss = -(logp * G_t).mean() - entropy_coef * ent
        opt.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(policy.parameters(), 5.0)
        opt.step()
    env.close()
    return {"returns": np.array(returns), "policy": policy,
            "final_eval": evaluate(policy, env_id, greedy_actions=False)}


def actor_critic(
    env_id: str = "CartPole-v1",
    episodes: int = 500,
    gamma: float = 0.99,
    lr: float = 1e-3,
    n_steps: int = 8,
    entropy_coef: float = 0.01,
    value_coef: float = 0.5,
    hidden: int = 64,
    seed: int = 0,
    max_steps: int = 500,
) -> dict:
    """Advantage actor-critic with ``n_steps``-step bootstrapping.

    ``A_t = sum_{k<t+n} gamma^k r_k + gamma^n V(s_n) - V(s_t)``; the policy loss is
    ``-log pi(a|s) * A.detach()`` and the critic regresses V toward the same target.
    """
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(seed)
    env = gym.make(env_id)
    obs_dim = int(np.prod(env.observation_space.shape))
    n_actions = int(env.action_space.n)
    model = ActorCritic(obs_dim, n_actions, hidden)
    opt = torch.optim.Adam(model.parameters(), lr=lr)

    returns = []
    for ep in range(episodes):
        obs, _ = env.reset(seed=seed * 10_000 + ep)
        ep_return = 0.0
        obs_buf, act_buf, rew_buf, logp_buf, val_buf = [], [], [], [], []
        done = False
        while not done:
            for _ in range(n_steps):
                logits, value = model(torch.as_tensor(obs, dtype=torch.float32))
                dist = torch.distributions.Categorical(logits=logits)
                a = dist.sample()
                obs2, r, term, trunc, _ = env.step(int(a.item()))
                obs_buf.append(obs)
                act_buf.append(int(a.item()))
                rew_buf.append(float(r))
                logp_buf.append(float(dist.log_prob(a).item()))
                val_buf.append(float(value.item()))
                obs = obs2
                ep_return += float(r)
                done = bool(term or trunc)
                if done:
                    break
            # bootstrap from the state where the rollout stopped
            with torch.no_grad():
                next_value = 0.0 if done else float(
                    model(torch.as_tensor(obs, dtype=torch.float32))[1].item())

            adv, rets = [], []
            gae, next_val = 0.0, next_value
            for t in reversed(range(len(rew_buf))):
                nonterminal = 0.0 if (t == len(rew_buf) - 1 and done) else 1.0
                delta = rew_buf[t] + gamma * next_val * nonterminal - val_buf[t]
                gae = delta + gamma * 0.95 * nonterminal * gae
                adv.insert(0, gae)
                rets.insert(0, gae + val_buf[t])
                next_val = val_buf[t]

            obs_t = torch.as_tensor(np.array(obs_buf), dtype=torch.float32)
            act_t = torch.as_tensor(act_buf, dtype=torch.long)
            adv_t = torch.as_tensor(adv, dtype=torch.float32)
            ret_t = torch.as_tensor(rets, dtype=torch.float32)
            logits, values = model(obs_t)
            dist = torch.distributions.Categorical(logits=logits)
            logp = dist.log_prob(act_t)
            policy_loss = -(logp * adv_t.detach()).mean()
            value_loss = F.mse_loss(values, ret_t.detach())
            entropy = dist.entropy().mean()
            loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            opt.step()

            obs_buf, act_buf, rew_buf, logp_buf, val_buf = [], [], [], [], []
        returns.append(ep_return)
    env.close()
    return {"returns": np.array(returns), "policy": model,
            "final_eval": evaluate(model, env_id, greedy_actions=False)}


def ppo(
    env_id: str = "CartPole-v1",
    episodes: int = 300,
    gamma: float = 0.99,
    lr: float = 3e-4,
    clip: float = 0.2,
    update_epochs: int = 4,
    batch_episodes: int = 8,
    gae_lambda: float = 0.95,
    entropy_coef: float = 0.01,
    value_coef: float = 0.5,
    hidden: int = 64,
    seed: int = 0,
    max_steps: int = 500,
) -> dict:
    """PPO with a clipped surrogate objective and GAE(lambda).

    ``L = -min(r_t A_t, clip(r_t, 1-eps, 1+eps) A_t) + c_v (V - R)^2 - c_e H[pi]``
    where ``r_t = pi_new(a|s) / pi_old(a|s)``.
    """
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(seed)
    env = gym.make(env_id)
    obs_dim = int(np.prod(env.observation_space.shape))
    n_actions = int(env.action_space.n)
    model = ActorCritic(obs_dim, n_actions, hidden)
    opt = torch.optim.Adam(model.parameters(), lr=lr)

    returns = []
    ep = 0
    while ep < episodes:
        batch_obs, batch_act, batch_logp, batch_adv, batch_ret = [], [], [], [], []
        for _ in range(batch_episodes):
            obs, _ = env.reset(seed=seed * 10_000 + ep)
            ep += 1
            ep_obs, ep_act, ep_rew, ep_logp, ep_val, ep_done = [], [], [], [], [], []
            done = False
            total = 0.0
            while not done:
                logits, value = model(torch.as_tensor(obs, dtype=torch.float32))
                dist = torch.distributions.Categorical(logits=logits)
                a = dist.sample()
                obs2, r, term, trunc, _ = env.step(int(a.item()))
                ep_obs.append(obs)
                ep_act.append(int(a.item()))
                ep_rew.append(float(r))
                ep_logp.append(float(dist.log_prob(a).item()))
                ep_val.append(float(value.item()))
                ep_done.append(bool(term))
                obs = obs2
                total += float(r)
                done = bool(term or trunc)
                if done:
                    break
            returns.append(total)

            adv, rets = [], []
            gae, next_val = 0.0, 0.0
            for t in reversed(range(len(ep_rew))):
                nonterminal = 0.0 if ep_done[t] else 1.0
                delta = ep_rew[t] + gamma * next_val * nonterminal - ep_val[t]
                gae = delta + gamma * gae_lambda * nonterminal * gae
                adv.insert(0, gae)
                rets.insert(0, gae + ep_val[t])
                next_val = ep_val[t]
            batch_obs.extend(ep_obs)
            batch_act.extend(ep_act)
            batch_logp.extend(ep_logp)
            batch_adv.extend(adv)
            batch_ret.extend(rets)

        obs_t = torch.as_tensor(np.array(batch_obs), dtype=torch.float32)
        act_t = torch.as_tensor(batch_act, dtype=torch.long)
        old_logp_t = torch.as_tensor(batch_logp, dtype=torch.float32)
        adv_t = torch.as_tensor(batch_adv, dtype=torch.float32)
        ret_t = torch.as_tensor(batch_ret, dtype=torch.float32)
        adv_t = (adv_t - adv_t.mean()) / (adv_t.std() + 1e-8)

        n = len(batch_obs)
        idx = np.arange(n)
        for _ in range(update_epochs):
            rng = np.random.default_rng(seed + ep)
            rng.shuffle(idx)
            for start in range(0, n, 256):
                mb = idx[start:start + 256]
                logits, values = model(obs_t[mb])
                dist = torch.distributions.Categorical(logits=logits)
                logp = dist.log_prob(act_t[mb])
                ratio = torch.exp(logp - old_logp_t[mb])
                a = adv_t[mb]
                surrogate = torch.min(ratio * a,
                                      torch.clamp(ratio, 1 - clip, 1 + clip) * a)
                policy_loss = -surrogate.mean()
                value_loss = F.mse_loss(values, ret_t[mb])
                entropy = dist.entropy().mean()
                loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
                opt.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(model.parameters(), 0.5)
                opt.step()
    env.close()
    return {"returns": np.array(returns), "policy": model,
            "final_eval": evaluate(model, env_id, greedy_actions=False)}


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def _report(name: str, result: dict, seconds: float) -> None:
    curve = result["returns"]
    hit = episodes_to(curve, 195.0)
    print(f"{name:14s} episodes={len(curve):4d}  steps={result.get('steps', -1):7d}  "
          f"last-20={np.mean(curve[-20:]):7.1f}  best-20={np.max(smooth(curve, 20)):7.1f}  "
          f"to-195={hit if hit is not None else '-':>4}  eval={result['final_eval']:6.1f}  "
          f"time={seconds:5.1f}s")


def main() -> None:
    total_start = time.time()

    print("=" * 96)
    print("1. DQN vs Double DQN on CartPole-v1 (2 seeds each)")
    print("=" * 96)
    print(f"{'agent':14s} {'episodes':>9} {'steps':>7} {'last-20':>8} {'best-20':>8} "
          f"{'to-195':>7} {'eval':>6} {'time':>8}")
    runs = {}
    for double in (False, True):
        for seed in (0, 1):
            t0 = time.time()
            res = train_dqn(episodes=300, double=double, seed=seed)
            name = ("Double DQN" if double else "DQN") + f" s{seed}"
            _report(name, res, time.time() - t0)
            if seed == 0:
                runs["Double DQN" if double else "DQN"] = res

    print("\n" + "=" * 96)
    print("2. Policy-gradient family on CartPole-v1")
    print("=" * 96)
    t0 = time.time()
    runs["REINFORCE"] = reinforce(episodes=800, seed=0)
    _report("REINFORCE", runs["REINFORCE"], time.time() - t0)

    t0 = time.time()
    runs["A2C"] = actor_critic(episodes=500, seed=0)
    _report("A2C", runs["A2C"], time.time() - t0)

    t0 = time.time()
    runs["PPO"] = ppo(episodes=300, seed=0)
    _report("PPO", runs["PPO"], time.time() - t0)

    print("\n" + "=" * 96)
    print("3. Learning-curve checkpoints (mean return over 20-episode windows)")
    print("=" * 96)
    checkpoints = (0, 20, 50, 100, 200, 300, 400, 600, 800)
    header = "agent      " + "".join(f"{c:>8}" for c in checkpoints)
    print(header)
    for name, res in runs.items():
        c = res["returns"]
        row = []
        for cp in checkpoints:
            if cp == 0:
                row.append(np.mean(c[:20]))
            elif cp < len(c):
                row.append(np.mean(c[cp - 20:cp]))
            else:
                row.append(np.nan)
        print(f"{name:10s} " + "".join(
            f"{('-' if np.isnan(v) else f'{v:8.1f}')}" for v in row))

    print(f"\ntotal wall-clock: {time.time() - total_start:.1f}s on CPU, "
          f"torch {torch.__version__}")


if __name__ == "__main__":
    main()
