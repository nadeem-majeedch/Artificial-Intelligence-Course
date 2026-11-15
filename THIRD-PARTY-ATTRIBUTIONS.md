# Third-Party Attributions

This register records material in or required by the course that the author does **not** own. Such
material keeps its own licence and is **not covered** by the course's MIT, CC BY 4.0 or CC0 grants;
none of it is relicensed by [LICENSE](LICENSE), [CONTENT-LICENSE.md](CONTENT-LICENSE.md) or
[DATASET-LICENSE.md](DATASET-LICENSE.md).

**Repository content:** original code, original prose, original synthetic data, and no committed
third-party code, images, diagrams or datasets. The third-party surface is:

1. software dependencies installed by the reader;
2. optional datasets and pretrained model weights downloaded at runtime;
3. bibliographic references, cited rather than redistributed;
4. short quotations used for teaching and criticism.

**Verification date for the upstream sources below: 15 November 2026.**

---

## 1. Software dependencies

Installed by the reader; not vendored, copied or modified in this repository. Versions are those
observed in the release-validation environment and are not pinned by a lockfile.

| Package | Version observed | Licence | Used for | Attribution requirement |
| --- | --- | --- | --- | --- |
| NumPy | 2.5.3 | BSD-3-Clause | Arrays and numerics throughout | Retain copyright/licence notice in redistributed copies |
| SciPy | 1.18.1 | BSD-3-Clause | `convolve2d` reference in vision, statistics | Same |
| pandas | 3.0.6 | BSD-3-Clause | Tabular datasets | Same |
| matplotlib | 3.11.2 | PSF-based matplotlib licence | Plots in notebooks | Same |
| PyTorch | 2.14.1+cpu | BSD-3-Clause | Neural-network modules, notebooks | Same |
| Gymnasium | 1.4.0 | MIT | CartPole and FrozenLake benchmarks | Retain notice |
| transformers | 5.18.0 | Apache-2.0 | Optional pretrained-model demonstrations | Retain NOTICE where applicable |
| scikit-learn | 1.9.1 | BSD-3-Clause | Classical ML, evaluation, digits loader | Same |
| sentence-transformers | 6.1.0 | Apache-2.0 | Optional embedding demo (M11) | Retain NOTICE |
| `datasets` | 5.2.0 | Apache-2.0 | Optional Hugging Face dataset loader | Retain NOTICE |
| pytest | 9.1.1 | MIT | Test suite | Retain notice |
| PyYAML | 6.0.3 | MIT | Citation/metadata validation | Retain notice |
| nbclient / nbformat | 0.11.0 / 5.11.1 | BSD-3-Clause | Notebook execution audit | Same |
| tqdm | 4.70.1 | MPL-2.0 AND MIT | Progress bars (transitive via transformers) | Retain notices |

`torchvision` is referenced in M07 documentation as an optional path but is not installed in the
validation environment and is not required for any executed notebook. Dependency versions are
observations, not a supported-version lock.

## 2. Datasets not redistributed

None of these is committed to the repository. They are loaded by a library or downloaded by the
reader, who accepts the upstream terms at that point.

| Dataset | Upstream and verification | Licence | How it appears here | Attribution / notes |
| --- | --- | --- | --- | --- |
| UCI optical digits (`load_digits`) | [UCI dataset 80](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits), DOI [10.24432/C50P49](https://doi.org/10.24432/C50P49); verified 2026-11-15 | **CC BY 4.0** (dataset); BSD-3-Clause (scikit-learn loader) | Loaded at runtime by M07/M14; no rows committed | Cite Alpaydin & Kaynak (1998) and UCI; do not present as course-authored or CC0 |
| Iris | [UCI dataset 53](https://archive.ics.uci.edu/dataset/53/iris), DOI [10.24432/C56C76](https://doi.org/10.24432/C56C76); verified 2026-11-15 | **CC BY 4.0** | Referenced as the real-world counterpart of a synthetic dataset; no rows copied | Cite R. A. Fisher / UCI |
| Fashion-MNIST | Xiao, Rasul & Vollgraf (2017), [arXiv:1708.07747](https://arxiv.org/abs/1708.07747) | Dataset repository: MIT; images distributed for research use | Optional local IDX files read by `deep_data.py`; synthetic texture stand-in when absent | Cite Xiao et al. and the Zalando repository; verify before bundling |
| CartPole-v1 / FrozenLake-v1 | [Gymnasium](https://gymnasium.farama.org/) / Farama Foundation | MIT (code); environments are implementations, not data | Instantiated at runtime in M10 and tests | Cite Gymnasium/Farama Foundation |

The previous UCI uncertainty is resolved: both dataset pages state CC BY 4.0 and provide the DOIs
above. No UCI rows are redistributed. M11, M13 and M14 now describe `load_digits` as CC BY 4.0, not
public domain.

## 3. Pretrained models (runtime downloads)

Weights are **not committed**. The licences and URLs below were read from the public Hugging Face
model cards on 15 November 2026. They are recorded per model, not inferred from the model family or
the downloading library.

| Model | Licence | Authoritative model card | Where used | Recorded restrictions / notes |
| --- | --- | --- | --- | --- |
| `google/flan-t5-small` | **Apache-2.0** | <https://huggingface.co/google/flan-t5-small> | M11 RAG/evaluation demonstration | Model card describes research use and says the model should not be used directly in an application without a safety and fairness assessment; unacceptable uses such as abusive generation are excluded |
| `distilgpt2` | **Apache-2.0** | <https://huggingface.co/distilbert/distilgpt2> | M11 token/attention and generation demonstrations | Model card records bias and out-of-scope uses inherited from GPT-2, including uses requiring generated text to be true |
| `gpt2` | **MIT** | <https://huggingface.co/openai-community/gpt2> | Optional M11 generation comparison | Model card records bias and limitations; training data is not a browsable released dataset |
| `t5-small` | **Apache-2.0** | <https://huggingface.co/google-t5/t5-small> | Optional M11 sequence-to-sequence demonstration | Standard T5 model-card limitations |
| `distilbert-base-uncased` | **Apache-2.0** | <https://huggingface.co/distilbert/distilbert-base-uncased> | M07/M08 optional transfer-learning demonstration | Model-card limitations apply |
| `sentence-transformers/all-MiniLM-L6-v2` | **Apache-2.0** | <https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2> | M11 retrieval/embedding demonstration | Intended as a sentence and short-paragraph encoder; inputs over 256 word pieces are truncated by default |

A permissive weight licence does not grant rights over training data, and it does not automatically
determine the copyright status of model outputs. Re-check the model card before redistributing
weights, fine-tunes or derived model files.

## 4. Model outputs and generated material

There is no general rule that model outputs carry the same licence as model weights. The course
therefore does **not** relicense pretrained-model outputs and makes no ownership claim over them.

- Committed sample data in `modules/M11-…/code/gen_samples.npz` comes from VAE, GAN and DDPM models
  trained from scratch on course-generated digits; it is treated as original generated data under
  CC0 1.0.
- Notebook outputs that call a pretrained checkpoint are runtime illustrations. They may be short,
  non-substantial generations; they are not presented as course-authored prose.
- No long verbatim extraction from a pretrained model is intentionally committed. Spot checks found
  no such passage, but this is not an exhaustive legal review.
- A reader reusing an output is responsible for the model's terms and for any third-party material
  the output may reproduce.

## 5. Bibliographic references and quotations

`resources/research-papers.md`, `resources/library/papers-and-surveys.md` and
`resources/library/ai-agents.md` contain **95 bibliographic entries**. They are citations and links,
not copies:

- no paper PDFs, figures or long excerpts are stored;
- paywalled papers are linked or named, never reproduced;
- short attributed quotations used in lessons remain the property of their authors and are used for
  teaching, criticism and identification;
- a citation does not establish permission to redistribute the cited work.

**Quotation policy.** Use only the shortest passage needed to identify or criticise a source, keep
the author and work attached, and link to the source. Do not reproduce a paper's argument,
substantial passage, table, figure or code as a substitute for the original. Any quotation longer
than a sentence should be reviewed by the owner before publication; the release audit sampled
lessons but did not conduct an exhaustive line-by-line copyright review.

## 6. Images, diagrams and code snippets

- **No binary image assets** exist in the repository (0 `.png`, `.jpg`, `.svg`, `.gif`).
- Diagrams are Mermaid text or Markdown tables authored for the course, covered by CC BY 4.0.
- Notebook images are generated procedurally by course code (M09) or by matplotlib from synthetic
  data; no third-party image is embedded.
- No third-party source code is copied. Where an algorithm follows a paper, the paper is cited; the
  implementation is course-authored and MIT-licensed.

## 7. Attribution obligations for redistributors

If you redistribute this repository or a derived course:

1. Keep [LICENSE](LICENSE) with the code and the MIT notice intact.
2. Keep the CC BY 4.0 attribution block from [CONTENT-LICENSE.md](CONTENT-LICENSE.md).
3. Do **not** apply MIT, CC BY 4.0 or CC0 to third-party material listed above.
4. If you bundle UCI digits, Fashion-MNIST or another dataset, add its citation and comply with its
   current terms; the course's CC0 dedication does not travel with it.
5. If you redistribute model weights, fine-tunes or model files, check the model card yourself.

## 8. Owner review status

| Item | Status | Remaining action |
| --- | --- | --- |
| `google/flan-t5-small` licence | **Resolved 2026-11-15**: Apache-2.0 on the current model card | Observe the model card's safety and acceptable-use caveats; no weight redistribution is planned |
| UCI digits and Iris licence | **Resolved 2026-11-15**: both CC BY 4.0, DOI recorded | Preserve citations; do not describe as public domain |
| Other pretrained models | **Resolved 2026-11-15**: licences and URLs in §3 | Re-check before redistributing weights or fine-tunes |
| Model outputs | **Policy recorded** in §4 | Owner should confirm the policy is acceptable for the intended publication; no general legal clearance is claimed |
| Quotations | **Policy recorded** in §5 | Owner should review any quotation longer than a sentence; no exhaustive copyright review was performed |
| Chain of title / contributor consent | **Open** | Complete [OWNERSHIP-REVIEW-CHECKLIST.md](OWNERSHIP-REVIEW-CHECKLIST.md); a single-author Git history is evidence of authorship, not a signed chain of title |
| Dependency versions | **Recorded, not pinned** | Consider a tested environment file or lockfile if exact reproduction is required |

Nothing in this register grants a licence to third-party material, and nothing here is legal
advice. Mechanical checks confirm internal consistency, not legal clearance.
