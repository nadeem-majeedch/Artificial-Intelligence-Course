"""Mechanical licensing-consistency checks for the course repository.

What this verifies
------------------
1. The five licensing documents exist and are non-empty.
2. The MIT text carries the canonical grant, copyright line and warranty disclaimer.
3. The CC BY 4.0 and CC0 1.0 canonical URLs are present and correctly spelled.
4. README and FAQ state the four-layer architecture (code, content, data, third-party) and do not contradict it.
5. The dataset licence names every committed dataset file and excludes external datasets.
6. The third-party register carries attribution fields and explicit exclusions.
7. The licensing inventory covers all ten categories.
8. `CITATION.cff` parses, declares MIT for the software with mixed-licence scope documented, and invents no DOI/ORCID/date.
9. Every relative licence link resolves.
10. No course file still says "no licence applies" / "permission is required".

What this does NOT do
---------------------
It cannot verify authorship, chain of title, permission to redistribute third-party
material, or whether a licence is legally enforceable. Passing this script means the
documents are internally consistent, not that the repository is legally cleared.

Usage:  python audit/check_licensing.py
Exit status 1 if any check fails.
"""

import glob
import json
import os
import re
import sys
import urllib.parse

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REQUIRED_FILES = [
    "LICENSE",
    "CONTENT-LICENSE.md",
    "DATASET-LICENSE.md",
    "THIRD-PARTY-ATTRIBUTIONS.md",
    "LICENSING-INVENTORY.md",
]
LICENCE_DOCS = REQUIRED_FILES + ["CITATION.cff", "README.md", "docs/faq.md"]

CC_BY = "https://creativecommons.org/licenses/by/4.0/"
CC_BY_LEGAL = "https://creativecommons.org/licenses/by/4.0/legalcode"
CC0 = "https://creativecommons.org/publicdomain/zero/1.0/"
CC0_LEGAL = "https://creativecommons.org/publicdomain/zero/1.0/legalcode"

LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
CONTRADICTIONS = [
    r"not offered here under an open licen[cs]e",
    r"permission is required",
    r"all rights reserved",
    r"entire repository is (?:licensed|released) under",
    r"everything (?:here )?is (?:licensed )?under (?:the )?MIT",
]
COURSE_FILES_EXCLUDED = [
    "PHASE-23", "FINAL-", "AUDIT", "REPORT", "LICENSE-AND-ATTRIBUTION-PROPOSAL",
    "LICENSING-INVENTORY", "THIRD-PARTY-ATTRIBUTIONS", "CONTENT-LICENSE", "DATASET-LICENSE",
    "audit/", "LICENSING-AND-REFERENCES-AUDIT",
]


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def check_required(failures):
    for path in REQUIRED_FILES:
        if not os.path.exists(path):
            failures.append(("FILES", path, "missing"))
        elif not read(path).strip():
            failures.append(("FILES", path, "empty"))


def check_mit(failures):
    text = read("LICENSE") if os.path.exists("LICENSE") else ""
    required = [
        "MIT License",
        "Copyright (c) 2026 Muhammad Nadeem Majeed",
        "Permission is hereby granted, free of charge",
        "The above copyright notice and this permission notice shall be included",
        'THE SOFTWARE IS PROVIDED "AS IS"',
        "WITHOUT WARRANTY OF ANY KIND",
    ]
    for marker in required:
        if marker not in text:
            failures.append(("MIT", "LICENSE", f"missing: {marker[:40]}"))
    if "CC BY" in text or "CC0" in text:
        failures.append(("MIT", "LICENSE", "code licence must not claim content/data licences"))


def check_cc_urls(failures):
    content = read("CONTENT-LICENSE.md")
    data = read("DATASET-LICENSE.md")
    for url in (CC_BY, CC_BY_LEGAL):
        if url not in content:
            failures.append(("CC BY", "CONTENT-LICENSE.md", f"missing {url}"))
    for url in (CC0, CC0_LEGAL):
        if url not in data:
            failures.append(("CC0", "DATASET-LICENSE.md", f"missing {url}"))
    if "Attribution" not in content or "indicate changes" not in content.lower():
        failures.append(("CC BY", "CONTENT-LICENSE.md", "attribution/modification terms missing"))
    if "third-party" not in content.lower():
        failures.append(("CC BY", "CONTENT-LICENSE.md", "third-party exclusion missing"))


def check_readme_faq(failures):
    readme = read("README.md")
    faq = read("docs/faq.md")
    for phrase in ("MIT License", "CC BY 4.0", "CC0 1.0", "THIRD-PARTY-ATTRIBUTIONS.md"):
        if phrase not in readme:
            failures.append(("README", "README.md", f"missing {phrase}"))
    if "no single repository-wide licence" not in readme.lower() and \
            "there is no\nsingle repository-wide licence" not in readme.lower():
        failures.append(("README", "README.md", "one-licence disclaimer missing"))
    if "permission is required" in faq or "not offered here under an open licen" in faq:
        failures.append(("FAQ", "docs/faq.md", "still says permission is required"))
    for phrase in ("MIT", "CC BY 4.0", "CC0 1.0"):
        if phrase not in faq:
            failures.append(("FAQ", "docs/faq.md", f"missing {phrase}"))


def check_datasets(failures):
    text = read("DATASET-LICENSE.md")
    for path in glob.glob("modules/*/code/**/*.npz", recursive=True):
        if os.path.basename(path) not in text:
            failures.append(("DATASETS", path, "not listed in DATASET-LICENSE.md"))
    if "dataset_cards.json" not in text:
        failures.append(("DATASETS", "DATASET-LICENSE.md", "dataset cards not referenced"))
    for external in ("Fashion-MNIST", "load_digits", "Iris"):
        if external not in text:
            failures.append(("DATASETS", "DATASET-LICENSE.md", f"external dataset {external} not excluded"))
    cards_path = "modules/M13-responsible-explainable-secure-ai/code/data/dataset_cards.json"
    if os.path.exists(cards_path):
        cards = json.loads(read(cards_path))
        for card in cards:
            if card.get("licence") != "CC0-1.0":
                failures.append(("DATASETS", cards_path,
                                 f"{card.get('name')} licence is {card.get('licence')!r}"))


def check_third_party(failures):
    text = read("THIRD-PARTY-ATTRIBUTIONS.md")
    for marker in ("Licence", "Attribution", "not covered", "Fashion-MNIST",
                   "load_digits", "distilgpt2", "Apache-2.0", "MIT"):
        if marker not in text:
            failures.append(("THIRD-PARTY", "THIRD-PARTY-ATTRIBUTIONS.md", f"missing {marker}"))
    if "distilgpt2" in text and "Apache-2.0" not in text.split("distilgpt2")[1][:200]:
        failures.append(("THIRD-PARTY", "THIRD-PARTY-ATTRIBUTIONS.md",
                         "distilgpt2 licence not stated as Apache-2.0"))


def check_inventory(failures):
    text = read("LICENSING-INVENTORY.md")
    for number in range(1, 11):
        if not re.search(rf"^## {number}\. ", text, re.M):
            failures.append(("INVENTORY", "LICENSING-INVENTORY.md", f"category {number} missing"))
    if "not a legal opinion" not in text.lower():
        failures.append(("INVENTORY", "LICENSING-INVENTORY.md", "legal-review disclaimer missing"))


def check_citation(failures):
    if yaml is None:
        failures.append(("CFF", "CITATION.cff", "PyYAML unavailable; syntax not checked"))
        return
    try:
        data = yaml.safe_load(read("CITATION.cff"))
    except yaml.YAMLError as error:
        failures.append(("CFF", "CITATION.cff", f"YAML error: {error}"))
        return
    for key in ("cff-version", "message", "title", "authors", "repository-code"):
        if key not in data:
            failures.append(("CFF", "CITATION.cff", f"missing {key}"))
    if data.get("license") != "MIT":
        failures.append(("CFF", "CITATION.cff", f"license is {data.get('license')!r}, expected MIT"))
    if "doi" in data or "date-released" in data or "identifiers" in data:
        failures.append(("CFF", "CITATION.cff", "unverified release/archival fields present"))
    author = (data.get("authors") or [{}])[0]
    if author.get("family-names") != "Majeed":
        failures.append(("CFF", "CITATION.cff", "author family name incorrect"))
    if "PUCIT" not in (author.get("affiliation") or ""):
        failures.append(("CFF", "CITATION.cff", "affiliation missing PUCIT"))
    if data.get("repository-code") != "https://github.com/nadeem-majeedch/Artificial-Intelligence-Course":
        failures.append(("CFF", "CITATION.cff", "repository URL incorrect"))


def check_links(failures):
    for path in LICENCE_DOCS:
        if not path.endswith(".md") or not os.path.exists(path):
            continue
        directory = os.path.dirname(path)
        for target in LINK.findall(read(path)):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            file_part = urllib.parse.unquote(target.split("#")[0])
            if not file_part:
                continue
            resolved = os.path.normpath(os.path.join(directory, file_part))
            if not os.path.exists(resolved):
                failures.append(("LINK", path, target))


def check_contradictions(failures):
    for path in glob.glob("**/*.md", recursive=True) + glob.glob("modules/*/code/*.py"):
        normalised = path.replace("\\", "/")
        if any(marker in normalised for marker in COURSE_FILES_EXCLUDED):
            continue
        text = read(path)
        for pattern in CONTRADICTIONS:
            if re.search(pattern, text, re.I):
                failures.append(("CONTRADICTION", normalised, pattern))


def main():
    failures = []
    for check in (check_required, check_mit, check_cc_urls, check_readme_faq,
                  check_datasets, check_third_party, check_inventory, check_citation,
                  check_links, check_contradictions):
        check(failures)
    print(f"licensing checks: {len(failures)} failure(s)")
    for kind, path, detail in failures:
        print(f"  [{kind}] {path}: {detail}")
    print("NOTE: mechanical consistency only; authorship and third-party permission "
          "require human review.")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
