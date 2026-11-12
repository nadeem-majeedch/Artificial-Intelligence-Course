# Glossary — NLP and Vision (M08, M09)

Language processing and computer vision. M08 has reference code but no lessons; M09 has no
content at all. Their entries link to the module page and are marked **module page only**.
Back to the [glossary index](README.md).

## B

### Bag of words
**Abbreviation.** BoW · **Module.** M08
**Simple definition.** Representing a document by counts of its vocabulary words, ignoring order.
**Detailed explanation.** BoW is simple, sparse and surprisingly strong for topic and spam
classification. It loses word order and treats all words as equally distant, which is why
TF-IDF weighting and n-grams exist as partial repairs.
**Mathematics.** $\phi(d) = (c_1, \dots, c_{|V|})$ where $c_i$ counts term $i$ in document $d$.
**Practical example.** A support-ticket router on BoW + logistic regression reaches 0.86 macro F1
in milliseconds, and the top coefficients are readable words.
**Related.** [TF-IDF](#tf-idf), [Tokenisation](#tokenisation), [BM25](#bm25)
**Where it is taught.** Module page only — [M08 NLP](../../modules/M08-natural-language-processing/README.md)

### BM25
**Abbreviation.** BM25 · **Module.** M08
**Simple definition.** A lexical ranking function scoring documents by term overlap, with
saturation and length normalisation.
**Detailed explanation.** BM25 fixes two flaws of raw term counts: a term appearing 50 times is
not 50 times more relevant, and long documents should not win by length. It remains a strong
baseline for retrieval and is often fused with dense retrieval.
**Mathematics.** $\text{score}(q,d) = \sum_{t \in q} \text{IDF}(t)\cdot\frac{f_{t,d}(k_1+1)}{f_{t,d} + k_1(1-b+b\frac{|d|}{\text{avgdl}})}$
**Practical example.** In the M11 RAG notebook BM25 wins on exact identifiers (error codes, part
numbers) while dense retrieval wins on paraphrases.
**Related.** [TF-IDF](#tf-idf), [Retrieval-augmented generation](generative-ai.md#retrieval-augmented-generation), [Bag of words](#bag-of-words)
**Where it is taught.** Module page only — [M08 NLP](../../modules/M08-natural-language-processing/README.md)

## C

### Convolution
**Abbreviation.** — · **Module.** M09
**Simple definition.** Sliding a small learned filter over an image to produce a feature map.
**Detailed explanation.** Convolution encodes two priors: locality (nearby pixels interact) and
translation equivariance (a cat is a cat anywhere). Stacking convolutions with downsampling
builds a hierarchy from edges to textures to objects.
**Mathematics.** $y[i,j] = \sum_{m,n} x[i+m, j+n]\,w[m,n] + b$
**Practical example.** A 3×3 filter with 16 channels over a 32×32 RGB image produces a 30×30×16
map, using 448 parameters.
**Related.** [Pooling](deep-learning.md#pooling), [Object detection](#object-detection), [Image classification](#image-classification)
**Where it is taught.** Module page only — [M09 Computer Vision](../../modules/README.md#m09)

## I

### Image classification
**Abbreviation.** — · **Module.** M09
**Simple definition.** Assigning a label to a whole image.
**Detailed explanation.** The task is solved well by CNN or transformer backbones trained on
large labelled sets, and transfer learning makes it practical on small datasets. Accuracy hides
class imbalance and distribution shift, so per-class metrics and a confusion matrix are required.
**Mathematics.** $\hat{y} = \arg\max_c \text{softmax}(f_\theta(x))_c$
**Practical example.** Fine-tuning a pretrained backbone on 2,000 plant images reaches 0.94
accuracy against 0.71 from scratch.
**Related.** [Convolution](#convolution), [Object detection](#object-detection), [Transfer learning](deep-learning.md#transfer-learning)
**Where it is taught.** Module page only — [M09 Computer Vision](../../modules/README.md#m09)

### Intersection over Union
**Abbreviation.** IoU · **Module.** M09
**Simple definition.** The overlap between a predicted and a true region, divided by their union.
**Detailed explanation.** IoU is the standard measure for detection and segmentation quality: 1.0
is a perfect match, 0 is no overlap, and a threshold (commonly 0.5) converts it into a hit or a
miss. It penalises both missed area and spurious area.
**Mathematics.** $\text{IoU} = \dfrac{|A \cap B|}{|A \cup B|}$
**Practical example.** A 4×4 predicted box overlapping 12 of a 16-pixel ground-truth box gives
$\text{IoU} = 12/20 = 0.6$ — a hit at threshold 0.5, a miss at 0.75.
**Related.** [Object detection](#object-detection), [Image classification](#image-classification)
**Where it is taught.** Module page only — [M09 Computer Vision](../../modules/README.md#m09)

## O

### Object detection
**Abbreviation.** — · **Module.** M09
**Simple definition.** Locating objects in an image with bounding boxes and class labels.
**Detailed explanation.** Detection adds localisation to classification, so evaluation needs both
a class decision and an overlap threshold. One-stage detectors are fast; two-stage detectors are
more accurate on small objects.
**Mathematics.** mAP = mean over classes of the area under the precision–recall curve at a given IoU.
**Practical example.** A detector at mAP@0.5 = 0.62 finds most vehicles but misses 30% of
pedestrians at night — a per-class breakdown that a single mAP hides.
**Related.** [Intersection over Union](#intersection-over-union), [Convolution](#convolution)
**Where it is taught.** Module page only — [M09 Computer Vision](../../modules/README.md#m09)

## S

### Stemming and lemmatisation
**Abbreviation.** — · **Module.** M08
**Simple definition.** Reducing words to a common root (stemming) or dictionary form
(lemmatisation).
**Detailed explanation.** Both collapse inflection so "running" and "runs" match. Stemming chops
suffixes and can produce non-words; lemmatisation uses vocabulary and part of speech and is
slower but linguistically correct.
**Mathematics.** —
**Practical example.** A keyword search for "analyse" misses "analysing" unless the index is
stemmed; Porter stemming maps both to "analys".
**Related.** [Tokenisation](#tokenisation), [Bag of words](#bag-of-words)
**Where it is taught.** Module page only — [M08 NLP](../../modules/M08-natural-language-processing/README.md)

### Semantic segmentation
**Abbreviation.** — · **Module.** M09
**Simple definition.** Assigning a class to every pixel of an image.
**Detailed explanation.** Segmentation trades locality for detail: encoder–decoder architectures
downsample to capture context and upsample to recover boundaries, with skip connections carrying
fine detail. Evaluation uses per-class IoU.
**Mathematics.** $\text{mIoU} = \frac{1}{C}\sum_{c}\frac{|P_c \cap G_c|}{|P_c \cup G_c|}$
**Practical example.** A road-scene segmenter at mIoU 0.71 separates cars and pedestrians well but
confuses bicycle lanes with pavement.
**Related.** [Intersection over Union](#intersection-over-union), [Convolution](#convolution), [Object detection](#object-detection)
**Where it is taught.** Module page only — [M09 Computer Vision](../../modules/README.md#m09)


## T

### TF-IDF
**Abbreviation.** TF-IDF · **Module.** M08
**Simple definition.** Weighting a term by how often it appears in a document and how rare it is
across the corpus.
**Detailed explanation.** Common words carry little signal, so the inverse document frequency
down-weights them. The result is a sparse vector that is competitive for retrieval and
classification and remains interpretable.
**Mathematics.** $\text{tfidf}(t,d) = \text{tf}(t,d)\cdot\log\frac{N}{\text{df}(t)}$
**Practical example.** A term occurring in half the corpus contributes $\log 2 = 0.693$; one
occurring in a single document of 1,000 contributes 6.9 — ten times the weight.
**Related.** [Bag of words](#bag-of-words), [BM25](#bm25)
**Where it is taught.** Module page only — [M08 NLP](../../modules/M08-natural-language-processing/README.md)

### Tokenisation
**Abbreviation.** — · **Module.** M08
**Simple definition.** Splitting text into the units a model processes.
**Detailed explanation.** Word tokenisation is simple but blows up on typos and morphology;
subword tokenisation (BPE, WordPiece) keeps the vocabulary bounded and handles unseen words by
composition. The choice determines sequence length, cost and what counts as "rare".
**Mathematics.** $\text{BPE}$: repeatedly merge the most frequent adjacent symbol pair.
**Practical example.** A 37-symbol base alphabet with 18 merges yields a 55-symbol vocabulary in
the M11 tokeniser lab — a miniature of a 50,000-token production vocabulary.
**Related.** [Stemming and lemmatisation](#stemming-and-lemmatisation), [Bag of words](#bag-of-words), [Token](deep-learning.md#token)
**Where it is taught.** Module page only — [M08 NLP](../../modules/M08-natural-language-processing/README.md)

## W

### Word embedding
**Abbreviation.** — · **Module.** M08
**Simple definition.** A dense vector for a word, learned so that similar words are close.
**Detailed explanation.** Word2vec and GloVe established that distributional statistics encode
meaning, and that vector arithmetic captures relations. Context-free embeddings conflate senses;
contextual models (transformers) fixed that.
**Mathematics.** $\cos(e_a, e_b) = \frac{e_a \cdot e_b}{\lVert e_a\rVert\,\lVert e_b\rVert}$
**Practical example.** $\cos(\text{king} - \text{man} + \text{woman},\ \text{queen}) \approx 0.85$ on
a 300-dimensional embedding.
**Related.** [TF-IDF](#tf-idf), [Tokenisation](#tokenisation), [Embedding](deep-learning.md#embedding)
**Where it is taught.** Module page only — [M08 NLP](../../modules/M08-natural-language-processing/README.md)

### Named entity recognition
**Abbreviation.** NER · **Module.** M08
**Simple definition.** Finding and classifying names of people, organisations, places and similar
entities in text.
**Detailed explanation.** NER is usually framed as sequence labelling, where each token gets a tag
and the tags must be consistent (BIO scheme). It is a building block for relation extraction and
document routing.
**Mathematics.** $P(t_1,\dots,t_n \mid w_1,\dots,w_n)$ with constrained transitions.
**Practical example.** A contract pipeline extracts parties, dates and amounts, then routes the
document to the right reviewer.
**Related.** [Tokenisation](#tokenisation), [Word embedding](#word-embedding)
**Where it is taught.** Module page only — [M08 NLP](../../modules/M08-natural-language-processing/README.md)

---

[Glossary index](README.md) · [Deep learning](deep-learning.md) · [Reinforcement learning](reinforcement-learning.md) · [Quick reference](../glossary.md)
