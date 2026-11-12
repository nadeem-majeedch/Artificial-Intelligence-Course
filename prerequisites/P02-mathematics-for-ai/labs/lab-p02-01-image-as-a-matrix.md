# LAB-P02-01 — An Image Is a Matrix

| Unit | P02 · Mathematics for AI |
| :--- | :--- |
| Level | 100 |
| Effort | 2.5 hours, suggested split: session 1 = tasks 1–3, session 2 = tasks 4–6 |
| Lessons covered | [LP02-01](../lessons/LP02-01-scalars-vectors-matrices-and-tensors.md), [LP02-02](../lessons/LP02-02-matrix-operations-and-multiplication.md), [LP02-03](../lessons/LP02-03-transpose-inverse-and-eigenvalues.md) |
| Dataset | generated in the lab (a synthetic 64×64 image) |
| Notebook | [NB-P02-01](../notebooks/nb-p02-01-linear-algebra.ipynb) — support for the matrix operations |

[← Unit home](../README.md) · [Prerequisites home](../../README.md)

## Scenario

A small digitisation unit in the department scans handwritten attendance sheets. The scans come back
rotated by a few degrees and with uneven brightness, and the OCR step downstream fails on the rotated
ones. The engineer, Mr. Adeel, wants a short script that loads a grayscale image as an array, applies a
rotation, and reports how similar two images are — so he can decide whether a rescan is needed. He has
no GPU and no image library beyond what NumPy provides.

## Your role

You are the junior engineer on the task. You report to Mr. Adeel and you will be judged on whether the
transformations are **correct and explainable**: he needs to know what matrix produced the rotated image,
not just that it looks rotated.

## What you are given

| Item | Location | Notes |
| :--- | :--- | :--- |
| Image | generated in Task 1 | 64×64 float array in [0, 1] |
| Starter code | none | NumPy and Matplotlib only |
| Constraints | — | no SciPy, no PIL, no OpenCV; transforms implemented from matrix definitions |

**Not provided:** a rotation helper, an interpolation function, or a similarity metric. Implement each
from the maths in LP02-02 and LP02-03.

## Requirements

**Functional**

- R1 — Build a 64×64 image containing a filled rectangle and a diagonal line, as a NumPy array.
- R2 — Implement `rotate(points, degrees)` that returns transformed coordinates using the 2×2 rotation
  matrix, applied to a stack of points.
- R3 — Produce a rotated image by mapping destination pixels back to source pixels (inverse mapping),
  with nearest-neighbour sampling.
- R4 — Implement `cosine_similarity(a, b)` for flattened images and report it for the original and
  rotated versions.
- R5 — Handle a rotation of 0° exactly, and a request for an angle outside $[0, 360)$ by wrapping it.

**Non-functional**

- N1 — Whole script runs in under 5 seconds.
- N2 — Deterministic: the same seed and angle give the same array.
- N3 — Every reported number comes from code, and each transform is accompanied by one sentence saying
  which matrix it is.

## Tasks

1. **Build the image.** Create a zeros array of shape `(64, 64)`, set a 20×30 rectangle to 1.0, and draw
   a diagonal line by assigning along `np.arange`. Display it with `imshow(..., cmap="gray")`.
   *(success: the shape prints as `(64, 64)` and the figure shows both shapes)*
2. **Write the rotation matrix.** For angle $\theta$, construct
   $\begin{bmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{bmatrix}$ and multiply a stack
   of pixel coordinates. Confirm that 90° maps $(1, 0)$ to $(0, 1)$ and that $\det R = 1$.
   *(success: the determinant prints as 1.000 and the rotated unit vectors are correct to 1e-9)*
3. **Rotate by inverse mapping.** For each destination pixel, apply $R^{-1}$ to find the source pixel and
   copy its value; out-of-range sources become 0. *(success: rotating by 360° reproduces the original
   exactly)*
4. **Measure similarity.** Flatten both images and compute the cosine similarity of LP02-01. Report it
   for 0°, 15°, 45° and 90°. *(success: similarity decreases monotonically with angle)*
5. **Explain a failure.** Rotate by 45° and inspect the diagonal line. Find one artefact caused by
   nearest-neighbour sampling and explain the mechanism in two sentences. *(success: the explanation
   names the sampling step, not "the image is blurry")*
6. **Report.** Write five sentences to Mr. Adeel: what the script does, what the similarity values mean,
   and one limitation he should know before relying on it.

## Deliverables

| File | Contents |
| :--- | :--- |
| `lab_p02_01.py` | Runnable script implementing R1–R5 |
| `rotation_panel.png` | Four panels: original, 15°, 45°, 90°, with titles |
| `report.md` | ≤ 400 words: the matrices used, similarity table, artefact analysis |

## Evaluation criteria

| Criterion | Weight | Excellent | Adequate | Not yet |
| :--- | ---: | :--- | :--- | :--- |
| Mathematical correctness | 35% | Correct rotation and inverse mapping; determinant check passes | Rotation right, mapping slightly off | Wrong matrix or direction |
| Implementation | 25% | Vectorised where natural, clear functions | Loops work, slow but correct | Does not run |
| Analysis | 25% | Artefact explained mechanistically; similarity interpreted | Noticed but unexplained | No analysis |
| Communication | 15% | Engineer could act on it | Understandable | Missing or vague |

## Extension challenges

1. **Better sampling.** Replace nearest-neighbour with bilinear interpolation and compare the 45° result
   and the similarity score.
2. **Eigen-directions.** Take the 2×2 matrix $\begin{bmatrix}2&1\\1&3\end{bmatrix}$, find its
   eigenvectors, and draw them over a unit circle transformed by that matrix.
3. **Colour.** Extend to a rank-3 tensor of shape `(64, 64, 3)` and rotate each channel with the same
   matrix. What must change in the indexing?

## Hints

<details><summary>Hint 1 — getting started</summary>

Build a coordinate grid with `np.meshgrid(np.arange(64), np.arange(64))`, stack the two arrays into a
`(4096, 2)` matrix of points, and treat that as your vector list. One matrix product then transforms
every pixel coordinate at once.

</details>

<details><summary>Hint 2 — the likely sticking point</summary>

The image origin is the top-left corner and the y-axis points down, so a mathematical rotation looks
clockwise on screen. Either accept that and say so, or translate to the image centre before rotating and
back afterwards — but do not silently mix the two conventions.

</details>

<details><summary>Hint 3 — checking your work</summary>

An invariant worth testing: rotation preserves the sum of pixel values up to sampling effects, and
rotating by 90° four times should return the original image to within rounding. If either fails, the
inverse mapping is wrong.

</details>

## Reflection

1. Why does the implementation map destination pixels back to the source, rather than pushing source
   pixels forward?
2. Cosine similarity of two images ignores brightness offsets. When would that be helpful, and when
   would it be misleading?
3. What would change if the image were 6400×6400 rather than 64×64?

## Time budget

| Session | Tasks | Time |
| :--- | :--- | ---: |
| 1 | 1–3 | 75 min |
| 2 | 4–6 | 75 min |
