"""Tests for M11 generative modelling: diffusion schedule and LoRA mechanics."""

import numpy as np
import pytest
import torch

import gen_models
import lora


def test_diffusion_schedule_is_monotonic_and_consistent():
    betas, alphas, alpha_bar = gen_models.diffusion_schedule(n_steps=50)
    betas, alphas, alpha_bar = (np.asarray(x, dtype=float) for x in (betas, alphas, alpha_bar))
    assert betas.shape == alphas.shape == alpha_bar.shape == (50,)
    assert np.all(betas > 0) and np.all(betas < 1)
    assert np.allclose(alphas, 1.0 - betas)
    assert np.all(np.diff(betas) >= 0)
    assert np.all(np.diff(alpha_bar) <= 0)
    assert alpha_bar[0] == pytest.approx(alphas[0])


def test_diffusion_schedule_hits_its_declared_endpoints():
    betas, _alphas, _alpha_bar = gen_models.diffusion_schedule(
        n_steps=10, beta_start=1e-4, beta_end=0.02)
    betas = np.asarray(betas, dtype=float)
    assert betas[0] == pytest.approx(1e-4)
    assert betas[-1] == pytest.approx(0.02)


def test_lora_layer_is_the_identity_at_initialisation():
    torch.manual_seed(0)
    base = torch.nn.Linear(6, 4)
    layer = lora.LoRALayer(base, r=2, alpha=4.0)
    x = torch.randn(3, 6)
    assert torch.allclose(layer(x), base(x), atol=1e-7)


def test_lora_freezes_the_base_and_adds_only_the_low_rank_parameters():
    base = torch.nn.Linear(6, 4)
    layer = lora.LoRALayer(base, r=2, alpha=4.0)
    assert all(not p.requires_grad for p in layer.base.parameters())
    assert layer.A.requires_grad and layer.B.requires_grad
    expected = 6 * 2 + 2 * 4
    assert layer.A.numel() + layer.B.numel() == expected
    assert layer.scale == pytest.approx(2.0)


def test_lora_update_is_low_rank_after_training_one_step():
    torch.manual_seed(1)
    base = torch.nn.Linear(5, 3)
    layer = lora.LoRALayer(base, r=1, alpha=2.0)
    x = torch.randn(4, 5)
    out = layer(x)
    out.sum().backward()
    assert layer.B.grad is not None and layer.B.grad.abs().sum() > 0
    assert base.weight.grad is None


def test_param_report_counts_total_and_trainable_parameters():
    model = torch.nn.Sequential(torch.nn.Linear(4, 3), torch.nn.Linear(3, 2))
    report = lora.param_report(model)
    assert report["total"] == 4 * 3 + 3 + 3 * 2 + 2
    assert report["trainable"] == report["total"]
    for parameter in model.parameters():
        parameter.requires_grad = False
    assert lora.param_report(model)["trainable"] == 0
