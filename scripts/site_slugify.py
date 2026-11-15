"""GitHub-compatible heading slugging for the course website.

The course's source links were written for GitHub's heading anchors. Python-Markdown's default
slugger collapses some punctuation differently, which produced broken in-page links in M04. This
function mirrors the slug logic used by ``audit/check_course.py`` so source links and rendered
anchors agree.
"""

from __future__ import annotations

import re


def github_slugify(value: str, separator: str) -> str:
    text = re.sub(r"`", "", value)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return text.replace(" ", separator).strip(separator)
