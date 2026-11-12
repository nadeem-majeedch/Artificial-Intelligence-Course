# Documentation

The authoritative references for the languages and libraries this course uses. This is a working
page: keep it open while you code rather than reading it end to end.

**Course home:** [README](../README.md) · **Books:** [books.md](books.md) ·
**Papers:** [research-papers.md](research-papers.md) · **Glossary:** [glossary.md](glossary.md)

## How to use documentation well

1. **Start with the user guide, not the API reference.** Guides explain the idea and the intended
   workflow; the API reference tells you the arguments of one function. Beginners read the
   reference first and conclude the library is incomprehensible.
2. **Read the example, then modify it.** Copy the smallest example that resembles your problem,
   run it, then change one thing at a time.
3. **Check the version.** A tutorial written for an older release may use functions that have been
   renamed or removed. The version is shown in the documentation's header.
4. **Trust the docstring over the blog post.** If they disagree, the source wins.
5. **When an error is unclear, search the exact error message** in the library's issue tracker. Most
   errors you will meet have been met, and answered, before.

## Python

| Resource | Use it for |
| :--- | :--- |
| [The Python Tutorial](https://docs.python.org/3/tutorial/) | Learning the language from the source. Chapters 3–9 cover everything P01 teaches. |
| [The Python Standard Library](https://docs.python.org/3/library/) | Built-in modules: `pathlib`, `json`, `csv`, `math`, `random`, `itertools`, `collections`. |
| [PEP 8 — Style Guide](https://peps.python.org/pep-0008/) | How to write Python that other people can read. The course follows it. |
| [PEP 484 — Type Hints](https://peps.python.org/pep-0484/) | The syntax behind the type annotations used in course code. |

## Numerical and data libraries

| Resource | Use it for |
| :--- | :--- |
| [NumPy user guide](https://numpy.org/doc/stable/user/) | Arrays, broadcasting, indexing, random generators. The foundation for everything else. |
| [NumPy API reference](https://numpy.org/doc/stable/reference/) | Exact behaviour of `np.linalg`, `np.random`, reductions and dtypes. |
| [pandas user guide](https://pandas.pydata.org/docs/user_guide/) | Loading, selecting, grouping, joining, missing data, time series. |
| [pandas API reference](https://pandas.pydata.org/docs/reference/) | Method signatures when you know what you want but not its exact name. |
| [Matplotlib tutorials](https://matplotlib.org/stable/tutorials/) | Figures, axes, subplots and styling from first principles. |
| [Matplotlib gallery](https://matplotlib.org/stable/gallery/) | Find the plot you want, copy the code, adapt it. |
| [SciPy reference](https://docs.scipy.org/doc/scipy/) | Optimisation, statistics, linear algebra and signal routines beyond NumPy. |
| [NetworkX documentation](https://networkx.org/documentation/stable/) | Graphs for search, Bayesian networks and knowledge graphs. |

## Machine learning

| Resource | Use it for |
| :--- | :--- |
| [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html) | The best-written machine-learning documentation in existence. Read the chapters on model selection, preprocessing and metrics — they are the course's M06 in reference form. |
| [scikit-learn API reference](https://scikit-learn.org/stable/modules/classes.html) | Estimator signatures, parameters and attributes. |
| [scikit-learn examples](https://scikit-learn.org/stable/auto_examples/index.html) | Complete, runnable pipelines for nearly every algorithm taught in M06. |

## Deep learning

| Resource | Use it for |
| :--- | :--- |
| [PyTorch tutorials](https://pytorch.org/tutorials/) | Tensors, autograd, training loops, data loading — the "60-minute blitz" is the fastest useful start. |
| [PyTorch API reference](https://pytorch.org/docs/stable/index.html) | `torch.nn`, `torch.optim`, `torch.utils.data`, reductions and dtypes. |
| [PyTorch recipes](https://pytorch.org/tutorials/recipes/recipes_index.html) | Short, task-shaped answers: saving a model, freezing layers, profiling. |
| [Hugging Face Transformers](https://huggingface.co/docs/transformers/) | Pretrained models, tokenizers, fine-tuning and pipelines. The reference for M08 and M11. |
| [Hugging Face Datasets](https://huggingface.co/docs/datasets/) | Loading and processing datasets, including streaming. |
| [Hugging Face course](https://huggingface.co/learn) | A structured, free course that complements M08's transformer material. |

## Reinforcement learning

| Resource | Use it for |
| :--- | :--- |
| [Gymnasium documentation](https://gymnasium.farama.org/) | The standard environment interface: `reset`, `step`, spaces, wrappers. The reference for M10. |
| [Gymnasium environments](https://gymnasium.farama.org/environments/classic_control/) | Classic control tasks — cart-pole, mountain car — used in the M10 labs. |

## Notebooks and environments

| Resource | Use it for |
| :--- | :--- |
| [Jupyter documentation](https://docs.jupyter.org/) | Installing, running and configuring notebooks. |
| [Jupyter Notebook interface guide](https://jupyter-notebook.readthedocs.io/en/stable/) | Cells, kernels, keyboard shortcuts, restarting and running all. |
| [Google Colab FAQ](https://research.google.com/colaboratory/faq.html) | Free hosted notebooks, when installing locally is impractical. |
| [VS Code — Jupyter](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) | Running `.ipynb` files inside an editor, with debugging. |

## Reference works

| Resource | Use it for |
| :--- | :--- |
| [arXiv](https://arxiv.org/) | Preprints; every paper in the course's reading list is here. |
| [Papers with Code](https://paperswithcode.com/) | Papers linked to implementations and benchmark results. Useful when you want to see how a method is actually built. |
| [Google Machine Learning Glossary](https://developers.google.com/machine-learning/glossary) | Alternative definitions of machine-learning terms, useful for cross-checking. |

## A note on tutorials and videos

Video courses and blog tutorials are excellent for installation problems and for a second
explanation of one specific idea. They are weak at teaching you to reason, because you cannot pause
a video to derive something yourself. Use them to unblock a specific point, then return to the
lesson and the notebook.

**Navigation:** [Course home](../README.md) · [Books](books.md) ·
[Research papers](research-papers.md) · [Glossary](glossary.md) ·
[Modules](../modules/README.md)
