"""Check that every published hour total uses the same measured figures.

The course uses one method (docs/CURRICULUM-MAP.md §3.1): a module total is the sum of
its guided, practical, assessment and project components; the programme total is the four
prerequisite sections plus the fourteen module totals.

This script verifies the arithmetic and the consistency of the documents that quote it.
It does not judge whether the estimates are pedagogically right.

Usage:  python audit/check_hours.py
Exit status 1 if any total disagrees or a stale design figure is still presented as current.
"""

import glob
import re
import sys

MODULES = 350.7
PREREQUISITES = 56.0
PROGRAMME = 406.7
PATHS = {"core": 169, "core_plus_dl": 194, "full": 407,
         "nlp": 270, "vision": 243, "decision": 256, "responsible": 268}

MODULE_ORDER = ["M01", "M02", "M03", "M04", "M05", "M06", "M07",
                "M08", "M09", "M10", "M11", "M12", "M13", "M14"]


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def module_pages():
    found = {}
    for path in sorted(glob.glob("modules/M*/README.md")):
        match = re.search(r"^# (M\d\d)", read(path), re.M)
        if match:
            found[match.group(1)] = path
    return found


def check_module_totals(failures):
    pages = module_pages()
    if len(pages) != 14:
        failures.append(("MODULES", "modules/*/README.md", f"found {len(pages)} module pages"))
    total = 0.0
    for code in MODULE_ORDER:
        path = pages.get(code)
        if not path:
            failures.append(("MODULES", code, "module page missing"))
            continue
        text = read(path)
        match = re.search(r"^\| Study time \| ([\d.]+) hours", text, re.M)
        if not match:
            failures.append(("MODULES", path, "no Study time line"))
            continue
        hours = float(match.group(1))
        total += hours
        categories = re.search(
            r"^\| Study time \| [\d.]+ hours — guided ([\d.]+) · practical ([\d.]+) · "
            r"assessment ([\d.]+) · project ([\d.]+) \|", text, re.M)
        if categories:
            parts = sum(float(value) for value in categories.groups())
            if abs(parts - hours) > 0.05:
                failures.append(("MODULES", path,
                                 f"components sum to {parts:.1f}, total says {hours:.1f}"))
    if abs(total - MODULES) > 0.05:
        failures.append(("MODULES", "module pages", f"sum {total:.1f}, expected {MODULES}"))


def check_curriculum_map(failures):
    text = read("docs/CURRICULUM-MAP.md")
    if "350.7" not in text or "406.7" not in text:
        failures.append(("MAP", "docs/CURRICULUM-MAP.md", "measured totals missing"))
    section = text.split("### 3.1", 1)
    if len(section) < 2:
        failures.append(("MAP", "docs/CURRICULUM-MAP.md", "§3.1 method missing"))
    table = text.split("## 4. Prerequisite track", 1)[0]
    for code in MODULE_ORDER:
        row = re.search(rf"^\| {code} \|.*?\| ([\d.]+) \| [^|]+ \|$", table, re.M)
        if not row:
            failures.append(("MAP", "docs/CURRICULUM-MAP.md", f"no hours row for {code}"))
    if "| **350.7** |" not in table:
        failures.append(("MAP", "docs/CURRICULUM-MAP.md", "module total row is not 350.7"))
    prereq = re.findall(r"### (P\d\d) — [^\n]*· (\d+) h", text)
    if sum(int(hours) for _, hours in prereq) != PREREQUISITES:
        failures.append(("MAP", "docs/CURRICULUM-MAP.md", "prerequisite hours do not sum to 56"))


def check_paths(failures):
    readme = read("README.md")
    for value in PATHS.values():
        if f"≈ {value} hours" not in readme and f"≈ {value}" not in readme:
            failures.append(("PATHS", "README.md", f"missing ≈ {value} hours"))
    faq = read("docs/faq.md")
    for value in (169, 194, 407):
        if str(value) not in faq:
            failures.append(("PATHS", "docs/faq.md", f"missing {value}"))
    learning = read("docs/learning-path.md")
    for value in (169, 194, 407):
        if f"≈ {value}" not in learning:
            failures.append(("PATHS", "docs/learning-path.md", f"missing ≈ {value}"))
    roadmap = read("docs/course-roadmap.md")
    if "406.7" not in roadmap:
        failures.append(("PATHS", "docs/course-roadmap.md", "programme total not 406.7"))


def check_stale(failures):
    """Design budgets may be named as retired, but not presented as current totals."""
    for path in ["README.md", "docs/faq.md", "docs/learning-path.md",
                 "docs/course-roadmap.md", "docs/CURRICULUM-MAP.md", "modules/README.md"]:
        text = read(path)
        for pattern in (r"≈ 165 hours", r"≈ 192 hours", r"≈ 374 hours",
                        r"about 165 hours", r"about 374 hours"):
            for match in re.finditer(pattern, text):
                line = text[: match.start()].count("\n") + 1
                failures.append(("STALE", f"{path}:{line}", pattern))


def check_module_index(failures):
    text = read("modules/README.md")
    for code in MODULE_ORDER:
        row = re.search(rf"^\| \[{code}\]\(#{code.lower()}\) \|.*?\| \d+ \| ([\d.]+) \|", text, re.M)
        if not row:
            failures.append(("INDEX", "modules/README.md", f"no hours in index row for {code}"))
            continue
        page = module_pages().get(code)
        if page:
            page_hours = re.search(r"^\| Study time \| ([\d.]+) hours", read(page), re.M)
            if page_hours and abs(float(row.group(1)) - float(page_hours.group(1))) > 0.05:
                failures.append(("INDEX", "modules/README.md",
                                 f"{code} index {row.group(1)} vs page {page_hours.group(1)}"))


def main():
    failures = []
    for check in (check_module_totals, check_curriculum_map, check_paths,
                  check_stale, check_module_index):
        check(failures)
    print(f"hour checks: {len(failures)} failure(s)")
    for kind, path, detail in failures:
        print(f"  [{kind}] {path}: {detail}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
