"""Tests for M06 machine learning: metrics, linear models, classifiers, clustering.

Reference values come from closed-form mathematics or from numpy, never from the class
under test.
"""

import numpy as np
import pytest

import classifiers as clf
import linreg
import unsupervised as uns


def rng(seed=0):
    return np.random.default_rng(seed)


# ------------------------------------------------------------------ metrics
def test_regression_metrics_match_their_definitions():
    y = np.array([3.0, -0.5, 2.0, 7.0])
    p = np.array([2.5, 0.0, 2.0, 8.0])
    assert linreg.mse(y, p) == pytest.approx(np.mean((y - p) ** 2))
    assert linreg.rmse(y, p) == pytest.approx(np.sqrt(np.mean((y - p) ** 2)))
    assert linreg.mae(y, p) == pytest.approx(np.mean(np.abs(y - p)))
    ss_res = np.sum((y - p) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    assert linreg.r2_score(y, p) == pytest.approx(1 - ss_res / ss_tot)


def test_adjusted_r2_penalises_extra_features():
    y = rng(1).normal(size=40)
    p = y + rng(2).normal(scale=0.3, size=40)
    r2 = linreg.r2_score(y, p)
    assert linreg.adjusted_r2(y, p, n_features=1) < r2
    assert linreg.adjusted_r2(y, p, n_features=2) < linreg.adjusted_r2(y, p, n_features=1)


# ------------------------------------------------------------- linear models
def test_ols_matches_numpy_lstsq():
    X = rng(3).normal(size=(80, 3))
    y = X @ np.array([1.5, -2.0, 0.25]) + 0.75
    model = linreg.LinearRegression().fit(X, y)
    expected = np.linalg.lstsq(np.c_[np.ones(80), X], y, rcond=None)[0]
    assert np.allclose(np.r_[model.intercept_, model.coef_], expected, atol=1e-9)


def test_ridge_matches_the_closed_form_solution():
    X = rng(4).normal(size=(50, 2))
    y = X @ np.array([1.0, -1.0]) + rng(5).normal(scale=0.2, size=50)
    alpha = 2.5
    model = linreg.Ridge(alpha=alpha).fit(X, y)
    Xc, yc = X - X.mean(0), y - y.mean()
    expected = np.linalg.solve(Xc.T @ Xc + alpha * np.eye(2), Xc.T @ yc)
    assert np.allclose(model.coef_, expected, atol=1e-8)


def test_lasso_shrinks_coefficients_as_alpha_grows():
    X = rng(6).normal(size=(60, 2))
    y = X @ np.array([2.0, -2.0]) + rng(7).normal(scale=0.1, size=60)
    small = np.abs(linreg.Lasso(alpha=0.01).fit(X, y).coef_).sum()
    large = np.abs(linreg.Lasso(alpha=1.0).fit(X, y).coef_).sum()
    assert large <= small + 1e-6


def test_gradient_descent_reaches_the_ols_solution():
    X = rng(8).normal(size=(200, 2))
    y = 1.0 + X @ np.array([3.0, -2.0]) + rng(9).normal(scale=0.01, size=200)
    ols = linreg.LinearRegression().fit(X, y)
    gd = linreg.LinearRegressionGD(lr=0.05, epochs=3000).fit(X, y)
    assert np.allclose(np.r_[gd.intercept_, gd.coef_], np.r_[ols.intercept_, ols.coef_], atol=0.05)


def test_polynomial_features_contain_the_requested_terms():
    X = np.array([[2.0, 3.0]])
    out = linreg.PolynomialFeatures(degree=2, include_bias=False).fit_transform(X)
    assert out.shape == (1, 5)          # x1, x2, x1^2, x1x2, x2^2
    assert 4.0 in out and 9.0 in out and 6.0 in out


# ---------------------------------------------------------------- classifiers
def test_logistic_regression_separates_a_linearly_separable_set():
    X = np.vstack([rng(10).normal(scale=0.3, size=(40, 2)) - 2,
                   rng(11).normal(scale=0.3, size=(40, 2)) + 2])
    y = np.r_[np.zeros(40, dtype=int), np.ones(40, dtype=int)]
    model = clf.LogisticRegressionGD(lr=0.1, epochs=500).fit(X, y)
    assert model.score(X, y) > 0.95
    proba = model.predict_proba(X)
    assert proba.shape == (80, 2)
    assert np.allclose(proba.sum(1), 1.0)


def test_knn_with_one_neighbour_reproduces_the_training_labels():
    X = rng(12).normal(size=(30, 2))
    y = (X[:, 0] > 0).astype(int)
    model = clf.KNNClassifier(k=1).fit(X, y)
    assert np.array_equal(model.predict(X), y)


def test_gaussian_naive_bayes_matches_a_hand_computed_posterior():
    X = np.array([[0.0], [0.2], [1.0], [1.2], [5.0], [5.4]])
    y = np.array([0, 0, 0, 0, 1, 1])
    model = clf.GaussianNB().fit(X, y)
    likelihoods = []
    for label in (0, 1):
        column = X[y == label, 0]
        mu, var = column.mean(), column.var()
        likelihoods.append(np.exp(-(0.3 - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var))
    expected = np.array([4 / 6, 2 / 6]) * np.array(likelihoods)
    expected /= expected.sum()
    assert np.allclose(model.predict_proba(np.array([[0.3]]))[0], expected, atol=1e-9)


def test_multinomial_naive_bayes_prefers_the_matching_vocabulary():
    X = np.array([[3, 0, 0], [2, 1, 0], [0, 0, 4], [0, 1, 3]])
    y = np.array([0, 0, 1, 1])
    model = clf.MultinomialNB().fit(X, y)
    assert model.predict(np.array([[5, 0, 0]]))[0] == 0
    assert model.predict(np.array([[0, 0, 5]]))[0] == 1


def test_decision_tree_fits_and_or_but_a_single_stump_cannot():
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    for y in (np.array([0, 0, 0, 1]), np.array([0, 1, 1, 1])):
        assert np.array_equal(clf.DecisionTreeClassifier(max_depth=2).fit(X, y).predict(X), y)
    xor = np.array([0, 1, 1, 0])
    assert not np.array_equal(clf.DecisionTreeClassifier(max_depth=1).fit(X, xor).predict(X), xor)


def test_tree_feature_importances_sum_to_one_when_a_split_exists():
    X = rng(13).normal(size=(120, 3))
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    model = clf.DecisionTreeClassifier(max_depth=3).fit(X, y)
    assert model.feature_importances_.sum() == pytest.approx(1.0)


def test_forest_is_at_least_as_good_as_a_stump_on_a_non_linear_problem():
    X = rng(14).normal(size=(200, 2))
    y = ((X[:, 0] ** 2 + X[:, 1] ** 2) > 1.5).astype(int)
    forest = clf.RandomForestClassifier(n_estimators=25, max_depth=4, seed=0).fit(X, y)
    stump = clf.DecisionTreeClassifier(max_depth=1).fit(X, y)
    assert forest.score(X, y) > stump.score(X, y)
    assert forest.score(X, y) > 0.85


def test_linear_svm_separates_a_margin():
    X = np.vstack([rng(15).normal(scale=0.2, size=(30, 2)) - 1.5,
                   rng(16).normal(scale=0.2, size=(30, 2)) + 1.5])
    y = np.r_[-np.ones(30), np.ones(30)]
    model = clf.LinearSVM(C=10.0, lr=0.05, epochs=800).fit(X, y)
    pred = np.asarray(model.predict(X))
    if set(np.unique(pred)) <= {0, 1}:          # accept a 0/1 or a -1/+1 encoding
        pred = np.where(pred == 0, -1, 1)
    assert (pred == y).mean() > 0.95


# --------------------------------------------------------------- unsupervised
def test_kmeans_reduces_inertia_and_recovers_separated_blobs():
    a = rng(17).normal(loc=-4, scale=0.3, size=(60, 2))
    b = rng(18).normal(loc=4, scale=0.3, size=(60, 2))
    X = np.vstack([a, b])
    model = uns.KMeans(n_clusters=2, seed=0).fit(X)
    assert model.inertia_ < 0.05 * uns.inertia(X, np.zeros(len(X), dtype=int), np.zeros((1, 2)))
    labels = model.labels_
    assert len(set(labels[:60])) == 1 and len(set(labels[60:])) == 1
    assert labels[0] != labels[-1]


def test_silhouette_score_is_high_for_separated_clusters_and_low_for_overlap():
    separated = np.vstack([rng(19).normal(0, 0.2, (40, 2)), rng(20).normal(6, 0.2, (40, 2))])
    labels = np.r_[np.zeros(40, dtype=int), np.ones(40, dtype=int)]
    assert uns.silhouette_score(separated, labels) > 0.8
    overlapping = rng(21).normal(size=(80, 2))
    assert uns.silhouette_score(overlapping, rng(22).integers(0, 2, 80)) < 0.5


def test_pca_explained_variance_is_a_distribution_and_ordered():
    X = rng(23).normal(size=(100, 4))
    model = uns.PCA(n_components=3).fit(X)
    ratio = np.asarray(model.explained_variance_ratio_)
    assert ratio.sum() <= 1.0 + 1e-9
    assert np.all(np.diff(ratio) <= 1e-12)


def test_pca_components_are_orthonormal():
    X = rng(24).normal(size=(200, 3)) @ rng(25).normal(size=(3, 3))
    model = uns.PCA(n_components=2).fit(X)
    components = np.asarray(model.components_)
    assert components.shape == (2, 3)
    assert np.allclose(components @ components.T, np.eye(2), atol=1e-8)


def test_dbscan_marks_noise_and_finds_dense_regions():
    core = rng(26).normal(scale=0.2, size=(50, 2))
    noise = np.array([[10.0, 10.0], [-10.0, -10.0]])
    X = np.vstack([core, noise])
    labels = uns.DBSCAN(eps=0.8, min_samples=5).fit(X).labels_
    assert labels[-1] == -1 and labels[-2] == -1
    assert len(set(labels[:-2])) == 1


def test_anomaly_detectors_flag_injected_outliers():
    X = rng(27).normal(size=(200, 3))
    X[0] = [12.0, -12.0, 9.0]
    z = uns.zscore_anomalies(X, threshold=3.0)
    assert 0 in np.asarray(z[1] if isinstance(z, tuple) else z)
    iqr = uns.iqr_anomalies(X, k=1.5)
    assert 0 in np.asarray(iqr[1] if isinstance(iqr, tuple) else iqr)
    scores = uns.mahalanobis_scores(X)
    assert np.argmax(scores) == 0
