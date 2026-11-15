"""Validate the built MkDocs site.

Checks that the generated site contains the homepage, every module landing page, every lesson,
every laboratory, downloadable notebooks and the required rendering assets. It also verifies the
GitHub project-site base path and rejects generated/private artefacts.

Usage:
    python scripts/check_site.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE = "/Artificial-Intelligence-Course/"


def output_path(source: Path) -> Path:
    relative = source.relative_to(ROOT)
    if relative.name == "README.md":
        # MkDocs maps a directory README to that directory's index page.
        return SITE / relative.parent / "index.html"
    return SITE / relative.with_suffix("") / "index.html"


def require(path: Path, description: str, failures: list[str]) -> None:
    if not path.is_file():
        failures.append(f"missing {description}: {path.relative_to(ROOT)}")


def main() -> int:
    failures: list[str] = []
    require(SITE / "index.html", "homepage", failures)
    require(SITE / "search" / "search_index.json", "search index", failures)
    require(SITE / "sitemap.xml", "sitemap", failures)

    modules = sorted((ROOT / "modules").glob("M[0-9][0-9]-*"))
    lessons = sorted((ROOT / "modules").glob("M*/lessons/L*.md"))
    labs = sorted(
        path
        for path in (ROOT / "modules").glob("M*/labs/*.md")
        if path.name != "README.md"
    )

    for module in modules:
        require(output_path(module / "README.md"), f"module page {module.name}", failures)
    for lesson in lessons:
        require(output_path(lesson), f"lesson {lesson.stem}", failures)
    for lab in labs:
        require(output_path(lab), f"laboratory {lab.stem}", failures)

    # Notebooks are downloads, not rendered pages, but must be shipped unchanged.
    notebooks = sorted((ROOT / "modules").glob("M*/notebooks/*.ipynb"))
    for notebook in notebooks:
        relative = notebook.relative_to(ROOT)
        require(SITE / relative, f"notebook download {notebook.name}", failures)

    for page in (
        "getting-started",
        "laboratories",
        "assignments",
        "projects-and-capstones",
        "quizzes-and-self-assessment",
        "licensing",
        "about-instructor",
    ):
        require(SITE / page / "index.html", f"website page {page}", failures)

    require(SITE / "assets" / "logo.svg", "site logo", failures)
    require(SITE / "stylesheets" / "extra.css", "custom stylesheet", failures)
    require(SITE / "javascripts" / "mathjax.js", "MathJax configuration", failures)
    require(SITE / "javascripts" / "mermaid.js", "Mermaid renderer", failures)

    index = (SITE / "index.html").read_text(encoding="utf-8") if (SITE / "index.html").is_file() else ""
    if BASE not in index:
        failures.append(f"project-site base path {BASE!r} not found in homepage")
    if "tex-mml-chtml.js" not in index:
        failures.append("MathJax runtime is not linked from the homepage")
    if "mathjax.js" not in index:
        failures.append("MathJax configuration is not linked from the homepage")
    if "mermaid.js" not in index:
        failures.append("Mermaid renderer is not linked from the homepage")
    if "extra.css" not in index:
        failures.append("custom stylesheet is not linked from the homepage")

    forbidden = [
        path.relative_to(ROOT).as_posix()
        for path in SITE.rglob("*")
        if (
            path.name in {".git", ".coverage", "__pycache__", ".pytest_cache"}
            or path.name.startswith("_pip_")
            or path.name.startswith("_hf_")
            or path.name.endswith(".log")
            or path.name.startswith("PHASE-")
        )
    ]
    if forbidden:
        failures.append("private/temporary files entered the build: " + ", ".join(forbidden[:10]))

    search = SITE / "search" / "search_index.json"
    if search.is_file():
        try:
            json.loads(search.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            failures.append(f"search index is invalid JSON: {error}")

    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8") if (SITE / "sitemap.xml").is_file() else ""
    module_urls = re.findall(r"https://nadeem-majeedch\.github\.io/Artificial-Intelligence-Course/modules/M\d\d-[^<]+", sitemap)
    if len(module_urls) < 14:
        failures.append(f"sitemap contains {len(module_urls)} module URLs, expected at least 14")

    if failures:
        print(f"SITE CHECKS FAILED: {len(failures)} problem(s)")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(
        f"SITE CHECKS PASS: homepage, {len(modules)} modules, {len(lessons)} lessons, "
        f"{len(labs)} labs, {len(notebooks)} notebooks, assets, search and base path"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
