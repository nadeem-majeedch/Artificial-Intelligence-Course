"""Tests for M09 computer vision: filtering, thresholding, metrics, data properties."""

import numpy as np
import pytest
from scipy.signal import convolve2d as scipy_convolve

import vision_core as vc


def rng(seed=0):
    return np.random.default_rng(seed)


def test_convolution_with_an_identity_kernel_is_the_identity():
    image = rng(1).integers(0, 255, size=(9, 9)).astype(float)
    identity = np.zeros((3, 3))
    identity[1, 1] = 1.0
    assert np.allclose(vc.convolve2d(image, identity), image)


def test_convolution_matches_scipy_for_a_symmetric_kernel():
    image = rng(2).random((11, 11))
    kernel = vc.gaussian_kernel(5, 1.0)
    kernel = kernel / kernel.sum()
    expected = scipy_convolve(image, kernel, mode="same", boundary="fill", fillvalue=0.0)
    assert np.allclose(vc.convolve2d(image, kernel), expected, atol=1e-10)


def test_valid_padding_shrinks_the_output_by_k_minus_one():
    assert vc.convolve2d(np.zeros((8, 8)), np.ones((3, 3)), "valid").shape == (6, 6)
    assert vc.convolve2d(np.zeros((8, 8)), np.ones((5, 5)), "valid").shape == (4, 4)


def test_sobel_responds_to_a_vertical_edge_and_is_normalised():
    image = np.zeros((16, 16), dtype=float)
    image[:, 8:] = 255.0
    magnitude = vc.sobel_magnitude(image)
    assert magnitude.max() == pytest.approx(255.0)
    assert magnitude[:, 7].max() > magnitude[:, 1].max()


def test_otsu_split_is_the_same_for_uint8_and_unit_float_images():
    image = np.concatenate([np.full(60, 40), np.full(40, 190)]).reshape(10, 10).astype(np.uint8)
    threshold_u8 = vc.otsu_threshold(image)
    threshold_f = vc.otsu_threshold(image / 255.0)
    assert 40 <= threshold_u8 < 190
    assert 40 / 255 <= threshold_f < 190 / 255
    assert threshold_u8 / 255.0 == pytest.approx(threshold_f, abs=0.02)


def test_otsu_on_a_constant_image_returns_that_value():
    assert vc.otsu_threshold(np.full((4, 4), 77, dtype=np.uint8)) == pytest.approx(77.0)


def test_dilation_grows_and_erosion_shrinks_a_region():
    mask = np.zeros((9, 9), dtype=bool)
    mask[4, 4] = True
    assert vc.dilate(mask, 3).sum() == 9
    block = np.ones((9, 9), dtype=bool)
    assert vc.erode(block, 3).sum() < block.sum()


def test_hog_length_matches_the_cell_grid():
    image = rng(3).integers(0, 255, size=(32, 32)).astype(float)
    descriptor = vc.hog_descriptor(image, cell=8, bins=9)
    assert descriptor.size == (32 // 8) * (32 // 8) * 9
    assert np.isfinite(descriptor).all()


def test_iou_uses_xywh_boxes():
    assert vc.iou([0, 0, 10, 10], [0, 0, 10, 10]) == pytest.approx(1.0)
    assert vc.iou([0, 0, 10, 10], [20, 20, 5, 5]) == 0.0
    assert vc.iou([0, 0, 10, 10], [5, 0, 10, 10]) == pytest.approx(50 / 150)


def test_nms_suppresses_overlapping_lower_scores():
    kept = vc.nms([[0, 0, 10, 10], [1, 1, 10, 10], [40, 40, 10, 10]], [0.9, 0.8, 0.7], 0.5)
    assert kept == [0, 2]


def test_average_precision_is_one_for_a_perfect_ranking_and_low_for_reversed_scores():
    truth = [[0, 0, 10, 10]]
    perfect = vc.average_precision([[0, 0, 10, 10]], [0.9], truth, 0.5)
    missed = vc.average_precision([[50, 50, 10, 10]], [0.9], truth, 0.5)
    assert perfect == pytest.approx(1.0)
    assert missed == pytest.approx(0.0)


def test_dice_and_miou_match_pixel_definitions():
    a = np.zeros((10, 10), dtype=int)
    a[2:6, 2:6] = 1
    b = np.zeros((10, 10), dtype=int)
    b[4:8, 4:8] = 1
    intersection = int(((a == 1) & (b == 1)).sum())
    assert vc.dice(a, b, label=1) == pytest.approx(2 * intersection / (16 + 16))
    expected = np.mean([((a == 0) & (b == 0)).sum() / ((a == 0) | (b == 0)).sum(),
                        intersection / ((a == 1) | (b == 1)).sum()])
    assert vc.mean_iou(a, b, (0, 1)) == pytest.approx(expected)


def test_synthetic_datasets_are_reproducible_and_balanced():
    first, labels, _ = vc.make_leaf_images(n_per_class=8, seed=0)
    second, _labels, _ = vc.make_leaf_images(n_per_class=8, seed=0)
    other, _labels2, _ = vc.make_leaf_images(n_per_class=8, seed=1)
    assert np.array_equal(first, second)
    assert not np.array_equal(first, other)
    counts = np.bincount(np.asarray(labels).ravel())
    assert len(set(counts.tolist())) == 1
    assert first.dtype == np.uint8 and first.shape[1:] == (32, 32, 3)


def test_road_scene_has_all_three_labels_and_matching_shapes():
    image, mask = vc.make_road_scene(seed=2)
    assert image.shape == (64, 64, 3)
    assert mask.shape == (64, 64)
    assert set(np.unique(mask)) == {0, 1, 2}
