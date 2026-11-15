"""Structural acceptance checks for lessons, laboratories and assessments.

This does not judge prose quality; it finds missing sections, placeholder text, count
mismatches and broken cross-references that a human reviewer would otherwise have to
find by hand. Results go to ``audit/phase23b_structural.json`` and are printed as a
compact list of findings.

Usage:  python audit/structural_audit_phase23b.py
"""

import glob
import json
import os
import re

# Heading vocabulary differs by module generation; match the intent, case-insensitively.
LESSON_REQUIRED = {
    "objectives": r"(?im)^##+\s+(?:\d+\.\s*)?(Learning Objectives|What you will be able to do|Objectives)",
    "prerequisites": r"(?im)(^##+\s+(?:\d+\.\s*)?(Prerequisites?|Prerequisite Knowledge|Before you start|Assumed knowledge)|^\|\s*Prerequisites\s*\|)",
    "exercises": r"(?im)^##+\s+(?:\d+\.\s*)?(Practical\s+)?Exercises",
    "key_terms": r"(?im)^##+\s+(?:\d+\.\s*)?Key Terms",
    "further_reading": r"(?im)^##+\s+(?:\d+\.\s*)?(Further Reading|References and further reading)",
}
LAB_REQUIRED = {
    "purpose": r"(?im)^##+\s+(?:\d+\.\s*)?(Purpose|Objective|Overview|Scenario|Problem statement|Task)",
    "tasks": r"(?im)^##+\s+(?:\d+\.\s*)?(Tasks|Procedure|Step-by-step tasks|What to do|Work|Scenario|Part [A-Z]|Implementation tasks)\b",
    "deliverable": r"(?im)(^##+\s+(?:\d+\.\s*)?(Deliverable|Deliverables|What to submit|Submission requirements|Report structure|Output)|\*\*Deliverable[.:])",
}
PLACEHOLDERS = [r"\bTODO\b", r"\bFIXME\b", r"\bTBD\b", r"lorem ipsum", r"«[^»]+»", r"\?\?\?"]

def without_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def headings(text):
    return re.findall(r"^(#{1,6})\s+(.+?)\s*$", text, re.M)


def count_items(section):
    numbered = re.findall(r"^\s*\d+\.\s+\S", section, re.M)
    bullets = re.findall(r"^\s*[-*]\s+\S", section, re.M)
    bold = re.findall(r"^\s*\*\*[A-Z][^*]{2,40}\.\*\*", section, re.M)
    return max(len(numbered), len(bold), len(bullets))


def section(text, heading_regex):
    match = re.search(heading_regex, text, re.M)
    if not match:
        return ""
    rest = text[match.end():]
    return re.split(r"^##\s+", rest, flags=re.M)[0]


def main():
    findings = []
    summary = {"lessons": {}, "labs": {}, "assessments": {}}

    lessons = sorted(glob.glob("modules/M*/lessons/L*.md"))
    for path in lessons:
        text = open(path, encoding="utf-8").read()
        words = len(re.findall(r"\b\w+\b", text))
        missing = [name for name, pattern in LESSON_REQUIRED.items()
                   if not re.search(pattern, text, re.M)]
        exercises = count_items(section(text, LESSON_REQUIRED["exercises"])) if "exercises" not in missing else 0
        placeholders = [pattern for pattern in PLACEHOLDERS if re.search(pattern, without_code(text))]
        code_blocks = len(re.findall(r"^```", text, re.M)) // 2
        objectives = section(text, LESSON_REQUIRED["objectives"])
        objective_items = count_items(objectives) if objectives else 0
        summary["lessons"][path] = {"words": words, "missing": missing, "exercises": exercises,
                                    "objectives": objective_items, "code_blocks": code_blocks,
                                    "placeholders": placeholders}
        if missing:
            findings.append(("LESSON SECTIONS", path, ", ".join(missing)))
        if placeholders:
            findings.append(("PLACEHOLDER", path, ", ".join(placeholders)))
        if exercises < 2:
            findings.append(("LESSON EXERCISES", path, f"{exercises} items"))
        if objective_items < 3:
            findings.append(("LESSON OBJECTIVES", path, f"{objective_items} items"))
        if words < 800:
            findings.append(("LESSON SHORT", path, f"{words} words"))

    labs = sorted(glob.glob("modules/M*/labs/lab-*.md"))
    for path in labs:
        text = open(path, encoding="utf-8").read()
        missing = [name for name, pattern in LAB_REQUIRED.items()
                   if not re.search(pattern, text, re.M)]
        has_rubric = bool(re.search(r"(rubric|marking|evaluation criteria|assessment criteria|grading|scoring)", text, re.I))
        starter = bool(re.search(r"^##+\s+Starter material", text, re.M))
        starter_links = re.findall(r"\]\((starters/[^)]+|\.\./notebooks/[^)]+)\)", text)
        extensions = bool(re.search(r"Extension challenges", text, re.I))
        placeholders = [pattern for pattern in PLACEHOLDERS if re.search(pattern, without_code(text))]
        hours = re.search(r"\|\s*Time\s*\|\s*([0-9.]+)\s*hour", text, re.I)
        summary["labs"][path] = {"missing": missing, "rubric": has_rubric, "starter": starter,
                                 "starter_links": starter_links, "extensions": extensions,
                                 "hours": float(hours.group(1)) if hours else None,
                                 "placeholders": placeholders}
        if missing:
            findings.append(("LAB SECTIONS", path, ", ".join(missing)))
        if not has_rubric:
            findings.append(("LAB RUBRIC", path, "no assessment criteria/rubric wording"))
        for link in starter_links:
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), link))
            if not os.path.exists(resolved):
                findings.append(("LAB STARTER LINK", path, link))
        if placeholders:
            findings.append(("LAB PLACEHOLDER", path, ", ".join(placeholders)))

    quizzes = sorted(glob.glob("assessments/quizzes/*.md"))
    for path in quizzes:
        text = open(path, encoding="utf-8").read()
        questions = len(re.findall(r"\*\*Q\d+\.\d+\*\*", text)) or len(re.findall(r"^\s*\d+\.\s+", text, re.M))
        name = os.path.basename(path)
        solution = os.path.join("assessments", "solutions", name)
        has_solution = os.path.exists(solution)
        answers = 0
        if has_solution:
            answers = len(re.findall(r"\*\*Q\d+\.\d+", open(solution, encoding="utf-8").read()))
        summary["assessments"][path] = {"questions": questions, "solution": has_solution, "answer_items": answers}
        if not has_solution:
            findings.append(("QUIZ SOLUTION", path, "missing solution file"))
        elif answers and questions and answers < questions * 0.5:
            findings.append(("QUIZ KEY COUNT", path, f"{questions} questions vs {answers} answer items"))

    with open("audit/phase23b_structural.json", "w", encoding="utf-8") as handle:
        json.dump({"findings": findings, "summary": summary}, handle, indent=2)

    print(f"lessons checked: {len(lessons)}, labs: {len(labs)}, quizzes: {len(quizzes)}")
    for kind, path, detail in findings:
        print(f"  [{kind}] {path}: {detail}")
    print(f"TOTAL FINDINGS: {len(findings)}")


if __name__ == "__main__":
    main()
