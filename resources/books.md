# Books

An annotated reading list, ordered by what each book is actually good for. The course does not
require any of these — it is self-contained — but no single course is enough, and a good book is
still the best way to go deeper on one topic.

Several of the most useful texts are **free online**, which matters if cost is a barrier. Those are
marked 📖.

**Course home:** [README](../README.md) · **Glossary:** [glossary.md](glossary.md) ·
**Documentation:** [documentation.md](documentation.md) · **Papers:** [research-papers.md](research-papers.md)

## How to choose a book

1. **Match the book to the module you are struggling with**, not to your ambition. Buying five
   books and reading none is the usual outcome.
2. **Read the chapter that covers your problem**, then stop. Textbooks are references, not
   novels.
3. **Prefer the free option first.** If a free text explains the idea adequately, you have lost
   nothing.
4. **One book per topic is enough.** Different authors explain the same mathematics with different
   notation; collecting them creates confusion rather than clarity.

## Foundations of artificial intelligence

| Book | Level | Why read it |
| :--- | :--- | :--- |
| **Stuart Russell and Peter Norvig, *Artificial Intelligence: A Modern Approach*, 4th edition** (Pearson, 2020) | Intermediate | The standard reference for the whole field, and the source of the course's vocabulary and chapter structure. Use it as an encyclopaedia: read the section for whichever module you are in. 📖 Companion material, exercises and figures: [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/) |
| **Melanie Mitchell, *Artificial Intelligence: A Guide for Thinking Humans*** (Farrar, Straus and Giroux, 2019) | Beginner | A clear, sceptical tour of what AI can and cannot do, written for a general reader. The best single book to read *before* the course if you want the big picture first. |
| **Michael Wooldridge, *An Introduction to MultiAgent Systems*, 2nd edition** (Wiley, 2009) | Advanced | The formal treatment of agents and multi-agent interaction. Useful for M02 and M12, though M12's material on language-model agents postdates it. |
| **Judea Pearl, *Probabilistic Reasoning in Intelligent Systems*** (Morgan Kaufmann, 1988) | Advanced | The origin of Bayesian networks. Dense, but it explains *why* the representation is built the way it is. Read the first three chapters for M05. |

## Mathematics for AI

| Book | Level | Why read it |
| :--- | :--- | :--- |
| **Marc Peter Deisenroth, A. Aldo Faisal and Cheng Soon Ong, *Mathematics for Machine Learning*** (Cambridge University Press, 2020) | Intermediate | Written precisely for this gap: linear algebra, calculus, probability and optimisation, each motivated by a machine-learning application. 📖 Free PDF: [mml-book.github.io](https://mml-book.github.io/) |
| **Joseph K. Blitzstein and Jessica Hwang, *Introduction to Probability*, 2nd edition** (CRC Press, 2019) | Beginner | The clearest introduction to probability available, with intuition before formalism. Chapters 1–3 cover everything M05 assumes. 📖 Free PDF and course materials: [projects.iq.harvard.edu/stat110](https://projects.iq.harvard.edu/stat110) |
| **Gilbert Strang, *Linear Algebra and Its Applications*** (Cengage) | Beginner | If P02's approach does not suit you, Strang's is the classic alternative, with lectures available alongside. |

## Machine learning

| Book | Level | Why read it |
| :--- | :--- | :--- |
| **Christopher M. Bishop, *Pattern Recognition and Machine Learning*** (Springer, 2006) | Advanced | The rigorous probabilistic view of machine learning. Beautiful and demanding; use it when you want the derivation behind M06's algorithms. |
| **Trevor Hastie, Robert Tibshirani and Jerome Friedman, *The Elements of Statistical Learning*, 2nd edition** (Springer, 2009) | Advanced | The statistical-learning reference: bias–variance, regularisation, trees and ensembles, explained with unusual care. 📖 Free PDF: [hastie.su.domains/ElemStatLearn](https://hastie.su.domains/ElemStatLearn/) |
| **Kevin P. Murphy, *Probabilistic Machine Learning: An Introduction*** (MIT Press, 2022) | Advanced | A modern, unified treatment covering both classical methods and deep learning. The best single book to grow into after this course. 📖 Draft chapters: [probml.github.io](https://probml.github.io/) |
| **Aurélien Géron, *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*, 3rd edition** (O'Reilly, 2022) | Beginner | Practical and well organised. Best used alongside M06 and M07 for its worked pipelines and code, not as a substitute for the theory. |
| **Sebastian Raschka and Yuxi (Hayden) Liu, *Machine Learning with PyTorch and Scikit-Learn*** (Packt, 2022) | Beginner | A PyTorch-first companion if you prefer learning the framework while you learn the concepts. |
| **Shai Shalev-Shwartz and Shai Ben-David, *Understanding Machine Learning: From Theory to Algorithms*** (Cambridge University Press, 2014) | Advanced | Where generalisation comes from, formally. Read it if you want to know why the bias–variance story is true rather than merely useful. 📖 Free PDF: [cs.huji.ac.il/~shais/UnderstandingMachineLearning](https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/) |

## Deep learning

| Book | Level | Why read it |
| :--- | :--- | :--- |
| **Ian Goodfellow, Yoshua Bengio and Aaron Courville, *Deep Learning*** (MIT Press, 2016) | Advanced | The foundational text. Pre-transformer, but the chapters on optimisation, regularisation and convolutional networks remain the clearest treatment anywhere. 📖 Free HTML: [deeplearningbook.org](https://www.deeplearningbook.org/) |
| **Simon J. D. Prince, *Understanding Deep Learning*** (MIT Press, 2023) | Intermediate | The most readable rigorous account of modern deep learning, including transformers and diffusion. The best single book for M07 and M11. 📖 Free PDF: [udlbook.github.io](https://udlbook.github.io/udlbook/) |
| **François Chollet, *Deep Learning with Python*, 2nd edition** (Manning, 2021) | Beginner | Learn-by-building, from the author of Keras. Good for the practical instincts that the course's from-scratch exercises do not teach. |
| **Aston Zhang, Zachary C. Lipton, Mu Li and Alexander J. Smola, *Dive into Deep Learning*** (online, updated) | Intermediate | An executable book: every concept comes with runnable code. 📖 Free: [d2l.ai](https://d2l.ai/) |

## Natural language processing

| Book | Level | Why read it |
| :--- | :--- | :--- |
| **Daniel Jurafsky and James H. Martin, *Speech and Language Processing*, 3rd edition draft** | Intermediate | The standard NLP reference, continually updated to cover language models. Chapters on tokenisation, embeddings and transformers map directly onto M08 and M11. 📖 Free online: [web.stanford.edu/~jurafsky/slp3](https://web.stanford.edu/~jurafsky/slp3/) |
| **Jacob Eisenstein, *Introduction to Natural Language Processing*** (MIT Press, 2019) | Advanced | A more formal, methods-first treatment. Useful if you want the mathematical framing behind the pipeline. |

## Reinforcement learning

| Book | Level | Why read it |
| :--- | :--- | :--- |
| **Richard S. Sutton and Andrew G. Barto, *Reinforcement Learning: An Introduction*, 2nd edition** (MIT Press, 2018) | Intermediate | The definitive text, and unusually well written. M10 follows its structure closely. 📖 Free PDF: [incompleteideas.net/book/the-book-2nd.html](http://incompleteideas.net/book/the-book-2nd.html) |

## Python and data handling

| Book | Level | Why read it |
| :--- | :--- | :--- |
| **Allen B. Downey, *Think Python*** (Green Tea Press / O'Reilly) | Beginner | The gentlest serious introduction to programming, written for people who have never coded. Use it if P01 moves too fast. 📖 Free online: [allendowney.github.io/ThinkPython](https://allendowney.github.io/ThinkPython/) |
| **Jake VanderPlas, *Python Data Science Handbook*** (O'Reilly) | Beginner | NumPy, pandas, Matplotlib and scikit-learn, explained with excellent examples. The best companion for P04 and M06. 📖 Free online: [jakevdp.github.io/PythonDataScienceHandbook](https://jakevdp.github.io/PythonDataScienceHandbook/) |
| **Al Sweigart, *Automate the Boring Stuff with Python*, 2nd edition** (No Starch Press, 2019) | Beginner | Programming taught through useful tasks. Good motivation if you are learning Python for the first time. 📖 Free online: [automatetheboringstuff.com](https://automatetheboringstuff.com/) |

## Responsible and explainable AI

| Book | Level | Why read it |
| :--- | :--- | :--- |
| **Christoph Molnar, *Interpretable Machine Learning*** (online, 2nd edition) | Intermediate | The practical reference for explanation methods: permutation importance, SHAP, LIME, surrogate models. Maps directly onto M13. 📖 Free online: [christophm.github.io/interpretable-ml-book](https://christophm.github.io/interpretable-ml-book/) |
| **Cathy O'Neil, *Weapons of Math Destruction*** (Crown, 2016) | Beginner | How algorithmic scoring goes wrong in practice: policing, hiring, education, insurance. Read it before M13 — the case studies make the technical material matter. |
| **Brian Christian, *The Alignment Problem*** (W. W. Norton, 2020) | Beginner | The ideas behind alignment, reward hacking and specification, told through the people who developed them. The best non-technical preparation for M10 and M11. |
| **Ruha Benjamin, *Race After Technology*** (Polity, 2019) | Beginner | How technical systems encode social inequality. A useful counterweight to purely metric views of fairness in M13. |

## Building your own library

If you can only choose four, choose these: **AIMA** (the field), **Deisenroth et al.** (the
mathematics), **Prince** (modern deep learning), and **Molnar** (explanation). All four are either
free online or widely available in university libraries.

**Navigation:** [Course home](../README.md) · [Glossary](glossary.md) ·
[Documentation](documentation.md) · [Research papers](research-papers.md) ·
[Modules](../modules/README.md) · [FAQ](../docs/faq.md)
