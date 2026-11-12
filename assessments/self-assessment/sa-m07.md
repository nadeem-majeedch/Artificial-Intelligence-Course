# SA-M07 — Self-Assessment: Neural Networks and Deep Learning

Module M07 · [Module](../../modules/M07-neural-networks-and-deep-learning/README.md) · [Quiz](../quizzes/quiz-m07.md) · [Index](README.md)

Rate each item **Confident / Shaky / Not yet**.

## Key concepts checklist

- [ ] Explain why nonlinear activations are required
- [ ] Describe backpropagation as the chain rule over a computation graph
- [ ] Compute output shapes and parameter counts for conv layers
- [ ] Explain what batch normalisation and dropout do, and when they are disabled
- [ ] Describe why residual connections help very deep networks
- [ ] State when transfer learning is preferable to training from scratch

## Knowledge-check questions

1. Why does a two-layer network with identity activations collapse to one linear layer?
2. A $3\times3$ conv has 64 input channels and 128 filters. How many parameters with bias?
3. Why is dropout applied only during training, and how is scaling handled?
4. What problem does batch normalisation address, and what does it not fix?
5. Why do CNNs share weights across positions? What does that assume?

## Practical competency checklist

- [ ] Implement a forward pass and verify shapes
- [ ] Check gradients numerically before training
- [ ] Tune a learning rate using evidence, not guesswork
- [ ] Read a learning curve and decide the next experiment

## Suggested revision topics

Perceptron to MLP · activations · backprop · optimisers · regularisation · normalisation · CNNs ·
RNNs and attention · transfer learning.

## Readiness test for M08

Without notes:

1. Compute the parameter count of a small CNN.
2. Explain what a gradient of zero implies and why it stalls learning.
3. Name the two changes that most reliably fix overfitting in a small dataset.

If any is shaky, revisit L07-03 and L07-05 before M08.
