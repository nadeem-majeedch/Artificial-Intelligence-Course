"""gen_models.py -- VAE, GAN and diffusion from scratch on 8x8 digits (M11, L11-01).

All three models are deliberately small (a few hundred thousand parameters) so
that they train on a CPU in under a minute each. The point is the objective,
not the sample quality: each model is trained on the same 64-dimensional data
and judged with the same metrics, so the comparison is honest.

    VAE        evidence lower bound: reconstruction + beta * KL
    GAN        adversarial: min_G max_D E log D(x) + E log(1 - D(G(z)))
    DDPM       denoising diffusion: predict the noise added at step t

Data: scikit-learn's `load_digits` (8x8 grayscale, 1797 images, 10 classes),
the UCI digits dataset (CC BY 4.0) loaded through scikit-learn; no download is needed.
Every random component is seeded.

Run ``python gen_models.py`` for the numbers quoted in L11-01 and NB-11-01.
"""

from __future__ import annotations

import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def digits(seed: int = 0):
    """Return (X, y): X is float32 (n, 64) in [0,1], y is int64 labels."""
    from sklearn.datasets import load_digits

    d = load_digits()
    X = (d.images.reshape(len(d.images), -1) / 16.0).astype(np.float32)
    y = d.target.astype(np.int64)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(X))
    return torch.from_numpy(X[perm]), torch.from_numpy(y[perm])


# ---------------------------------------------------------------------------
# 1. Variational autoencoder
# ---------------------------------------------------------------------------

class VAE(nn.Module):
    """Gaussian-latent autoencoder. Encoder outputs mu and log-var; decoder outputs logits."""

    def __init__(self, dim: int = 64, latent: int = 8, hidden: int = 128):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(dim, hidden), nn.ReLU(),
                                 nn.Linear(hidden, hidden), nn.ReLU())
        self.mu = nn.Linear(hidden, latent)
        self.logvar = nn.Linear(hidden, latent)
        self.dec = nn.Sequential(nn.Linear(latent, hidden), nn.ReLU(),
                                 nn.Linear(hidden, hidden), nn.ReLU(),
                                 nn.Linear(hidden, dim))

    def encode(self, x):
        h = self.enc(x)
        return self.mu(h), self.logvar(h).clamp(-8, 8)

    def reparameterise(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        return mu + std * torch.randn_like(std)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterise(mu, logvar)
        return self.dec(z), mu, logvar


def train_vae(epochs: int = 30, latent: int = 8, hidden: int = 128, beta: float = 1.0,
              lr: float = 1e-3, batch: int = 128, seed: int = 0) -> dict:
    set_seed(seed)
    X, y = digits(seed)
    model = VAE(64, latent, hidden)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    history = {"loss": [], "recon": [], "kl": []}
    n = len(X)
    for ep in range(epochs):
        perm = torch.randperm(n)
        tot = rec = kl = 0.0
        for i in range(0, n, batch):
            idx = perm[i:i + batch]
            xb = X[idx]
            logits, mu, logvar = model(xb)
            bce = F.binary_cross_entropy_with_logits(logits, xb, reduction="sum") / len(xb)
            kld = (-0.5 * (1 + logvar - mu.pow(2) - logvar.exp()).sum(1)).mean()
            loss = bce + beta * kld
            opt.zero_grad()
            loss.backward()
            opt.step()
            tot += float(loss) * len(xb)
            rec += float(bce) * len(xb)
            kl += float(kld) * len(xb)
        history["loss"].append(tot / n)
        history["recon"].append(rec / n)
        history["kl"].append(kl / n)
    with torch.no_grad():
        mu, logvar = model.encode(X)
        z = model.reparameterise(mu, logvar)
        recon = torch.sigmoid(model.dec(z))
    return {"model": model, "history": history, "X": X, "y": y,
            "recon_mse": float(F.mse_loss(recon, X).item()),
            "active_latents": int((mu.std(0) > 0.1).sum().item()),
            "latent_std": mu.std(0).cpu().numpy().round(3).tolist()}


def vae_samples(model: VAE, n: int = 200, seed: int = 0) -> torch.Tensor:
    set_seed(seed)
    with torch.no_grad():
        z = torch.randn(n, model.mu.out_features)
        return torch.sigmoid(model.dec(z))


# ---------------------------------------------------------------------------
# 2. Generative adversarial network
# ---------------------------------------------------------------------------

class Generator(nn.Module):
    def __init__(self, latent: int = 8, dim: int = 64, hidden: int = 128):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(latent, hidden), nn.ReLU(),
                                 nn.Linear(hidden, hidden), nn.ReLU(),
                                 nn.Linear(hidden, dim), nn.Sigmoid())

    def forward(self, z):
        return self.net(z)


class Discriminator(nn.Module):
    def __init__(self, dim: int = 64, hidden: int = 128):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(dim, hidden), nn.LeakyReLU(0.2),
                                 nn.Linear(hidden, hidden), nn.LeakyReLU(0.2),
                                 nn.Linear(hidden, 1))

    def forward(self, x):
        return self.net(x)


def train_gan(steps: int = 1500, latent: int = 8, hidden: int = 128, lr: float = 2e-4,
              batch: int = 64, seed: int = 0) -> dict:
    set_seed(seed)
    X, y = digits(seed)
    G, D = Generator(latent, 64, hidden), Discriminator(64, hidden)
    optG = torch.optim.Adam(G.parameters(), lr=lr, betas=(0.5, 0.999))
    optD = torch.optim.Adam(D.parameters(), lr=lr, betas=(0.5, 0.999))
    bce = nn.BCEWithLogitsLoss()
    hist = {"d_loss": [], "g_loss": [], "d_real": [], "d_fake": []}
    n = len(X)
    for step in range(steps):
        idx = torch.randint(0, n, (batch,))
        real = X[idx]
        z = torch.randn(batch, latent)
        fake = G(z).detach()

        d_real = D(real)
        d_fake = D(fake)
        loss_d = bce(d_real, torch.ones_like(d_real)) + bce(d_fake, torch.zeros_like(d_fake))
        optD.zero_grad()
        loss_d.backward()
        optD.step()

        z = torch.randn(batch, latent)
        fake = G(z)
        d_out = D(fake)
        loss_g = bce(d_out, torch.ones_like(d_out))
        optG.zero_grad()
        loss_g.backward()
        optG.step()

        hist["d_loss"].append(float(loss_d))
        hist["g_loss"].append(float(loss_g))
        hist["d_real"].append(float(torch.sigmoid(d_real).mean()))
        hist["d_fake"].append(float(torch.sigmoid(d_fake).mean()))
    with torch.no_grad():
        samples = G(torch.randn(500, latent))
    return {"G": G, "D": D, "history": hist, "X": X, "y": y, "samples": samples}


# ---------------------------------------------------------------------------
# 3. Denoising diffusion (DDPM)
# ---------------------------------------------------------------------------

class TimeMLP(nn.Module):
    """MLP denoiser that takes the noisy vector and a sinusoidal time embedding."""

    def __init__(self, dim: int = 64, t_dim: int = 16, hidden: int = 256):
        super().__init__()
        self.t_dim = t_dim
        self.net = nn.Sequential(nn.Linear(dim + t_dim, hidden), nn.SiLU(),
                                 nn.Linear(hidden, hidden), nn.SiLU(),
                                 nn.Linear(hidden, dim))

    def time_features(self, t: torch.Tensor, n_steps: int) -> torch.Tensor:
        freqs = torch.exp(-torch.arange(self.t_dim // 2) * (np.log(1000.0) / (self.t_dim // 2)))
        args = t.float()[:, None] / n_steps * freqs[None, :] * 2 * np.pi
        return torch.cat([torch.sin(args), torch.cos(args)], dim=-1)

    def forward(self, x, t, n_steps):
        return self.net(torch.cat([x, self.time_features(t, n_steps)], dim=-1))


def diffusion_schedule(n_steps: int = 200, beta_start: float = 1e-4,
                       beta_end: float = 0.02):
    betas = torch.linspace(beta_start, beta_end, n_steps)
    alphas = 1.0 - betas
    alpha_bar = torch.cumprod(alphas, dim=0)
    return betas, alphas, alpha_bar


def train_diffusion(steps: int = 1500, n_steps: int = 200, hidden: int = 256,
                    lr: float = 1e-3, batch: int = 128, seed: int = 0) -> dict:
    set_seed(seed)
    X, y = digits(seed)
    betas, alphas, alpha_bar = diffusion_schedule(n_steps)
    model = TimeMLP(64, 16, hidden)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    hist = []
    n = len(X)
    for step in range(steps):
        idx = torch.randint(0, n, (batch,))
        x0 = X[idx]
        t = torch.randint(0, n_steps, (batch,))
        eps = torch.randn_like(x0)
        ab = alpha_bar[t][:, None]
        xt = ab.sqrt() * x0 + (1 - ab).sqrt() * eps
        eps_hat = model(xt, t, n_steps)
        loss = F.mse_loss(eps_hat, eps)
        opt.zero_grad()
        loss.backward()
        opt.step()
        hist.append(float(loss))
    return {"model": model, "history": np.array(hist), "X": X, "y": y,
            "n_steps": n_steps, "betas": betas, "alphas": alphas,
            "alpha_bar": alpha_bar}


@torch.no_grad()
def diffusion_samples(model, alpha_bar, alphas, betas, n: int = 200, n_steps: int = 200,
                      seed: int = 0) -> torch.Tensor:
    set_seed(seed)
    x = torch.randn(n, 64)
    for t in reversed(range(n_steps)):
        tt = torch.full((n,), t, dtype=torch.long)
        eps_hat = model(x, tt, n_steps)
        a, ab = alphas[t], alpha_bar[t]
        beta = betas[t]
        mean = (x - (1 - a) / (1 - ab).sqrt() * eps_hat) / a.sqrt()
        if t > 0:
            x = mean + beta.sqrt() * torch.randn_like(x)
        else:
            x = mean
    return x.clamp(0, 1)


# ---------------------------------------------------------------------------
# 4. Metrics shared by all three
# ---------------------------------------------------------------------------

def sample_metrics(samples: torch.Tensor, X: torch.Tensor, y: torch.Tensor) -> dict:
    """Nearest-neighbour distance, class coverage and diversity of generated data.

    The 1-NN classifier is fitted on the *real* training split only, so the class
    distribution of the samples is not circular: it measures whether the
    generator produces recognisable digits, not whether it memorised labels.
    """
    from sklearn.neighbors import KNeighborsClassifier

    S = samples.numpy()
    Xn = X.numpy()
    dist = ((S[:, None, :] - Xn[None, :, :]) ** 2).sum(-1)
    nn = dist.min(1)
    knn = KNeighborsClassifier(n_neighbors=1).fit(Xn, y.numpy())
    pred = knn.predict(S)
    counts = np.bincount(pred, minlength=10)
    p = counts / counts.sum()
    entropy = float(-(p[p > 0] * np.log(p[p > 0])).sum())
    pairwise = ((S[:, None, :] - S[None, :, :]) ** 2).sum(-1)
    upper = pairwise[np.triu_indices(len(S), k=1)]
    return {
        "nn_mse": float(nn.mean()),
        "nn_mse_median": float(np.median(nn)),
        "classes_seen": int((counts > 0).sum()),
        "class_entropy": entropy,
        "max_class_share": float(p.max()),
        "pairwise_mse": float(upper.mean()),
        "sample_mean": float(S.mean()),
        "real_mean": float(Xn.mean()),
    }


def digits_images(arr: np.ndarray, n: int = 10):
    """Reshape a flat array into an (n, 8, 8) grid for plotting."""
    return arr[:n].reshape(-1, 8, 8)


# ---------------------------------------------------------------------------
# 5. Demo
# ---------------------------------------------------------------------------

def main() -> None:
    X, y = digits(0)
    print("=" * 84)
    print("Data")
    print("=" * 84)
    print(f"images        : {len(X)}  shape {tuple(X.shape)}  classes {len(torch.unique(y))}")
    print(f"pixel range   : [{float(X.min()):.2f}, {float(X.max()):.2f}]  "
          f"mean {float(X.mean()):.3f}")
    gaps = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)
    gaps.fill_diagonal_(np.inf)
    print(f"nearest-neighbour MSE between real images: {float(gaps.min(1).values.mean()):.5f}")

    print("\n" + "=" * 84)
    print("1. Variational autoencoder (beta=1, latent 8, 30 epochs)")
    print("=" * 84)
    t0 = time.time()
    v = train_vae()
    dt = time.time() - t0
    h = v["history"]
    print(f"epochs 30 in {dt:.1f}s   final loss {h['loss'][-1]:.2f} "
          f"(recon {h['recon'][-1]:.2f}, KL {h['kl'][-1]:.2f})")
    print(f"loss path     : {[round(x, 1) for x in h['loss'][::5]]}")
    print(f"reconstruction MSE on training data: {v['recon_mse']:.5f}")
    print(f"active latents (std > 0.1): {v['active_latents']}/8")
    print(f"latent std    : {v['latent_std']}")
    s = vae_samples(v["model"], 300)
    m = sample_metrics(s, v["X"], v["y"])
    print(f"VAE samples   : nn_mse {m['nn_mse']:.4f}  classes {m['classes_seen']}/10  "
          f"max class share {m['max_class_share']:.2f}  diversity {m['pairwise_mse']:.4f}")

    print("\n" + "=" * 84)
    print("2. GAN (latent 8, 1500 steps)")
    print("=" * 84)
    t0 = time.time()
    g = train_gan()
    dt = time.time() - t0
    hd, hg = g["history"]["d_loss"], g["history"]["g_loss"]
    print(f"1500 steps in {dt:.1f}s   D loss {np.mean(hd[-100:]):.3f}  "
          f"G loss {np.mean(hg[-100:]):.3f}")
    print(f"D(real) {np.mean(g['history']['d_real'][-100:]):.3f}  "
          f"D(fake) {np.mean(g['history']['d_fake'][-100:]):.3f}")
    print(f"loss path D   : {[round(float(np.mean(hd[i:i + 100])), 2) for i in range(0, 1500, 300)]}")
    m = sample_metrics(g["samples"], g["X"], g["y"])
    print(f"GAN samples   : nn_mse {m['nn_mse']:.4f}  classes {m['classes_seen']}/10  "
          f"max class share {m['max_class_share']:.2f}  diversity {m['pairwise_mse']:.4f}")

    print("\n" + "=" * 84)
    print("3. Diffusion (DDPM, 200 timesteps, 1500 training steps)")
    print("=" * 84)
    t0 = time.time()
    d = train_diffusion()
    dt = time.time() - t0
    hist = d["history"]
    print(f"1500 steps in {dt:.1f}s   final noise-prediction MSE {hist[-1]:.4f}  "
          f"first-100 mean {hist[:100].mean():.4f}  last-100 mean {hist[-100:].mean():.4f}")
    print(f"loss path     : {[round(float(hist[i:i + 250].mean()), 4) for i in range(0, 1500, 250)]}")
    t0 = time.time()
    s = diffusion_samples(d["model"], d["alpha_bar"], d["alphas"], d["betas"], 200)
    print(f"sampling 200 images over 200 reverse steps: {time.time() - t0:.1f}s")
    m = sample_metrics(s, d["X"], d["y"])
    print(f"DDPM samples  : nn_mse {m['nn_mse']:.4f}  classes {m['classes_seen']}/10  "
          f"max class share {m['max_class_share']:.2f}  diversity {m['pairwise_mse']:.4f}")

    print("\n" + "=" * 84)
    print("4. Same metrics, one table")
    print("=" * 84)
    va = sample_metrics(vae_samples(v["model"], 300), v["X"], v["y"])
    ga = sample_metrics(g["samples"], g["X"], g["y"])
    da = sample_metrics(s, d["X"], d["y"])
    print(f"{'model':10s} {'nn_mse':>8} {'classes':>8} {'max share':>10} "
          f"{'diversity':>10} {'mean pixel':>11}")
    print(f"{'real':10s} {float(gaps.min(1).values.mean()):8.4f} {'10':>8} "
          f"{float(np.bincount(y.numpy()).max() / len(y)):10.2f} "
          f"{float(gaps[gaps < np.inf].mean()):10.4f} {float(X.mean()):11.3f}")
    for name, a in (("VAE", va), ("GAN", ga), ("DDPM", da)):
        print(f"{name:10s} {a['nn_mse']:8.4f} {a['classes_seen']:8d} "
              f"{a['max_class_share']:10.2f} {a['pairwise_mse']:10.4f} "
              f"{a['sample_mean']:11.3f}")

    np.savez_compressed(
        "gen_samples.npz",
        real=v["X"].numpy()[:64], real_labels=v["y"].numpy()[:64],
        vae=vae_samples(v["model"], 64).numpy(),
        gan=g["samples"][:64].numpy(),
        ddpm=s[:64].numpy(),
        vae_loss=np.array(v["history"]["loss"]),
        gan_d=np.array(g["history"]["d_loss"]),
        gan_g=np.array(g["history"]["g_loss"]),
        ddpm_loss=d["history"],
    )
    print("\nsaved gen_samples.npz (samples and loss curves for the notebook figures)")


if __name__ == "__main__":
    main()
