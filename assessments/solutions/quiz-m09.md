# QUIZ-M09 — Solutions and Explanations

> **Availability.** M09 (Computer Vision) is not published in this repository yet. This paper is
> included so the assessment set is complete; it cannot be attempted until the module's
> lessons and labs are available.

[Quiz](quiz-m09.md) · [Assessment index](../README.md)

---

## Part A

**Q9.1 — A.** IoU is the intersection area divided by the union area, in $[0,1]$. Dividing by the
prediction area alone gives a different (and asymmetric) measure, which is why IoU is preferred for
matching boxes.

**Q9.2 — B.** Padding controls output size (and lets border pixels influence as many filters as
interior ones). It does not change the parameter count, which depends on kernel size and channels.

**Q9.3 — C.** Semantic segmentation labels every pixel. Detection outputs boxes and labels;
classification outputs one label per image.

**Q9.4 — B.** Augmentation is a regulariser: it reduces variance by making the model invariant to
transformations it should ignore. It does not add information about classes it has never seen.

## Part B

**Q9.5 — True.** With stride 1 and padding $p$, output size is $(n+2p-k)/1+1$. For $k=3$, $p=1$:
$(n+2-3)+1=n$. This is the standard "same" convolution.

## Part C

**Q9.6 — Model answer.** Two mechanisms: (i) covariate shift — lighting, background, blur and
framing differ from the curated set, so the input distribution at test time is not the training
distribution; (ii) shortcut learning — curated datasets often have background or capture artefacts
correlated with the label, which the model uses and which are absent in the field.

**Q9.7 — Model answer.** A defect detector's cost is dominated by missed defects (false negatives).
Overall accuracy is high when defects are rare, even if every defect is missed. Per-class recall
states the fraction of defects found, which is the quantity the inspection process depends on.

## Part D

**Q9.8 —** $A$: $4\times4=16$. $B$: $4\times4=16$. Intersection: $x\in[2,4]$ (2), $y\in[2,4]$ (2)
→ 4. Union $=16+16-4=28$. IoU $=4/28\approx0.143$.

**Q9.9 —**

- conv $3\times3$, stride 1, pad 1: $64\times64$ (same)
- max-pool $2\times2$: $32\times32$
- conv $3\times3$, stride 1, pad 0: $30\times30$

## Part E

**Q9.10 —**

$$
\begin{bmatrix}7&8\\6&7\end{bmatrix}
$$

Top-left window max(1,3,5,7)=7; top-right max(2,4,6,8)=8; bottom-left max(0,2,4,6)=6; bottom-right
max(1,3,5,7)=7.

---

[Quiz](quiz-m09.md) · [Previous solutions](quiz-m08.md) · [Assessment index](../README.md)
