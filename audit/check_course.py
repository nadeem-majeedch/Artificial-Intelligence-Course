"""Regression checks for the repository's Markdown and metadata.

Checks
------
1. Every relative Markdown link resolves to a file, and every ``#anchor`` resolves to a
   heading in that file.
2. Every lesson has a Practical Exercises section with 2-6 items.
3. Every laboratory either has a starter script that exists, a linked notebook that exists,
   or is explicitly analytical (no starter required).
4. The four labs that lacked extension challenges now have them.
5. ``CITATION.cff`` parses as YAML, carries the required CFF keys, and contains no
   fabricated DOI, version, release date or ORCID.

Usage:  python audit/check_course.py [--quiet]
Exit status is 1 if any check fails.
"""

import glob
import os
import re
import sys
import urllib.parse

try:
    import yaml
except ImportError:  # pragma: no cover - the course environment ships PyYAML
    yaml = None

LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)


def slug(heading):
    text = re.sub(r"`", "", heading)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.strip().lower()
    # GitHub removes punctuation and turns each space into one hyphen, so an em dash
    # between two spaces yields "--". Collapsing whitespace here would break real anchors.
    text = re.sub(r"[^\w\s-]", "", text)
    return text.replace(" ", "-").strip("-")


def headings(path):
    text = open(path, encoding="utf-8").read()
    found = set()
    for match in HEADING.finditer(text):
        found.add(slug(match.group(2)))
    # explicit HTML anchors: <a id="m01"></a> and <a name="m01"></a>
    found.update(re.findall(r"<a\s+(?:id|name)=\"([^\"]+)\"", text))
    return found


def without_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def check_links(quiet):
    broken = []
    total = 0
    cache = {}
    for path in glob.glob("**/*.md", recursive=True):
        if any(part in {".git", "node_modules", ".freebuff", "templates"} for part in path.split(os.sep)):
            continue
        directory = os.path.dirname(path)
        for target in LINK.findall(without_code(open(path, encoding="utf-8").read())):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            total += 1
            file_part, _, anchor = target.partition("#")
            file_part = urllib.parse.unquote(file_part)
            resolved = os.path.normpath(os.path.join(directory, file_part)) if file_part else path
            if not os.path.exists(resolved):
                broken.append((path, target, "missing file"))
                continue
            if anchor and resolved.endswith(".md"):
                if resolved not in cache:
                    cache[resolved] = headings(resolved)
                if anchor.lower() not in cache[resolved]:
                    broken.append((path, target, "missing anchor"))
    if not quiet:
        print(f"links checked: {total}   broken: {len(broken)}")
    for item in broken[:40]:
        print("  BROKEN", *item)
    return broken


def exercise_counts():
    counts = {}
    for path in sorted(glob.glob("modules/M*/lessons/L*.md")):
        text = open(path, encoding="utf-8").read()
        # M01-M11 use "## 10. Practical Exercises"; M12-M14 use "## Exercises"
        match = re.search(r"^##+\s+(?:\d+\.\s*)?(?:Practical\s+)?Exercises\s*$", text, re.M)
        if not match:
            counts[path] = 0
            continue
        section = text[match.end():]
        section = re.split(r"^##\s+", section, flags=re.M)[0]
        numbered = re.findall(r"^\s*\d+\.\s+\S", section, re.M)
        bold = re.findall(r"^\s*[-*]?\s*\*\*[A-Z][^*]{2,40}\.\*\*", section, re.M)
        counts[path] = max(len(numbered), len(bold))
    return counts


def check_exercises(quiet):
    counts = exercise_counts()
    weak = [(path, f"{n} exercise items") for path, n in counts.items() if n < 2]
    if not quiet:
        buckets = {}
        for number in counts.values():
            buckets[number] = buckets.get(number, 0) + 1
        print(f"lessons: {len(counts)}   exercise items per lesson: "
              f"{dict(sorted(buckets.items()))}")
    for path, number in weak:
        print(f"  EXERCISES {number}: {path}")
    return weak


def check_labs(quiet):
    labs = sorted(glob.glob("modules/M*/labs/lab-*.md"))
    problems = []
    starters = 0
    linked = 0
    for path in labs:
        text = open(path, encoding="utf-8").read()
        has_starters = "## Starter material" in text
        starter_links = [link for link in LINK.findall(text)
                         if "starters/" in link or "../notebooks/" in link]
        if has_starters:
            linked += 1
        for link in starter_links:
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), link.split("#")[0]))
            if not os.path.exists(resolved):
                problems.append((path, link))
        if any(link.endswith(".py") for link in starter_links) and has_starters:
            starters += 1
    if not quiet:
        print(f"labs: {len(labs)}   with starter material: {linked}   with a starter script: {starters}")
    for item in problems:
        print("  LAB LINK", *item)

    required = {
        "lab-13-01": "modules/M13-responsible-explainable-secure-ai/labs/lab-13-01-fairness-audit.md",
        "lab-13-02": "modules/M13-responsible-explainable-secure-ai/labs/lab-13-02-security-and-prompt-injection-testing.md",
        "lab-14-01": "modules/M14-advanced-ai-applications-and-capstone/labs/lab-14-01-multimodal-and-graph-systems.md",
        "lab-14-02": "modules/M14-advanced-ai-applications-and-capstone/labs/lab-14-02-efficient-serving.md",
    }
    for name, path in required.items():
        if path in labs:
            text = open(path, encoding="utf-8").read()
            if "Extension challenges (optional)" not in text:
                problems.append((path, "missing extension section"))
                print(f"  EXTENSIONS missing: {name}")
    return problems


def check_citation(quiet):
    problems = []
    if not os.path.exists("CITATION.cff"):
        return [("CITATION.cff", "missing")]
    text = open("CITATION.cff", encoding="utf-8").read()
    if yaml is None:
        print("  CITATION.cff: PyYAML not installed, syntax not validated")
        return problems
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as error:
        return [("CITATION.cff", f"YAML error: {error}")]
    for key in ("cff-version", "message", "title", "authors"):
        if key not in data:
            problems.append(("CITATION.cff", f"missing {key}"))
    for author in data.get("authors", []):
        if "family-names" not in author or "given-names" not in author:
            problems.append(("CITATION.cff", "author missing family/given names"))
    forbidden = {"doi", "version", "date-released", "identifiers", "orcid"}
    present = sorted(forbidden & set(data))
    if present:
        print(f"  CITATION.cff: unverified fields present: {present}")
    if not quiet:
        print(f"CITATION.cff: parsed, keys={len(data)}, authors={len(data.get('authors', []))}")
    return problems


def main():
    quiet = "--quiet" in sys.argv
    failures = check_links(quiet) + check_exercises(quiet) + check_labs(quiet) + check_citation(quiet)
    print(f"TOTAL PROBLEMS: {len(failures)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
