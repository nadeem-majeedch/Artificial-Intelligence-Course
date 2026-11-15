# Phase 24 — Curriculum Hours Reconciliation

**Question.** Why did the curriculum map report roughly 318 hours for the modules (374 with
prerequisites), while the module pages summed to 350.7 (about 407)?

**Answer.** They were different quantities, and several documents mixed them. 318/374 were
*design budgets* written before the labs, notebooks and projects existed. 350.7/406.7 are the
*measured published workload* on the module pages, which count practical and project time
explicitly. Both numbers were arithmetically correct; the repository presented them as if they
were the same total.

---

## 1. Root cause

1. `docs/CURRICULUM-MAP.md` §2 and §3 carried the original design budgets (318/374) in the
   tables, while §7 admitted that the published material measured 350.7/407.
2. `modules/README.md` used measured hours in its index table but design hours in each module's
   `Study time` line, so the same page disagreed with itself.
3. `README.md`, `docs/faq.md`, `docs/course-roadmap.md` and `docs/learning-path.md` repeated the
   design figures. `docs/learning-path.md` carried both ("165 design, 190 published"), and its
   Path A rows summed to 159 rather than either figure.
4. The M14 module page's itemised table summed to 30 hours while its header said 32.9; the
   capstone page repeated 30.
5. Four modules account for most of the gap: M04 (21 → 31.6), M10 (25 → 34.1), M12 (19 → 27.8)
   and M14 (30 → 32.9). Each has substantial project or practical work that the design budget
   omitted.

No hours were double-counted. The gap is entirely the difference between an estimate made
before the artefacts were written and a count made from the artefacts.

## 2. The single method now used everywhere

`docs/CURRICULUM-MAP.md` §3.1 defines it:

| Step | Rule |
| --- | --- |
| Unit | One hour of total student effort at the stated level; contact hours are not tracked because the course is self-study |
| Components | **Guided** (lesson reading and worked examples), **practical** (labs, coding, hands-on notebooks), **assessment** (quizzes, assignments, self-assessment), **project** (mini-project or capstone) |
| Module total | Sum of the four published components on that module's page, to one decimal |
| Programme total | Prerequisites (14 + 24 + 10 + 8 = 56 h) + all module totals (350.7 h) = **406.7 h** |
| Study paths | Full module totals included, plus an explicit prerequisite share; core uses P01 in full and 50% of P02–P04 (21 h) as a stated planning assumption |
| Rounding | Module/component figures exact to one decimal; path/programme totals rounded to the nearest hour for display |

The 50% prerequisite share is an assumption, not a measurement: the repository does not record
per-lesson prerequisite hours. It is stated wherever a core-path total appears, and changing it
changes only the path totals, never the module totals.

## 3. Before and after, per module

| Module | Design budget (old) | Measured published (now canonical) | Difference |
| --- | ---: | ---: | ---: |
| M01 | 10 | 12.8 | +2.8 |
| M02 | 18 | 17.9 | −0.1 |
| M03 | 26 | 19.9 | −6.1 |
| M04 | 21 | 31.6 | +10.6 |
| M05 | 24 | 20.6 | −3.4 |
| M06 | 31 | 31.4 | +0.4 |
| M07 | 27 | 24.9 | −2.1 |
| M08 | 22 | 24.3 | +2.3 |
| M09 | 22 | 26.8 | +4.8 |
| M10 | 25 | 34.1 | +9.1 |
| M11 | 24 | 23.3 | −0.7 |
| M12 | 19 | 27.8 | +8.8 |
| M13 | 19 | 22.4 | +3.4 |
| M14 | 30 | 32.9 | +2.9 |
| **Modules** | **318** | **350.7** | **+32.7** |
| Prerequisites | 56 | 56 | 0 |
| **Programme** | **374** | **406.7** | **+32.7** |

Component totals across the fourteen modules: guided **112.4**, practical **110.0**, assessment
**75.8**, project **52.5** — sum **350.7**.

## 4. Study-path totals after reconciliation

| Path | Composition | Old | New | Arithmetic |
| --- | --- | ---: | ---: | --- |
| Core | P01 + 50% of P02–P04 + M01–M06 | 165 | **169** | 14 + 21 + 134.2 = 169.2 |
| Core + deep learning | Core + M07 | 192 | **194** | 169.2 + 24.9 = 194.1 |
| Full programme | All prerequisites + all modules | 374 | **407** | 56 + 350.7 = 406.7 |
| NLP & generative AI | Core + M07 + M08 + M11 + M12 | 257 | **270** | 194.1 + 24.3 + 23.3 + 27.8 = 269.5 |
| Vision | Core + M07 + M09 + M13 | 223 | **243** | 194.1 + 26.8 + 22.4 = 243.3 |
| Decision systems | Core + M07 + M10 + M12 | 236 | **256** | 194.1 + 34.1 + 27.8 = 256.0 |
| Responsible AI | Core + M07 + M13 + M12 + M11 | 244 | **268** | 194.1 + 22.4 + 27.8 + 23.3 = 267.6 |

Semester split: **158.8 h** (P01–P04 + M01–M05) and **247.9 h** (M06–M14), total 406.7.

## 5. Documents updated

| File | Change |
| --- | --- |
| `docs/CURRICULUM-MAP.md` | §2 and §3 totals; per-module hours; new §3.1 method; §7 paths and arithmetic; retired-budget note |
| `modules/README.md` | Index hours (already measured) and all fourteen `Study time` lines corrected to the module pages; core-path mention 165 → 169 |
| `docs/course-roadmap.md` | Stage headings, module table, semester split and total |
| `README.md` | Learning-path table, 17-week schedule and FAQ answer |
| `docs/faq.md` | Core/deep-learning/full-programme durations |
| `docs/learning-path.md` | Path A table and status, Path B/C totals, specialisation table, pacing weeks; removed stale "complete" bullets and the 159-hour row sum |
| `modules/M14-…/README.md` | Total line now reconciles to 32.9 with a rounding note |
| `modules/M14-…/capstone/README.md` | "14 of its 32.9 hours" |
| `audit/check_hours.py` | New deterministic check of all the above |

## 6. Verification

`python audit/check_hours.py` → **0 failures**. It checks:

- each module page's components sum to its stated total, and the fourteen totals sum to 350.7;
- prerequisite sections sum to 56;
- the curriculum map carries 350.7/406.7 and a row for every module;
- README, FAQ, learning path and roadmap quote the reconciled path totals;
- no document still presents 165/192/374 as a current total;
- the module index hours match each module page.

Also run: `audit/check_course.py` (0 problems), full pytest (188 passed), compilation (exit 0),
licensing checker (0 failures).

## 7. Remaining limitations

- Hours are planning estimates, not measured student time. No timing study exists.
- The 50% "essentials" share for P02–P04 is an explicit assumption; per-lesson prerequisite hours
  are not recorded.
- Contact hours are not tracked, because the course has no timetable. The documents say so rather
  than inventing a split.
- The module pages remain the source of truth: a future change to a lab or project must update its
  module total, and `check_hours.py` will fail until every summary agrees.
