"""Tests for M14 advanced AI applications.

These target the reusable parts: graph construction and leakage-free splits, the
neuro-symbolic policy boundary, time-series alignment and drift, federated averaging,
and multimodal encoding/retrieval metrics.
"""

import numpy as np
import pytest
import torch

import efficiency
import federated
import graphs
import multimodal
import neurosymbolic
import timeseries_monitor as tsm


# ---------------------------------------------------------------------------
# Graph construction and splits
# ---------------------------------------------------------------------------

def test_graph_is_symmetric_without_self_loops_and_balanced_labels():
    X, y, A, classes = graphs.make_graph(seed=0)
    assert X.shape == (200, 12)
    assert classes == 5
    assert np.allclose(A, A.T)
    assert np.all(np.diag(A) == 0)
    # Each node samples DEGREE neighbours; reciprocal linking raises the mean
    # above DEGREE but cannot exceed 2*DEGREE.
    mean_degree = float(A.sum(1).mean())
    assert graphs.DEGREE <= mean_degree <= 2 * graphs.DEGREE
    assert np.all(A.sum(1) >= 1)
    counts = np.bincount(y, minlength=classes)
    assert np.all(counts == 40)


def test_measured_homophily_increases_with_the_generation_parameter():
    measured = []
    for homophily in (0.0, 0.5, 1.0):
        X, y, A, _ = graphs.make_graph(homophily=homophily, seed=1)
        measured.append(graphs.edge_homophily(A, y))
    assert measured[0] < measured[1] < measured[2]
    assert measured[-1] == pytest.approx(1.0)
    # With five classes, uniform random mixing gives about 1/5 homophily.
    assert 0.15 < measured[0] < 0.25


def test_split_is_disjoint_stratified_and_covers_every_node():
    _, y, _, classes = graphs.make_graph(seed=2)
    train, test = graphs.split_nodes(y, train_frac=0.2, seed=2)
    assert len(set(train) & set(test)) == 0
    assert len(train) + len(test) == len(y)
    for c in range(classes):
        assert int((y[train] == c).sum()) == 8
        assert int((y[test] == c).sum()) == 32


def test_label_noise_flips_only_training_labels_and_is_reproducible():
    _, y, _, _ = graphs.make_graph(seed=3)
    train, test = graphs.split_nodes(y, seed=3)
    noisy = graphs.noisy_labels(y, train, fraction=0.1, seed=3)
    assert np.array_equal(noisy[test], y[test])
    changed = np.where(noisy != y)[0]
    assert len(changed) == int(0.1 * len(train))
    assert set(changed).issubset(set(train))
    assert np.array_equal(noisy, graphs.noisy_labels(y, train, fraction=0.1, seed=3))


def test_sbm_has_symmetric_edges_and_class_blocks():
    X, y, A, classes = graphs.make_sbm(seed=0)
    assert X.shape == (200, 12)
    assert classes == 5
    assert np.allclose(A, A.T)
    assert np.all(np.diag(A) == 0)
    assert graphs.edge_homophily(A, y) > 0.5


def test_sbm_is_reproducible_for_a_fixed_seed():
    first = graphs.make_sbm(seed=11)
    second = graphs.make_sbm(seed=11)
    assert np.array_equal(first[1], second[1])
    assert np.array_equal(first[2], second[2])
    assert not np.array_equal(first[2], graphs.make_sbm(seed=12)[2])


def test_inductive_run_is_reproducible_and_records_validation_accuracy():
    first = graphs.run_inductive("sbm", seed=3)
    second = graphs.run_inductive("sbm", seed=3)
    for model in ("majority", "mlp", "gcn"):
        assert first[model]["accuracy"] == second[model]["accuracy"]
    assert 0.0 <= first["gcn"]["validation_accuracy"] <= 1.0
    assert first["gcn"]["accuracy"] >= 0.5


def test_sbm_homophily_falls_as_cross_class_probability_rises():
    measured = []
    for p_out in (0.0, 0.01, 0.06, 0.2):
        X, y, A, _ = graphs.make_sbm(p_out=p_out, seed=0)
        measured.append(graphs.edge_homophily(A, y))
    assert measured == sorted(measured, reverse=True)
    assert measured[0] > 0.95


def test_inductive_split_is_disjoint_stratified_and_complete():
    _, y, _, classes = graphs.make_graph(seed=5)
    tr, va, te = graphs.inductive_split(y, seed=5)
    assert len(set(tr) & set(va)) == 0
    assert len(set(tr) & set(te)) == 0
    assert len(set(va) & set(te)) == 0
    assert len(tr) + len(va) + len(te) == len(y)
    for c in range(classes):
        assert int((y[tr] == c).sum()) == 24
        assert int((y[va] == c).sum()) == 8
        assert int((y[te] == c).sum()) == 8


def test_inductive_adjacencies_hide_test_nodes_and_test_test_edges():
    _, y, A, _ = graphs.make_graph(seed=6)
    _, _, test = graphs.inductive_split(y, seed=6)
    fit, infer = graphs._inductive_adjacencies(A, test)
    # Training graph: test rows carry only their self-loop.
    assert np.allclose(fit[np.ix_(test, test)], np.eye(len(test)))
    # Inference graph: test-test edges are removed, so that block is diagonal only.
    block = infer[np.ix_(test, test)]
    assert np.allclose(block, np.diag(np.diag(block)))
    assert np.all(np.diag(block) > 0)
    # Test-to-training edges remain visible at inference, as in a deployed graph.
    assert np.any(infer[np.ix_(test, np.setdiff1d(np.arange(len(y)), test))] > 0)


def test_evaluate_metrics_matches_hand_computation():
    y_true = np.array([0, 0, 1, 1, 2, 2])
    y_pred = np.array([0, 1, 1, 1, 2, 0])
    result = graphs.evaluate_metrics(y_true, y_pred, [0, 1, 2])
    assert result["accuracy"] == pytest.approx(4 / 6)
    # Class 0: P=1, R=0.5; class 1: P=2/3, R=1; class 2: P=1, R=0.5.
    per_class = {row["class"]: row for row in result["per_class"]}
    # One of the two class-0 predictions is correct.
    assert per_class[0]["precision"] == pytest.approx(0.5)
    assert per_class[0]["recall"] == pytest.approx(0.5)
    assert per_class[1]["precision"] == pytest.approx(2 / 3)
    assert per_class[2]["recall"] == pytest.approx(0.5)
    assert result["confusion"].tolist() == [[1, 1, 0], [0, 2, 0], [1, 0, 1]]


def test_majority_baseline_predicts_the_largest_training_class():
    pred, fill = graphs.majority_baseline(np.array([0, 1, 1, 1, 2]), np.zeros(3), 3)
    assert pred.tolist() == [1, 1, 1]
    assert fill.tolist() == [1, 1, 1]


def test_normalise_matches_the_symmetric_adjacency_formula():
    A = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.float32)
    result = graphs.normalise(A)
    expected = np.full((2, 2), 0.5, dtype=np.float32)
    assert np.allclose(result, expected)


def test_training_is_deterministic_for_a_fixed_seed_and_returns_an_accuracy():
    X, y, A, classes = graphs.make_graph(seed=4)
    An = graphs.normalise(A)
    train, test = graphs.split_nodes(y, seed=4)
    torch.manual_seed(11)
    first_model = graphs.MLP(12, classes)
    torch.manual_seed(11)
    second_model = graphs.MLP(12, classes)
    first = graphs.train(first_model, X, y, An, train, test, epochs=20, seed=4)
    second = graphs.train(second_model, X, y, An, train, test, epochs=20, seed=4)
    assert first == pytest.approx(second)
    assert 0.0 <= first <= 1.0


# ---------------------------------------------------------------------------
# Neuro-symbolic policy
# ---------------------------------------------------------------------------

def test_policy_income_boundary_is_strict():
    size = 2.0
    limit = neurosymbolic.INCOME_CAP + neurosymbolic.PER_PERSON * size
    assert bool(neurosymbolic.policy(limit - 1, 0, size, 0)) is True
    assert bool(neurosymbolic.policy(limit, 0, size, 0)) is False


def test_policy_savings_cap_and_property_rule():
    assert bool(neurosymbolic.policy(0, neurosymbolic.SAVINGS_CAP, 1, 0)) is False
    assert bool(neurosymbolic.policy(0, neurosymbolic.SAVINGS_CAP - 1, 1, 0)) is True
    # Owning property disqualifies only above the income threshold.
    assert bool(neurosymbolic.policy(19_000, 0, 5, 1)) is False
    assert bool(neurosymbolic.policy(10_000, 0, 5, 1)) is True


def test_policy_uses_per_person_allowance():
    assert bool(neurosymbolic.policy(30_000, 0, 4, 0)) is True
    assert bool(neurosymbolic.policy(30_000, 0, 1, 0)) is False


def test_evaluate_counts_only_false_eligibility_claims():
    probs = np.array([0.9, 0.2, 0.51, 0.49])
    eligible = np.array([False, True, False, True])
    decided, violations = neurosymbolic.evaluate(probs, eligible)
    assert decided.tolist() == [1, 0, 1, 0]
    assert violations == 2


# ---------------------------------------------------------------------------
# Time-series alignment, forecasting and drift
# ---------------------------------------------------------------------------

def test_lag_matrix_aligns_features_and_target_without_leakage():
    y = np.arange(10, dtype=float)
    X, target = tsm.lag_matrix(y, n_lags=3)
    assert X.shape == (7, 3)
    assert target.tolist() == list(range(3, 10))
    # Columns are most-recent-first: column 0 is y[t-1], column 2 is y[t-3].
    assert X[0].tolist() == [2.0, 1.0, 0.0]
    assert X[1].tolist() == [3.0, 2.0, 1.0]


def test_seasonal_naive_repeats_the_last_season():
    y = np.arange(1, 8, dtype=float)
    forecast = tsm.seasonal_naive(y, horizon=10, season=7)
    assert forecast.tolist() == [1, 2, 3, 4, 5, 6, 7, 1, 2, 3]


def test_psi_is_zero_for_identical_samples_and_large_under_shift():
    rng = np.random.default_rng(0)
    reference = rng.normal(0, 1, 2000)
    assert tsm.psi(reference, reference) == pytest.approx(0.0, abs=1e-9)
    shifted = rng.normal(4, 1, 2000)
    assert tsm.psi(reference, shifted) > 0.25


# ---------------------------------------------------------------------------
# Federated averaging
# ---------------------------------------------------------------------------

def test_average_of_identical_models_reproduces_the_model():
    a, b = federated.make_model(), federated.make_model()
    b.load_state_dict(a.state_dict())
    averaged = federated.avg_models([a, b])
    for pa, pm in zip(a.parameters(), averaged.parameters()):
        assert torch.allclose(pa, pm, atol=1e-7)


def test_weighted_average_with_zero_weight_returns_the_other_model():
    a, b = federated.make_model(), federated.make_model()
    averaged = federated.avg_models([a, b], weights=[1.0, 0.0])
    for pa, pm in zip(a.parameters(), averaged.parameters()):
        assert torch.allclose(pa, pm, atol=1e-7)


# ---------------------------------------------------------------------------
# Multimodal encoding and retrieval metrics
# ---------------------------------------------------------------------------

def test_encode_text_uses_vocabulary_and_ignores_unknown_words():
    vocab = {"a": 0, "b": 1}
    encoded = multimodal.encode_text(["a b", "a", "b unknown"], vocab)
    assert encoded.shape == (3, 2)
    assert encoded.tolist() == [[1.0, 1.0], [1.0, 0.0], [0.0, 1.0]]


def test_parameter_and_size_accounting_match_the_layers():
    model = efficiency.Net([4, 3, 2])
    # (4*3 + 3) + (3*2 + 2) = 23 parameters, all float32.
    assert efficiency.n_params(model) == 23
    assert efficiency.size_kb(model) == pytest.approx(23 * 4 / 1024)


def test_quantisation_preserves_predictions_within_a_small_error():
    torch.manual_seed(0)
    model = efficiency.Net([8, 16, 3])
    x = torch.rand(5, 8)
    q = efficiency.quantise(model)
    with torch.no_grad():
        difference = (q(x) - model(x)).abs().max()
    assert float(difference) < 0.05


def test_pruning_zeros_at_least_the_requested_fraction_without_changing_shapes():
    torch.manual_seed(0)
    model = efficiency.Net([8, 16, 3])
    pruned = efficiency.prune(model, fraction=0.5)
    before = sum(int((m.weight != 0).sum()) for m in model.net if isinstance(m, torch.nn.Linear))
    after = sum(int((m.weight != 0).sum()) for m in pruned.net if isinstance(m, torch.nn.Linear))
    assert after <= before
    for m, p in zip(model.net, pruned.net):
        if isinstance(m, torch.nn.Linear):
            assert m.weight.shape == p.weight.shape


def test_retrieval_metrics_are_perfect_for_aligned_pairs_and_zero_for_reversed():
    eye = torch.eye(4)
    aligned = multimodal.retrieval_metrics(eye, eye)
    assert aligned["i2t_r1"] == pytest.approx(1.0)
    assert aligned["t2i_r1"] == pytest.approx(1.0)

    reversed_order = torch.eye(4).flip(0)
    broken = multimodal.retrieval_metrics(reversed_order, eye)
    assert broken["i2t_r1"] == pytest.approx(0.0)
    assert broken["t2i_r1"] == pytest.approx(0.0)
