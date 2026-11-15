"""Tests for M07 neural-network fundamentals: gradients, softmax, optimisers, MLP."""

import numpy as np
import pytest

from nn_numpy import MLP, Adam, Momentum, RMSProp, SGD, gradient_check, softmax


def rng(seed=0):
    return np.random.default_rng(seed)


def test_softmax_rows_sum_to_one_and_are_shift_invariant():
    z = rng(1).normal(size=(5, 4)) * 3
    p = softmax(z)
    assert np.allclose(p.sum(axis=1), 1.0)
    assert np.all(p >= 0)
    assert np.allclose(softmax(z + 1000), p, atol=1e-12)


def test_softmax_of_a_constant_row_is_uniform():
    p = softmax(np.full((1, 5), 7.0))
    assert np.allclose(p, 1 / 5)


def test_gradient_check_passes_on_a_small_network():
    X = rng(2).normal(size=(10, 4))
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    assert gradient_check(MLP([4, 6, 2], seed=0), X, y) < 1e-4


def test_forward_output_is_a_probability_distribution():
    X = rng(3).normal(size=(7, 3))
    model = MLP([3, 5, 2], seed=0)
    probs, cache = model.forward(X)
    assert probs.shape == (7, 2)
    assert np.allclose(probs.sum(axis=1), 1.0)
    assert set(cache)  # the cache must carry what backward needs


def test_loss_is_negative_mean_log_likelihood():
    probs = np.array([[0.9, 0.1], [0.2, 0.8]])
    y = np.array([0, 1])
    model = MLP([2, 2, 2], seed=0)
    expected = -np.mean([np.log(0.9), np.log(0.8)])
    assert model.loss(probs, y) == pytest.approx(expected, rel=1e-9)


def test_sgd_step_moves_against_the_gradient():
    params = [np.array([1.0, -2.0])]
    SGD(lr=0.1).step(params, [np.array([0.5, -0.5])])
    assert np.allclose(params[0], np.array([0.95, -1.95]))


def test_momentum_accumulates_velocity():
    opt = Momentum(lr=0.1, beta=0.9)
    params = [np.array([0.0])]
    grads = [np.array([1.0])]
    opt.step(params, grads)
    first = params[0][0]
    opt.step(params, grads)
    second = params[0][0] - first
    assert second < first  # the second step is larger: velocity accumulated


def test_rmsprop_and_adam_take_a_bounded_first_step():
    for opt in (RMSProp(lr=0.01), Adam(lr=0.01)):
        params = [np.array([0.0])]
        opt.step(params, [np.array([5.0])])
        # adaptive methods normalise by a running magnitude, so the first step is
        # proportional to lr rather than to the gradient's absolute size
        assert -0.05 <= params[0][0] < 0.0


def test_mlp_learns_a_simple_non_linear_problem():
    X = rng(4).normal(size=(300, 2))
    y = ((X[:, 0] > 0) ^ (X[:, 1] > 0)).astype(int)
    import nn_numpy
    model = MLP([2, 16, 2], activation="tanh", seed=0)
    history = nn_numpy.train(model, X, y, epochs=150, batch_size=32,
                             optimizer=Adam(lr=0.03), seed=0)
    assert model.score(X, y) > 0.9, history["accuracy"][-1]


def test_dropout_is_active_in_training_and_off_at_inference():
    X = rng(5).normal(size=(50, 4))
    model = MLP([4, 8, 2], seed=0)
    train_probs, _ = model.forward(X, dropout=0.5, training=True)
    eval_probs, _ = model.forward(X, dropout=0.5, training=False)
    assert not np.allclose(train_probs, eval_probs)
    assert np.allclose(model.predict_proba(X), model.predict_proba(X))
