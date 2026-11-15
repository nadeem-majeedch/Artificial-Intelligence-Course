# L09-06 — Advanced Computer Vision

| Module | M09 · Computer Vision |
| :--- | :--- |
| Level | 300 |
| Study time | 75 minutes |
| Prerequisites | [L09-05](L09-05-image-segmentation.md) · [L08-06](../../M08-natural-language-processing/lessons/L08-06-sequence-models-attention-and-transformers.md) |
| Code | `code/vision_core.py` |

[← Previous: L09-05](L09-05-image-segmentation.md) · [Module home](../README.md)

## 1. Learning Objectives

- **Decide** when to fine-tune, when to freeze, and when to train from scratch.
- **Explain** how a Vision Transformer turns an image into a sequence.
- **Compare** convolution and attention on inductive bias and data requirements.
- **Use** an image encoder as an embedding for retrieval, with a stated licence for any weights.
- **Describe** a vision-language model's contract and its failure modes.

## 2. Prerequisite Knowledge

Attention and transformers from
[L08-06](../../M08-natural-language-processing/lessons/L08-06-sequence-models-attention-and-transformers.md),
and the CNN pipeline from [L09-03](L09-03-image-classification-and-cnns.md).

## 3. Conceptual Explanation

### 3.1 Transfer learning is the default

Training a vision model from scratch needs data you do not have and compute you may not want to spend.
Transfer learning reuses features learned elsewhere:

| Strategy | What you train | When |
| :--- | :--- | :--- |
| Linear probe | final classifier only | tiny dataset, new classes |
| Partial fine-tune | last block + head | small dataset, related domain |
| Full fine-tune | everything, small learning rate | medium dataset |
| From scratch | everything, large learning rate | lots of data, or a domain where pretrained features mislead |

Freezing early layers keeps generic edge and texture detectors; fine-tuning late layers adapts semantics.
Lower the learning rate by 10× when unfreezing, or the pretrained features are destroyed in the first epoch.

### 3.2 Vision Transformers

A ViT splits the image into patches (for example 16×16), flattens each patch to a vector, adds a learned
position embedding, and runs a transformer encoder. There is no convolution: every patch can attend to
every other patch from layer one.

That is a different inductive bias. Convolution *assumes* locality and translation equivariance; attention
*learns* them from data. Consequences:

- ViTs need more data or stronger augmentation to match CNNs at small scale.
- ViTs scale better: with enough data they surpass CNNs, which is why large vision systems are transformer-based.
- Hybrids (convolutional stem + transformer body) get both, and are common in practice.

### 3.3 Multimodal models

A vision-language model maps an image and text into a shared embedding space (contrastive training) or
generates text conditioned on image tokens (captioning, visual question answering). Two engineering facts
matter more than the architecture:

1. **The contract is probabilistic.** "Describe this image" is a request, not a specification; the model
   can be fluent and wrong.
2. **The weights have a licence.** Every checkpoint you load has terms; record them, and prefer models
   whose licence you can defend in a report.

### 3.4 Embeddings, retrieval and clustering

A trained encoder turns an image into a vector. Cosine similarity then supports nearest-neighbour
retrieval, duplicate detection and clustering — no labels required. This is often the highest-value use
of vision in an organisation, and it is cheap: one forward pass per image.

## 4. Pseudocode

```text
function FINE_TUNE(backbone, data, freeze_until):
    for layer in backbone.layers:
        layer.requires_grad <- layer.index >= freeze_until
    optimiser <- Adam(params with lr = base_lr / 10)
    for epoch in 1..epochs:
        for images, labels in data:
            loss <- cross_entropy(backbone(images), labels)
            update
    return backbone
```

## 5. Worked Example — the same head, two feature sets

Using this module's synthetic signs, compare hand-crafted HOG features against learned CNN features with
the *same* classifier on top. On 120 images the two are usually within a couple of points of each other —
which is the honest result on tiny synthetic data, and the reason L09-03 insists on a baseline.

```python
import numpy as np
import vision_core as v
from sklearn.linear_model import LogisticRegression

images, labels, names = v.make_sign_images(n_per_class=40, size=32, seed=0)
features = np.stack([v.hog_descriptor(v.to_gray(img), cell=8) for img in images])
model = LogisticRegression(max_iter=1000).fit(features[:90], labels[:90])
print("HOG + logistic regression:", round(model.score(features[90:], labels[90:]), 3))
```

## 6. Mathematical Formulation

Scaled dot-product attention, applied to patch tokens $X \in \mathbb{R}^{N \times d}$:

$$\mathrm{Attn}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

For $N$ patches the attention matrix is $N \times N$: cost grows quadratically with image resolution, which
is why patch size is a compute decision, not an aesthetic one.

Contrastive (CLIP-style) loss for a batch of $B$ image-text pairs with cosine similarities $s_{ij}$:

$$\mathcal{L} = -\frac{1}{2B}\sum_i \left[\log\frac{e^{s_{ii}/\tau}}{\sum_j e^{s_{ij}/\tau}} +
\log\frac{e^{s_{ii}/\tau}}{\sum_j e^{s_{ji}/\tau}}\right]$$

## 7. Python Implementation

```python
import numpy as np
import vision_core as v

images, labels, names = v.make_leaf_images(n_per_class=30, size=32, seed=2)

# a cheap "embedding": downsample the image to 8x8 per channel and flatten
def embed(img):
    small = img[::4, ::4].astype(np.float32) / 255.0
    return small.reshape(-1)

vectors = np.stack([embed(img) for img in images])
norms = np.linalg.norm(vectors, axis=1, keepdims=True)
similarity = (vectors / norms) @ (vectors / norms).T
nearest = similarity[0].argsort()[::-1][1:4]
print("nearest neighbours of image 0:", nearest, "labels:", labels[nearest], "query:", labels[0])
```

Retrieval works with a feature map this crude; a pretrained encoder just works better. The pipeline —
embed, normalise, cosine, rank — is identical.

## 8. Practical Applications

- **Small-data domains** — medical, industrial and agricultural datasets where 200 labelled images is a
  good day; transfer learning is the only viable route.
- **Visual search** — product or document retrieval from an embedding index.
- **Accessibility** — captioning and visual question answering, with human review for consequential uses.
- **Quality assurance** — embedding drift detects when the incoming images stop resembling training data.

## 9. Common Mistakes

1. Fine-tuning with the pretrained learning rate, destroying the features you paid for.
2. Using ImageNet normalisation constants on images normalised differently.
3. Reporting a linear probe as if the whole backbone were trained.
4. Ignoring a checkpoint's licence until submission.
5. Treating a captioning model's output as verified fact.

## 10. Exercises

1. Fine-tune only the final layer of `TinyCNN` on a new class set and compare against training all layers
   with the same budget.
2. Compute attention cost for 16×16-pixel patches on a 224×224 image: how many tokens, how large is the
   attention matrix?
3. Build a retrieval demo with the crude embedding above and measure top-1 neighbour label accuracy.
4. Write the licence and provenance entry you would put in a report for a checkpoint you downloaded.

## 11. Self-Assessment

1. Why does a ViT need position embeddings but a CNN does not?
   *Attention is permutation-invariant, so patch order must be injected; convolution's sliding window
   already encodes relative position.*
2. What is the risk of freezing too many layers?
   *The frozen features may not represent the new domain, so the head cannot compensate.*
3. Why is cosine similarity preferred over Euclidean distance for embeddings?
   *It ignores vector magnitude, which is dominated by image brightness rather than content.*

## 12. Key Terms

**Transfer learning**, **fine-tuning**, **linear probe**, **Vision Transformer**, **patch embedding**,
**multimodal model**, **image embedding**, **cosine similarity**, **contrastive learning**. Definitions:
[glossary](../../../resources/glossary.md).

## 13. Further Reading

- Dosovitskiy et al. (2020), "An Image is Worth 16x16 Words" — the ViT paper.
- Radford et al. (2021), "Learning Transferable Visual Models From Natural Language Supervision" (CLIP).
- The model card of any checkpoint you use — read the licence before the abstract.

## What to Do Next

Finish the module with [LAB-09-04](../labs/lab-09-04-image-segmentation-with-unet.md) if you have not
already, then attempt [PA-09](../../../assessments/programming/pa-09-computer-vision.md)
and the [M09 quiz](../../../assessments/quizzes/quiz-m09.md).
