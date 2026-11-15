"""Structural and coverage audit across lessons, labs, quizzes, assignments and docs."""

import glob
import json
import re
from collections import Counter

LESSON_SECTIONS = [
    ("objectives", r"(?i)##\s*[0-9.]*\s*learning objectives"),
    ("prerequisites", r"(?i)##\s*[0-9.]*\s*prerequisite"),
    ("study_time", r"\|\s*Study time\s*\|"),
    ("concepts", r"(?i)##\s*[0-9.]*\s*(core concepts|key concepts|conceptual explanation|concepts)"),
    ("worked_example", r"(?i)worked example"),
    ("code", r"```python"),
    ("common_mistakes", r"(?i)common mistakes"),
    ("exercises", r"(?i)##\s*[0-9.]*\s*(exercises|practice|self-check)"),
    ("self_check", r"(?i)self-assessment|self-check"),
    ("further_reading", r"(?i)further reading|references"),
]

LAB_SECTIONS = [
    ("objectives", r"(?i)##\s*[0-9.]*\s*learning objectives"),
    ("scenario", r"(?i)##\s*[0-9.]*\s*scenario"),
    ("problem", r"(?i)##\s*[0-9.]*\s*(problem statement|requirements)"),
    ("dataset", r"(?i)##\s*[0-9.]*\s*(dataset|what you are given)"),
    ("tasks", r"(?i)##\s*[0-9.]*\s*(step-by-step tasks|tasks)"),
    ("starter", r"```python"),
    ("expected", r"(?i)##\s*[0-9.]*\s*(expected|deliverables)"),
    ("testing", r"(?i)##\s*[0-9.]*\s*(testing instructions|hints)"),
    ("submission", r"(?i)##\s*[0-9.]*\s*(submission|deliverables)"),
    ("rubric", r"(?i)##\s*[0-9.]*\s*(evaluation rubric|evaluation criteria)"),
    ("extensions", r"(?i)##\s*[0-9.]*\s*extension"),
]

lessons = sorted(glob.glob("modules/M*/lessons/*.md"))
labs = sorted(glob.glob("modules/M*/labs/*.md"))
projects = sorted(glob.glob("modules/M*/projects/*.md"))
quizzes = sorted(glob.glob("assessments/quizzes/*.md"))
quiz_keys = sorted(glob.glob("assessments/solutions/quiz-*.md"))
pas = sorted(glob.glob("assessments/programming/pa-*.md"))
aas = sorted(glob.glob("assessments/analytical/aa-*.md"))

summary = {"lessons": len(lessons), "labs": len(labs), "projects": len(projects),
           "quizzes": len(quizzes), "quiz_keys": len(quiz_keys), "programming": len(pas),
           "analytical": len(aas)}

problems = {"lessons": [], "labs": [], "projects": []}
lesson_stats = []
for path in lessons:
    text = open(path, encoding="utf-8").read()
    missing = [name for name, pat in LESSON_SECTIONS if not re.search(pat, text, flags=re.M)]
    words = len(re.findall(r"\b\w+\b", text))
    code_blocks = len(re.findall(r"```python", text))
    math_blocks = len(re.findall(r"\$\$", text)) // 2
    tables = text.count("| :---")
    lesson_stats.append({"path": path.replace("\\", "/"), "words": words, "code_blocks": code_blocks,
                         "math_blocks": math_blocks, "tables": tables, "missing": missing})

for stat in lesson_stats:
    if stat["missing"]:
        problems["lessons"].append((stat["path"], stat["missing"]))
    if stat["code_blocks"] == 0:
        problems["lessons"].append((stat["path"], ["no python code block"]))

for path in labs + projects:
    text = open(path, encoding="utf-8").read()
    if path in labs:
        missing = [name for name, pat in LAB_SECTIONS if not re.search(pat, text, flags=re.M)]
    else:
        need = {"problem": r"(?i)problem statement", "requirements": r"(?i)requirements",
                "architecture": r"(?i)architecture|milestone", "starter": r"```python",
                "rubric": r"(?i)criteri|rubric", "extensions": r"(?i)extension"}
        missing = [name for name, pat in need.items() if not re.search(pat, text, flags=re.M)]
    if missing:
        problems["labs" if path in labs else "projects"].append((path.replace("\\", "/"), missing))

# similarity between lessons: 6-word shingles, report pairs above 0.25 Jaccard
def shingles(text, k=6):
    words = re.findall(r"[a-z]+", text.lower())
    return {" ".join(words[i:i + k]) for i in range(max(0, len(words) - k + 1))}

sets = [(p, shingles(open(p, encoding="utf-8").read())) for p in lessons]
hot = []
for i in range(len(sets)):
    for j in range(i + 1, len(sets)):
        inter = len(sets[i][1] & sets[j][1])
        if not inter:
            continue
        jac = inter / len(sets[i][1] | sets[j][1])
        if jac > 0.1:
            hot.append((round(jac, 3), sets[i][0].replace("\\", "/"), sets[j][0].replace("\\", "/")))
hot.sort(reverse=True)

# licensing / external references
lic = Counter()
urls = Counter()
for path in glob.glob("**/*.md", recursive=True):
    if ".git" in path:
        continue
    text = open(path, encoding="utf-8", errors="replace").read()
    for match in re.findall(r"https?://([^/\s)]+)", text):
        urls[match] += 1
    if re.search(r"(?i)\blicen[cs]e\b", text):
        lic[path.split("/")[0] if "/" in path else path] += 1

quiz_pairs = []
for q in quizzes:
    qtext = open(q, encoding="utf-8").read()
    stem = q.split("\\")[-1].split("/")[-1]
    key = [k for k in quiz_keys if stem in k or k.endswith(stem)]
    n_q = len(re.findall(r"(?i)^##\s*Part [A-G]", qtext, flags=re.M))
    quiz_pairs.append({"quiz": stem, "questions": n_q, "answer_key": bool(key)})

out = {"summary": summary, "problems": problems, "lesson_stats": lesson_stats,
       "similar": hot[:15], "licence_files": sum(lic.values()), "domains": urls.most_common(12),
       "quiz_pairs": quiz_pairs}
with open("_content_audit.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2)

print("counts:", summary)
print("lessons with gaps:", len(problems["lessons"]), problems["lessons"][:5])
print("labs with gaps:", len(problems["labs"]), problems["labs"][:5])
print("projects with gaps:", len(problems["projects"]), problems["projects"][:5])
print("words min/median/max:", min(s["words"] for s in lesson_stats),
      sorted(s["words"] for s in lesson_stats)[len(lesson_stats) // 2],
      max(s["words"] for s in lesson_stats))
print("code blocks min/max:", min(s["code_blocks"] for s in lesson_stats), max(s["code_blocks"] for s in lesson_stats))
print("top lesson similarity:", hot[:3])
print("domains:", urls.most_common(8))
print("quiz keys matched:", sum(1 for q in quiz_pairs if q["answer_key"]), "/", len(quiz_pairs))
print("parts per quiz:", [q["questions"] for q in quiz_pairs])
print("lessons without python:", [s["path"].split("/")[-1] for s in lesson_stats if s["code_blocks"] == 0])
