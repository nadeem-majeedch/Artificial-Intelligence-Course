# Official Documentation

The authoritative references for every library the course uses. Official documentation is the only
source that cannot be out of date with the installed version, and the only one whose examples are
tested by the maintainers.

Keep this page open while coding. Read the user guide first, the API reference second.

[Library index](../README.md) · [Textbooks](textbooks.md) · [OER](open-educational-resources.md)

---

## Python

### The Python Tutorial
**Python Software Foundation** · current stable release
- **URL:** https://docs.python.org/3/tutorial/
- **Modules:** P01, M01 · **Level:** Beginner
- **Why:** The language taught by its maintainers, from data structures to errors and classes. Chapters 3–9 cover everything P01 assumes.
- **Access:** Free; Python documentation is published under the PSF licence.

### The Python Standard Library
**Python Software Foundation** · current stable release
- **URL:** https://docs.python.org/3/library/
- **Modules:** P01, P04, M10–M14 · **Level:** Beginner
- **Why:** The reference for `pathlib`, `json`, `csv`, `random`, `itertools`, `collections` and `unittest` — the modules the assignments expect you to know.
- **Access:** Free; PSF licence.

### PEP 8 — Style Guide for Python Code
**Python Software Foundation** · active
- **URL:** https://peps.python.org/pep-0008/
- **Modules:** P01 · **Level:** Beginner
- **Why:** The conventions the course code follows, and the reason your linter complains. Read it once; skim the naming sections thereafter.
- **Access:** Free; PSF licence.

## Numerical and data libraries

### NumPy user guide
**NumPy developers** · current stable
- **URL:** https://numpy.org/doc/stable/user/
- **Modules:** P02, P04, M06–M09 · **Level:** Beginner
- **Why:** Arrays, broadcasting, indexing and random generators explained in order. Broadcasting is the concept most students get wrong; read that section twice.
- **Access:** Free; NumPy is BSD-3-Clause licensed and its docs are openly available.

### NumPy: absolute beginners and quickstart
**NumPy developers**
- **URL:** https://numpy.org/doc/stable/user/absolute_beginners.html
- **Modules:** P02 · **Level:** Beginner
- **Why:** The shortest path from Python lists to vectorised array code, with runnable examples. Use it before PA-01.
- **Access:** Free; BSD-3-Clause project.

### pandas user guide
**pandas developers** · current stable
- **URL:** https://pandas.pydata.org/docs/user_guide/
- **Modules:** P04, M06, PA-01 · **Level:** Beginner
- **Why:** Loading, selecting, grouping, joining and handling missing data. The "groupby" and "missing data" chapters are the ones assignments actually need.
- **Access:** Free; pandas is BSD-3-Clause licensed.

### Matplotlib tutorials and gallery
**Matplotlib developers** · current stable
- **URL:** https://matplotlib.org/stable/tutorials/
- **Modules:** P04, M06–M14 · **Level:** Beginner
- **Why:** Figures, axes and subplots from first principles; the gallery is where you find the plot you want and adapt its code.
- **Access:** Free; Matplotlib is PSF-based/BSD-compatible and openly documented.

## Machine learning

### scikit-learn user guide
**scikit-learn developers** · current stable
- **URL:** https://scikit-learn.org/stable/user_guide.html
- **Modules:** M06, M13 · **Level:** Intermediate
- **Why:** The best-written machine-learning documentation in existence. The chapters on model selection, preprocessing and metrics are M06 in reference form.
- **Access:** Free; scikit-learn is BSD-3-Clause licensed.

### scikit-learn API reference
**scikit-learn developers**
- **URL:** https://scikit-learn.org/stable/modules/classes.html
- **Modules:** M06 · **Level:** Intermediate
- **Why:** Estimator signatures, parameters and attributes when you know what you want but not its exact name.
- **Access:** Free; BSD-3-Clause.

### scikit-learn examples
**scikit-learn developers**
- **URL:** https://scikit-learn.org/stable/auto_examples/index.html
- **Modules:** M06, M13 · **Level:** Intermediate
- **Why:** Complete, runnable pipelines for nearly every algorithm in M06, including the fairness and calibration examples. Copy, run, then modify.
- **Access:** Free; BSD-3-Clause.

## Deep learning

### PyTorch tutorials
**PyTorch Foundation / Meta** · current stable
- **URL:** https://pytorch.org/tutorials/
- **Modules:** M07, M09, M10, M11 · **Level:** Intermediate
- **Why:** Tensors, autograd, training loops and data loading, plus the "60-minute blitz" that is the fastest useful start. The RL and vision tutorials are directly usable.
- **Access:** Free; PyTorch is BSD-3-Clause licensed.

### PyTorch API reference
**PyTorch Foundation**
- **URL:** https://pytorch.org/docs/stable/index.html
- **Modules:** M07, M11 · **Level:** Intermediate
- **Why:** `torch.nn`, `torch.optim`, `torch.utils.data`, dtypes and device handling. The place to check whether a function returns a tuple before you unpack it.
- **Access:** Free; BSD-3-Clause.

### TensorFlow tutorials
**Google** · current stable
- **URL:** https://www.tensorflow.org/tutorials
- **Modules:** M07, M09 · **Level:** Intermediate
- **Why:** End-to-end examples for training, saving and serving models, including the Keras integration. Use it if your capstone deploys to a TensorFlow-serving stack.
- **Access:** Free; TensorFlow is Apache-2.0 licensed.

### Keras guides and API
**Keras team (Google)** · current release
- **URL:** https://keras.io/guides/
- **Modules:** M07, M09 · **Level:** Beginner
- **Why:** The highest-level way to build a network: layers, training loops, callbacks, saving. The "Keras for beginners" guides are the shortest path to a working model.
- **Access:** Free; Keras is Apache-2.0 licensed.

### Hugging Face Transformers documentation
**Hugging Face** · current release
- **URL:** https://huggingface.co/docs/transformers/
- **Modules:** M08, M11 · **Level:** Intermediate
- **Why:** Pretrained models, tokenisers, pipelines and fine-tuning, with a task-oriented guide for each. The reference for everything in M11 that uses a pretrained checkpoint.
- **Access:** Free; the library is Apache-2.0 licensed.

### Hugging Face Datasets and PEFT
**Hugging Face**
- **URL:** https://huggingface.co/docs/datasets/
- **Modules:** M06, M08, M11 · **Level:** Intermediate
- **Why:** Loading and processing datasets, and parameter-efficient fine-tuning (LoRA and friends) with a few lines. Read PEFT alongside the LoRA section of L11-06.
- **Access:** Free; Apache-2.0.

### OpenCV Python tutorials
**OpenCV team** · 4.x
- **URL:** https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- **Modules:** M09 · **Level:** Beginner
- **Why:** Images as arrays, colour conversion, filtering, edges, contours and video capture, each with a short Python example. The practical half of M09.
- **Access:** Free; OpenCV is Apache-2.0 licensed since 4.5.

### OpenCV API reference
**OpenCV team** · 4.x
- **URL:** https://docs.opencv.org/4.x/
- **Modules:** M09 · **Level:** Intermediate
- **Why:** Exact parameter names and flag constants for the functions the tutorials introduce. The Python signatures are under each C++ entry.
- **Access:** Free; Apache-2.0.

## Reinforcement learning environments

### Gymnasium documentation
**Farama Foundation** · current release
- **URL:** https://gymnasium.farama.org/
- **Modules:** M10 · **Level:** Intermediate
- **Why:** The standard environment interface — `reset`, `step`, spaces, wrappers — that the M10 labs use. Read the basic usage page before writing your first loop.
- **Access:** Free; Gymnasium is MIT licensed.

### Stable-Baselines3 documentation
**DLR-RM and contributors** · current release
- **URL:** https://stable-baselines3.readthedocs.io/
- **Modules:** M10 · **Level:** Intermediate
- **Why:** Reliable PPO, A2C, DQN and SAC implementations with tuned defaults. Useful as a baseline to compare your from-scratch agent against.
- **Access:** Free; MIT licensed.

## Notebooks and environment

### Jupyter documentation
**Project Jupyter** · current release
- **URL:** https://docs.jupyter.org/
- **Modules:** P01–M14 · **Level:** Beginner
- **Why:** Installing, running and configuring notebooks, including kernels and `nbconvert`. The FAQ answers most "why did my cell hang" questions.
- **Access:** Free; Jupyter is BSD-3-Clause licensed.

---

[Library index](../README.md) · [Textbooks](textbooks.md) · [OER](open-educational-resources.md) · [Agents](ai-agents.md)
