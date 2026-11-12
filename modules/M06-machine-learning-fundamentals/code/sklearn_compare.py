"""Fit the same models with this module's code and with scikit-learn, and compare.

The point is not that the libraries are interchangeable — they are not, down to the
defaults — but that the arithmetic is the same and the differences are explainable
(different optimisers, different stopping rules, different regularisation defaults).

Run `python sklearn_compare.py`. Requires scikit-learn (declared in the course
environment); the rest of the module does not.
"""

from __future__ import annotations

import numpy as np

import datasets as ds
import evaluation as ev
from classifiers import (
    DecisionTreeClassifier,
    KNNClassifier,
    LogisticRegressionGD,
)
from prep import StandardScaler, train_test_split
from unsupervised import KMeans, PCA, silhouette_score


def loan_data():
    frame = ds.loans()
    cols = [
        "annual_income_k", "loan_amount_k", "credit_score",
        "employment_years", "debt_ratio", "default_history",
    ]
    X = frame[cols].fillna(frame[cols].median()).to_numpy()
    y = frame["approved"].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, 0.25, seed=0, stratify=y)
    scaler = StandardScaler().fit(X_train)
    return scaler.transform(X_train), scaler.transform(X_test), y_train, y_test


def main() -> None:
    from sklearn.ensemble import RandomForestClassifier as SkForest
    from sklearn.linear_model import LogisticRegression as SkLogistic
    from sklearn.neighbors import KNeighborsClassifier as SkKNN
    from sklearn.tree import DecisionTreeClassifier as SkTree

    X_train, X_test, y_train, y_test = loan_data()

    print(f"{'model':22s} {'scratch acc':>11s} {'sklearn acc':>11s} {'scratch AUC':>11s} {'sklearn AUC':>11s}")

    pairs = [
        (
            "logistic regression",
            LogisticRegressionGD(lr=0.5, epochs=800, l2=0.0),
            SkLogistic(max_iter=1000, C=1e6),
        ),
        (
            "k-nearest neighbours",
            KNNClassifier(k=15),
            SkKNN(n_neighbors=15),
        ),
        (
            "decision tree (d=5)",
            DecisionTreeClassifier(max_depth=5, min_samples_leaf=5),
            SkTree(max_depth=5, min_samples_leaf=5, random_state=0),
        ),
        (
            "random forest",
            __import__("classifiers").RandomForestClassifier(
                n_estimators=100, max_depth=6, min_samples_leaf=5
            ),
            SkForest(n_estimators=100, max_depth=6, min_samples_leaf=5, random_state=0),
        ),
    ]

    for name, ours, theirs in pairs:
        ours.fit(X_train, y_train)
        theirs.fit(X_train, y_train)
        p_ours = ours.predict_proba(X_test)[:, 1]
        p_theirs = theirs.predict_proba(X_test)[:, 1]
        print(
            f"{name:22s} {ours.score(X_test, y_test):11.3f} {theirs.score(X_test, y_test):11.3f} "
            f"{ev.roc_auc_score(y_test, p_ours):11.3f} {ev.roc_auc_score(y_test, p_theirs):11.3f}"
        )

    print()
    frame = ds.customers()
    cols = ["annual_income_k", "spending_score", "recency_days", "purchase_frequency"]
    X = StandardScaler().fit_transform(frame[cols].to_numpy())

    ours = KMeans(4, seed=0).fit(X)
    from sklearn.cluster import KMeans as SkKMeans

    theirs = SkKMeans(n_clusters=4, n_init=10, random_state=0).fit(X)
    print("k-means inertia  scratch %.1f   sklearn %.1f" % (ours.inertia_, theirs.inertia_))
    print("k-means silhouette scratch %.3f sklearn %.3f" % (
        silhouette_score(X, ours.labels_),
        silhouette_score(X, theirs.labels_),
    ))

    pca_ours = PCA(2).fit(X)
    from sklearn.decomposition import PCA as SkPCA

    pca_theirs = SkPCA(n_components=2).fit(X)
    print("PCA explained ratio scratch", np.round(pca_ours.explained_variance_ratio_, 3))
    print("PCA explained ratio sklearn", np.round(pca_theirs.explained_variance_ratio_, 3))
    print("PCA loadings agree up to sign:",
          bool(np.allclose(np.abs(pca_ours.components_), np.abs(pca_theirs.components_), atol=1e-6)))


if __name__ == "__main__":
    main()
