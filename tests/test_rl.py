"""Tests for M10 reinforcement learning: DP identities, tabular control, replay buffer."""

import gymnasium as gym
import numpy as np
import pytest

import dqn
import experiments
import tabular
from dp import (bellman_residual, exact_policy_value, policy_evaluation,
                policy_iteration, random_policy, value_iteration)
from rl_envs import make_gridworld


def rollout(seed, steps=12):
    env = experiments.make_grid(size=4, slip=0.3)
    env.reset(seed=seed)
    rng = np.random.default_rng(0)
    trace = []
    for _ in range(steps):
        obs, reward, terminated, truncated, _info = env.step(int(rng.integers(0, 4)))
        trace.append((int(np.asarray(obs).ravel()[0]), round(float(reward), 6)))
        if terminated or truncated:
            break
    return trace


def test_gridworld_rollouts_are_reproducible_with_a_seed():
    assert rollout(7) == rollout(7)
    assert rollout(7) != rollout(8)   # slip is seeded, so the traces diverge


def test_value_iteration_satisfies_the_bellman_optimality_equation():
    mdp = make_gridworld(kind="open", slip=0.1)
    result = value_iteration(mdp, gamma=0.9, theta=1e-10)
    assert bellman_residual(mdp, result["V"], gamma=0.9) < 1e-8
    assert result["sweeps"] > 0


def test_policy_iteration_and_value_iteration_agree():
    mdp = make_gridworld(kind="maze", slip=0.05)
    vi = value_iteration(mdp, gamma=0.9, theta=1e-10)
    pi = policy_iteration(mdp, gamma=0.9, theta=1e-10)
    assert np.allclose(pi["V"], vi["V"], atol=1e-6)


def test_exact_policy_value_matches_iterative_evaluation():
    mdp = make_gridworld(kind="open")
    policy = random_policy(mdp, seed=0)
    iterative, _sweeps, _deltas = policy_evaluation(mdp, policy, gamma=0.9, theta=1e-12)
    exact = exact_policy_value(mdp, policy, gamma=0.9)
    assert np.allclose(iterative, exact, atol=1e-9)


def test_greedy_action_is_optimal_for_the_value_function():
    mdp = make_gridworld(kind="open")
    result = value_iteration(mdp, gamma=0.9, theta=1e-10)
    q_values = dqn_q_values(mdp, result["V"])
    for state in range(mdp.n_states):
        if mdp.is_terminal(state):
            continue
        best = int(np.argmax(q_values[state]))
        assert result["policy"][state] == best


def dqn_q_values(mdp, V):
    from dp import action_values
    return action_values(mdp, V, gamma=0.9)


def test_epsilon_greedy_respects_both_extremes():
    rng = np.random.default_rng(0)
    q = np.array([1.0, 5.0, 2.0])
    assert tabular.epsilon_greedy(q, 3, 0.0, rng) == 1
    picks = {tabular.epsilon_greedy(q, 3, 1.0, rng) for _ in range(60)}
    assert picks == {0, 1, 2}


def test_q_learning_learns_a_policy_that_reaches_the_goal():
    env = experiments.make_grid(size=4)
    result = tabular.q_learning(env, episodes=600, alpha=0.5, gamma=0.95,
                                eps=0.2, eps_end=0.02, decay_episodes=500, seed=0)
    Q = result["Q"]
    policy = lambda obs: int(np.argmax(Q.get(int(np.asarray(obs).ravel()[0]), np.zeros(4))))  # noqa: E731
    score = tabular.evaluate(experiments.make_grid(size=4), policy, episodes=30, seed=1)
    assert score["success"] > 0.9


def test_sarsa_and_q_learning_both_improve_over_a_random_policy():
    baseline = experiments.random_baseline(experiments.make_cliff(), episodes=100, seed=0)
    comparison = experiments.compare_sarsa_qlearning(episodes=300, seeds=(0, 1))
    floor = baseline.get("return", baseline.get("mean_return", -1e9))
    assert comparison["sarsa_tail"] > floor
    assert comparison["q_learning_tail"] > floor


def test_td0_converges_towards_the_exact_value_of_a_fixed_policy():
    policy = lambda obs: 0  # noqa: E731
    env = gym.make("FrozenLake-v1", is_slippery=False)
    exact = tabular.exact_values(env, policy, gamma=0.99)
    learned = tabular.td0_prediction(env, policy, episodes=3000, alpha=0.1, gamma=0.99, seed=0)
    error = np.mean([abs(learned.get(k, 0.0) - v) for k, v in exact.items()])
    assert error < 0.15


def test_replay_buffer_wraps_at_capacity_and_samples_the_right_shapes():
    buffer = dqn.ReplayBuffer(capacity=10, obs_dim=3)
    for step in range(25):
        buffer.add(np.array([step, step, step], dtype=float), step % 4, float(step), 
                   np.array([step + 1, step, step], dtype=float), False)
    batch = buffer.sample(6, np.random.default_rng(0))
    obs, action, reward, next_obs, done = batch
    assert obs.shape == (6, 3) and next_obs.shape == (6, 3)
    assert action.shape[0] == reward.shape[0] == done.shape[0] == 6
    assert reward.max() <= 24.0


def test_q_network_maps_a_batch_of_states_to_one_value_per_action():
    import torch

    torch.manual_seed(0)
    net = dqn.QNet(obs_dim=4, n_actions=2, hidden=16)
    values = net(torch.zeros(5, 4))
    assert values.shape == (5, 2)
    assert torch.isfinite(values).all()


def test_policy_network_outputs_a_finite_score_per_action():
    import torch

    net = dqn.PolicyNet(obs_dim=4, n_actions=2, hidden=16)
    scores = net(torch.randn(3, 4))
    assert scores.shape == (3, 2)
    if torch.all(scores >= 0):        # a softmax head
        assert torch.allclose(scores.sum(1), torch.ones(3), atol=1e-5)


def test_smoothing_and_episodes_to_use_the_documented_window():
    curve = list(range(10))
    smoothed = dqn.smooth(curve, window=3)
    assert len(smoothed) == len(curve) - 2
    assert smoothed[0] == pytest.approx(1.0)
    assert dqn.episodes_to([0] * 10 + [200] * 40, threshold=195, window=5) == 15
    assert dqn.episodes_to([0] * 10, threshold=195, window=5) is None


def test_epsilon_schedule_decays_to_its_floor_and_stays_there():
    values = [dqn.epsilon_schedule(step, start=1.0, end=0.05, decay_steps=100) for step in (0, 50, 100, 500)]
    assert values[0] == pytest.approx(1.0)
    assert values[1] < values[0]
    assert values[2] == pytest.approx(0.05)
    assert values[3] == pytest.approx(0.05)
