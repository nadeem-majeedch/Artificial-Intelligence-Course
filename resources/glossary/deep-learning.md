# Glossary — Deep Learning (M07)

Neural networks, training mechanics and architectures. Back to the [glossary index](README.md).

## A

### Activation function
**Abbreviation.** — · **Module.** M07
**Simple definition.** An elementwise nonlinear function applied to a layer's output.
**Detailed explanation.** Without nonlinearity a stack of linear layers is one linear layer, no
matter how deep. ReLU trains fast but can kill units; sigmoid and tanh saturate; the choice
changes optimisation behaviour, not representational power in theory.
**Mathematics.** $\text{ReLU}(z) = \max(0, z)$; $\sigma(z) = \frac{1}{1+e^{-z}}$
**Practical example.** A two-layer XOR network with a linear activation cannot exceed 50%
accuracy however long it trains; swapping in tanh reaches 100% in a few hundred epochs.
**Related.** [Multilayer perceptron](#multilayer-perceptron), [Backpropagation](#backpropagation)
**Where it is taught.** [L07-01 From perceptron to MLP](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-01-from-perceptron-to-mlp.md)

### Attention
**Abbreviation.** — · **Module.** M07
**Simple definition.** Weighting parts of the input by relevance when producing each output.
**Detailed explanation.** Attention computes a query–key similarity, turns it into weights, and
takes a weighted sum of values. It removes the sequential bottleneck of recurrence, which is why
it trains in parallel and why transformers replaced RNNs for language.
**Mathematics.** $\text{Attn}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$
**Practical example.** Translating "the animal did not cross the street because it was too
tired", attention places most weight of "it" on "animal" rather than "street".
**Related.** [Transformer](#transformer), [Recurrent neural network](#recurrent-neural-network), [Embedding](#embedding)
**Where it is taught.** [L07-07 Attention and transformers](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-07-attention-and-transformers.md)

## B

### Backpropagation
**Abbreviation.** Backprop · **Module.** M07
**Simple definition.** Applying the chain rule backwards through a network to get every
parameter's gradient.
**Detailed explanation.** The forward pass caches activations; the backward pass propagates the
loss gradient layer by layer, reusing those caches. It is reverse-mode automatic
differentiation specialised to a computation graph, and it costs about twice a forward pass.
**Mathematics.** $\frac{\partial L}{\partial W^{(l)}} = \delta^{(l)} (a^{(l-1)})^\top$, with $\delta^{(l)} = (W^{(l+1)\top}\delta^{(l+1)}) \odot f'(z^{(l)})$
**Practical example.** In the M07 from-scratch lab the hand-written backward pass is checked
numerically and agrees to a maximum relative error of 1.22e-08.
**Related.** [Gradient check](#gradient-check), [Activation function](#activation-function), [Multilayer perceptron](#multilayer-perceptron)
**Where it is taught.** [L07-02 Backpropagation: the mathematics of learning](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-02-backpropagation-the-mathematics-of-learning.md)

### Batch normalisation
**Abbreviation.** BatchNorm · **Module.** M07
**Simple definition.** Normalising each layer's pre-activations using the current mini-batch
statistics.
**Detailed explanation.** It stabilises and speeds training and permits higher learning rates.
At inference it uses running estimates, which is why train and eval modes differ and why a bug
here produces quietly wrong predictions.
**Mathematics.** $\hat{z} = \frac{z - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}$, then $\gamma\hat{z} + \beta$.
**Practical example.** Adding BatchNorm to a 12-layer CNN cuts epochs to reach 90% accuracy from
40 to 18 on the same data.
**Related.** [Regularisation](#regularisation-deep-learning), [Learning rate](#learning-rate)
**Where it is taught.** [L07-03 Training in practice](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-03-training-in-practice.md)

## C

### Convolutional neural network
**Abbreviation.** CNN · **Module.** M07
**Simple definition.** A network that applies small learned filters across the input, exploiting
local structure and translation invariance.
**Detailed explanation.** Weight sharing makes CNNs dramatically cheaper than dense layers on
images and encodes the prior that nearby pixels matter together. Pooling or striding reduces
resolution progressively, building a hierarchy from edges to objects.
**Mathematics.** $(f * g)(i,j) = \sum_{m}\sum_{n} f(i+m, j+n)\,g(m,n)$
**Practical example.** A 3×3 filter over a 32×32×3 image with 16 output channels has
$3\cdot3\cdot3\cdot16 + 16 = 448$ parameters — far fewer than a dense layer's 49,152.
**Related.** [Pooling](#pooling), [Attention](#attention), [Transfer learning](#transfer-learning)
**Where it is taught.** [L07-05 Convolutional neural networks](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-05-convolutional-neural-networks.md)

## E

### Embedding
**Abbreviation.** — · **Module.** M07
**Simple definition.** A learned dense vector representing a discrete token, item or category.
**Detailed explanation.** Embeddings place similar items near each other in a continuous space,
so similarity becomes geometry. They are trained jointly with the task, and their dimensions are
a capacity/speed trade-off.
**Mathematics.** $e_t = E^\top \mathbf{1}_t$ for embedding matrix $E \in \mathbb{R}^{|V| \times d}$.
**Practical example.** A 300-dimensional embedding trained on support tickets places "refund"
and "chargeback" close together, enabling semantic search that keyword matching misses.
**Related.** [Attention](#attention), [Transformer](#transformer), [Token](#token)
**Where it is taught.** [L07-07 Attention and transformers](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-07-attention-and-transformers.md)

## G

### Gradient check
**Abbreviation.** — · **Module.** M07
**Simple definition.** Comparing an analytic gradient with a finite-difference estimate to catch
backpropagation bugs.
**Detailed explanation.** A relative error below about $10^{-6}$ in double precision indicates a
correct implementation. The check is cheap on small networks and catches the errors that are
otherwise invisible: missing batch-size division, transposed matrices, wrong activation
derivative.
**Mathematics.** $\frac{\partial L}{\partial \theta} \approx \frac{L(\theta + \epsilon) - L(\theta - \epsilon)}{2\epsilon}$
**Practical example.** The M07 lab's 64-5-3 network passes at 1.22e-08; a transposed weight
matrix fails at 0.4, which is how the bug is found in minutes rather than days.
**Related.** [Backpropagation](#backpropagation), [Learning rate](#learning-rate)
**Where it is taught.** [L07-02 Backpropagation: the mathematics of learning](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-02-backpropagation-the-mathematics-of-learning.md)

## L

### Learning rate
**Abbreviation.** LR, $\eta$ · **Module.** M07
**Simple definition.** The step size applied to the gradient at each update.
**Detailed explanation.** Too small and training never finishes; too large and the loss
oscillates or diverges. Schedules and adaptive optimisers exist because the ideal value changes
during training.
**Mathematics.** $\theta_{t+1} = \theta_t - \eta \nabla_\theta L$
**Practical example.** On the XOR lab, $\eta = 5.0$ diverges while $\eta = 0.05$ converges in
under 500 epochs — the same architecture, two outcomes.
**Related.** [Backpropagation](#backpropagation), [Batch normalisation](#batch-normalisation), [Gradient check](#gradient-check)
**Where it is taught.** [L07-03 Training in practice](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-03-training-in-practice.md)

## M

### Multilayer perceptron
**Abbreviation.** MLP · **Module.** M07
**Simple definition.** A feed-forward network with one or more hidden layers of nonlinear units.
**Detailed explanation.** A hidden layer maps inputs into a space where classes that were not
linearly separable become separable — the geometric answer to XOR. Depth composes features;
width gives capacity within a layer.
**Mathematics.** $h = \sigma(W_1 x + b_1)$, $\hat{y} = \text{softmax}(W_2 h + b_2)$
**Practical example.** A 2-4-2 tanh network solves XOR with a final loss of 5.95e-05 while a
single perceptron stays at 50% accuracy forever.
**Related.** [Backpropagation](#backpropagation), [Activation function](#activation-function), [Convolutional neural network](#convolutional-neural-network)
**Where it is taught.** [L07-01 From perceptron to MLP](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-01-from-perceptron-to-mlp.md)

## O

### Optimiser
**Abbreviation.** — · **Module.** M07
**Simple definition.** The rule that turns gradients into parameter updates.
**Detailed explanation.** SGD uses the raw gradient; momentum accumulates direction; Adam scales
per-parameter steps by running estimates of the first and second moments. Adaptive methods reduce
tuning effort but can generalise slightly worse than well-tuned SGD.
**Mathematics.** Adam: $m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t$, $v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2$.
**Practical example.** The same CNN reaches 0.91 accuracy in 12 epochs with Adam and 25 with
plain SGD, but SGD ends 0.4 points higher after full training.
**Related.** [Learning rate](#learning-rate), [Regularisation](#regularisation-deep-learning)
**Where it is taught.** [L07-03 Training in practice](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-03-training-in-practice.md)

## P

### Pooling
**Abbreviation.** — · **Module.** M07
**Simple definition.** Downsampling a feature map by summarising small regions.
**Detailed explanation.** Max pooling keeps the strongest response in each window, shrinking
spatial dimensions and adding small translation tolerance. It discards location information,
which is why dense prediction tasks often prefer strided convolutions.
**Mathematics.** $\text{maxpool}_{2\times2}(X)_{ij} = \max(X_{2i:2i+2,\,2j:2j+2})$
**Practical example.** A 30×30 feature map with 2×2 pooling becomes 15×15, halving the
computation of the next layer.
**Related.** [Convolutional neural network](#convolutional-neural-network)
**Where it is taught.** [L07-05 Convolutional neural networks](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-05-convolutional-neural-networks.md)

### Perceptron
**Abbreviation.** — · **Module.** M07
**Simple definition.** The original single-layer linear classifier, updated only on mistakes.
**Detailed explanation.** It converges in finite steps when the classes are linearly separable
and provably never converges otherwise. That limitation, not an implementation bug, is why
hidden layers exist.
**Mathematics.** $w \leftarrow w + \eta (y - \hat{y}) x$
**Practical example.** Trained on AND and OR it reaches zero errors in six epochs; trained on XOR
its error count oscillates 2, 3, 4, 4, 4, 4 forever.
**Related.** [Multilayer perceptron](#multilayer-perceptron), [Activation function](#activation-function)
**Where it is taught.** [L07-01 From perceptron to MLP](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-01-from-perceptron-to-mlp.md)

## R

### Recurrent neural network
**Abbreviation.** RNN · **Module.** M07
**Simple definition.** A network that processes a sequence by carrying a hidden state from step
to step.
**Detailed explanation.** The recurrence lets information persist, but gradients either vanish or
explode over long sequences; LSTM and GRU gates were the fix. RNNs are still useful for streaming
data, though attention has displaced them for most language tasks.
**Mathematics.** $h_t = \tanh(W_h h_{t-1} + W_x x_t + b)$
**Practical example.** A GRU forecasting hourly demand keeps a 48-hour context; a plain RNN on
the same data forgets beyond about 10 hours.
**Related.** [Attention](#attention), [Transformer](#transformer)
**Where it is taught.** [L07-06 Sequence models: RNN, LSTM, GRU](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-06-sequence-models-rnn-lstm-gru.md)

### Regularisation (deep learning)
**Abbreviation.** — · **Module.** M07
**Simple definition.** Techniques that constrain a network to improve generalisation.
**Detailed explanation.** Dropout randomly disables units during training, weight decay penalises
large weights, early stopping halts when validation error rises, and data augmentation enlarges
the effective dataset. All trade training fit for test performance.
**Mathematics.** Dropout: $\tilde{h} = h \odot m$, $m_i \sim \text{Bernoulli}(1-p)$.
**Practical example.** Dropout 0.3 on a 3-layer classifier lifts validation accuracy from 0.84
to 0.89 while training accuracy falls from 0.99 to 0.94 — the gap closing is the point.
**Related.** [Overfitting](machine-learning.md#overfitting), [Batch normalisation](#batch-normalisation)
**Where it is taught.** [L07-04 Regularisation and diagnosis](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-04-regularisation-and-diagnosis.md)

## T

### Token
**Abbreviation.** — · **Module.** M07
**Simple definition.** A unit of text — a word, subword or character — that a model processes.
**Detailed explanation.** Tokenisation decides the vocabulary and the sequence length, and
therefore cost, context limits and failure modes on rare words. Subword schemes such as BPE
balance coverage against sequence length.
**Mathematics.** —
**Practical example.** "unbelievable" becomes `un + believ + able` in a 50,000-token BPE
vocabulary, so the model can handle the word even if it never saw it whole.
**Related.** [Embedding](#embedding), [Attention](#attention), [Transformer](#transformer)
**Where it is taught.** [L07-07 Attention and transformers](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-07-attention-and-transformers.md)

### Transfer learning
**Abbreviation.** — · **Module.** M07
**Simple definition.** Reusing a model trained on one task as the starting point for another.
**Detailed explanation.** Early layers learn general features (edges, syntax) that transfer;
later layers are task-specific. Fine-tuning a pretrained backbone reaches good accuracy with
orders of magnitude less data than training from scratch.
**Mathematics.** $\theta = \theta_{\text{pre}} + \Delta\theta$, with only $\Delta\theta$ trained (or all, at a small LR).
**Practical example.** Fine-tuning a pretrained ResNet on 2,000 plant images reaches 0.94
accuracy; the same architecture trained from scratch on the same data reaches 0.71.
**Related.** [Convolutional neural network](#convolutional-neural-network), [Embedding](#embedding)
**Where it is taught.** [L07-08 Transfer learning and autoencoders](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-08-transfer-learning-and-autoencoders.md)

### Transformer
**Abbreviation.** — · **Module.** M07
**Simple definition.** An architecture built from stacked self-attention and feed-forward blocks,
with no recurrence.
**Detailed explanation.** Self-attention lets every position see every other position in one
step, so training parallelises across the sequence. Positional encodings restore order, and the
cost grows quadratically with sequence length.
**Mathematics.** $\text{block}(X) = \text{LayerNorm}(X + \text{Attn}(X))$ then $\text{LayerNorm}(X + \text{FFN}(X))$
**Practical example.** A 6-layer transformer with 8 heads translates a 40-token sentence in one
forward pass, where an RNN needs 40 sequential steps.
**Related.** [Attention](#attention), [Token](#token), [Embedding](#embedding)
**Where it is taught.** [L07-07 Attention and transformers](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-07-attention-and-transformers.md)

## V

### Vanishing gradient
**Abbreviation.** — · **Module.** M07
**Simple definition.** Gradients shrinking toward zero as they propagate back through many
layers, so early layers stop learning.
**Detailed explanation.** Repeated multiplication by derivatives below 1 makes the signal decay
geometrically. ReLU, residual connections, normalisation and gating are the standard mitigations.
**Mathematics.** $\prod_{l=1}^{L} \sigma'(z^{(l)})$ decays exponentially in $L$.
**Practical example.** A 20-layer sigmoid network's first layer weights barely move after 50
epochs; adding residual connections restores learning and cuts loss tenfold.
**Related.** [Backpropagation](#backpropagation), [Recurrent neural network](#recurrent-neural-network), [Activation function](#activation-function)
**Where it is taught.** [L07-04 Regularisation and diagnosis](../../modules/M07-neural-networks-and-deep-learning/lessons/L07-04-regularisation-and-diagnosis.md)

---

[Glossary index](README.md) · [Machine learning](machine-learning.md) · [NLP and vision](nlp-and-vision.md) · [Quick reference](../glossary.md)
