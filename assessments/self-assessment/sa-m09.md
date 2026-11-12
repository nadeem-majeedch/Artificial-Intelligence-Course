# SA-M09 — Self-Assessment: Computer Vision

Module M09 · [Module](../../docs/CURRICULUM-MAP.md) · [Quiz](../quizzes/quiz-m09.md) · [Index](README.md)

Rate each item **Confident / Shaky / Not yet**.

## Key concepts checklist

- [ ] Describe an image as an array with shape, dtype and value range
- [ ] Compute convolution output size and parameter counts
- [ ] Explain pooling and its loss of spatial information
- [ ] Distinguish classification, detection and segmentation
- [ ] Compute IoU and explain its use in matching
- [ ] State why augmentation reduces variance
- [ ] Explain domain shift with a concrete example

## Knowledge-check questions

1. A $3\times3$ conv, stride 2, no padding on a 32×32 input — what is the output size?
2. Why does a segmentation model need a decoder or upsampling path?
3. Two boxes overlap 4 units²; areas are 16 and 16. Compute IoU.
4. Why does augmentation not fix a dataset that lacks a class entirely?
5. What does a per-class recall of 0.3 tell you that 0.95 accuracy hides?

## Practical competency checklist

- [ ] Build a training loop with augmentation and validation
- [ ] Inspect an error gallery and group failures by cause
- [ ] Test the model under at least three corruptions
- [ ] Report results per class, not only overall

## Suggested revision topics

Image representation · convolution arithmetic · pooling · CNN architectures · detection and
segmentation · augmentation · transfer learning · domain shift · robustness testing.

## Readiness test for M10

Without notes:

1. Compute output shapes through a two-conv, one-pool stack.
2. Compute IoU for two boxes and decide a match at threshold 0.5.
3. Name two reasons a high benchmark score may not survive deployment.

If any is shaky, revisit L09-03 and L09-06 before M10.
