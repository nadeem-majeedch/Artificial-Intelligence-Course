"""Assemble the MkDocs source tree from the course's source-of-truth files.

The repository keeps lessons, labs, notebooks and assessments in their original course
directories. MkDocs needs a single docs directory, so this script copies those directories into
the git-ignored ``.site-build/docs`` tree for a build. It never edits the source files.

Run from the repository root:

    python scripts/stage_site.py

The script fails if any module, lesson or laboratory is missing, so a broken inventory cannot
silently produce a partial website.
"""

from __future__ import annotations

import posixpath
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
STAGE_ROOT = ROOT / ".site-build"
DOCS = STAGE_ROOT / "docs"

COURSE_DIRS = ("modules", "prerequisites", "resources", "assessments", "docs")
ROOT_FILES = (
    "LICENSE",
    "CONTENT-LICENSE.md",
    "DATASET-LICENSE.md",
    "THIRD-PARTY-ATTRIBUTIONS.md",
    "LICENSING-INVENTORY.md",
    "CITATION.cff",
)
WEBSITE_PAGES = {
    "home.md": "index.md",
    "getting-started.md": "getting-started.md",
    "laboratories.md": "laboratories.md",
    "assignments.md": "assignments.md",
    "projects-and-capstones.md": "projects-and-capstones.md",
    "quizzes-and-self-assessment.md": "quizzes-and-self-assessment.md",
    "licensing.md": "licensing.md",
    "about-instructor.md": "about-instructor.md",
}
ASSET_DIRS = ("assets", "stylesheets", "javascripts")
GITHUB_TREE = "https://github.com/nadeem-majeedch/Artificial-Intelligence-Course/tree/main"
GITHUB_BLOB = "https://github.com/nadeem-majeedch/Artificial-Intelligence-Course/blob/main"
LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")

IGNORED_NAMES = {
    ".git",
    ".freebuff",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
    ".ipynb_checkpoints",
    ".DS_Store",
    "Thumbs.db",
}


def ignore_generated(directory: str, names: list[str]) -> set[str]:
    """Keep caches, logs and editor noise out of the public build."""
    return {
        name
        for name in names
        if name in IGNORED_NAMES
        or name.endswith((".pyc", ".pyo", ".log"))
        or name.startswith("_pip_")
        or name.startswith("_hf_")
    }


def copy_tree(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, ignore=ignore_generated)


def rewrite_staged_links() -> None:
    """Adapt repository-relative links for the public site.

    * The source README is staged as ``course-home.md`` to avoid MkDocs' README/index conflict.
      Links that pointed at the repository README are redirected to that page, preserving anchors.
    * Links to source directories (for example ``code/``) are redirected to the matching GitHub
      tree, because MkDocs cannot render a directory as a page.

    Only the generated staging tree is changed; source Markdown is untouched.
    """
    course_home = DOCS / "course-home.md"

    for page in DOCS.rglob("*.md"):
        lines = page.read_text(encoding="utf-8").splitlines(keepends=True)
        in_fence = False
        rewritten: list[str] = []
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith(("```", "~~~")):
                in_fence = not in_fence
                rewritten.append(line)
                continue
            if in_fence:
                rewritten.append(line)
                continue

            def replace(match: re.Match[str]) -> str:
                label, target, title = match.group(1), match.group(2), match.group(3) or ""
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    return match.group(0)
                file_part, marker, anchor = target.partition("#")
                if not file_part:
                    return match.group(0)
                resolved = (page.parent / unquote(file_part)).resolve()

                replacement: str | None = None
                if resolved in {course_home.resolve(), (DOCS / "README.md").resolve()}:
                    replacement = posixpath.relpath(
                        course_home.relative_to(DOCS).as_posix(),
                        page.parent.relative_to(DOCS).as_posix() or ".",
                    )
                else:
                    try:
                        relative = resolved.relative_to(DOCS.resolve()).as_posix()
                    except ValueError:
                        # A link to a repository file or directory that is deliberately not
                        # copied into the website (templates, ownership checklist).
                        try:
                            root_relative = resolved.relative_to(ROOT.resolve()).as_posix()
                        except ValueError:
                            return match.group(0)
                        if resolved.is_dir():
                            replacement = f"{GITHUB_TREE}/{root_relative}/"
                        elif resolved.is_file():
                            replacement = f"{GITHUB_BLOB}/{root_relative}"
                    else:
                        if resolved.is_dir():
                            replacement = f"{GITHUB_TREE}/{relative}/"
                        elif not resolved.exists():
                            # Staging mirrors the repository, so a missing website target can
                            # still be linked to its source on GitHub.
                            candidate = ROOT / relative
                            if candidate.is_dir():
                                replacement = f"{GITHUB_TREE}/{relative}/"
                            elif candidate.is_file():
                                replacement = f"{GITHUB_BLOB}/{relative}"

                if replacement is None:
                    return match.group(0)
                suffix = f"{marker}{anchor}" if marker else ""
                return f"[{label}]({replacement}{suffix}{title})"

            rewritten.append(LINK.sub(replace, line))
        page.write_text("".join(rewritten), encoding="utf-8")

    # Generated corpus/output Markdown is data, not a collection of web pages.
    for path in list((DOCS / "modules").glob("*/code/**/*.md")):
        path.unlink()


def validate_inventory() -> None:
    modules = sorted((ROOT / "modules").glob("M[0-9][0-9]-*"))
    lessons = sorted((ROOT / "modules").glob("M*/lessons/L*.md"))
    labs = sorted(
        path
        for path in (ROOT / "modules").glob("M*/labs/*.md")
        if path.name != "README.md"
    )
    if len(modules) != 14:
        raise SystemExit(f"expected 14 module directories, found {len(modules)}")
    if len(lessons) != 89:
        raise SystemExit(f"expected 89 lessons, found {len(lessons)}")
    if len(labs) != 38:
        raise SystemExit(f"expected 38 laboratories, found {len(labs)}")
    missing = [
        module / "README.md"
        for module in modules
        if not (module / "README.md").is_file()
    ]
    if missing:
        raise SystemExit(f"module landing pages missing: {missing}")


def main() -> int:
    validate_inventory()
    if STAGE_ROOT.exists():
        shutil.rmtree(STAGE_ROOT)
    DOCS.mkdir(parents=True)

    for directory in COURSE_DIRS:
        copy_tree(ROOT / directory, DOCS / directory)

    for filename in ROOT_FILES:
        shutil.copy2(ROOT / filename, DOCS / filename)
    shutil.copy2(ROOT / "README.md", DOCS / "course-home.md")

    website = ROOT / "website"
    for source_name, target_name in WEBSITE_PAGES.items():
        source = website / source_name
        if not source.is_file():
            raise SystemExit(f"website page missing: {source}")
        shutil.copy2(source, DOCS / target_name)

    for directory in ASSET_DIRS:
        copy_tree(website / directory, DOCS / directory)

    rewrite_staged_links()

    # A small marker makes it obvious that this tree is generated and must not be edited.
    (DOCS / ".generated-by-stage-site").write_text(
        "Generated by scripts/stage_site.py. Do not edit; source files live in the repository.\n",
        encoding="utf-8",
    )

    lesson_count = len(list((DOCS / "modules").glob("M*/lessons/L*.md")))
    lab_count = len(
        [
            path
            for path in (DOCS / "modules").glob("M*/labs/*.md")
            if path.name != "README.md"
        ]
    )
    print(
        f"staged {len(list((DOCS / 'modules').glob('M*/README.md')))} modules, "
        f"{lesson_count} lessons, {lab_count} laboratories into {DOCS}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
