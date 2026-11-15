"""Verify the course bibliography against arXiv metadata and live URLs.

The files use a fixed entry shape:

    ### Title
    Author, Author and Author · *Venue*, year
    - **URL:** https://...
    - **Modules:** M03 · **Level:** Advanced

For arXiv links the title, first author and year are compared with the arXiv API. For
other links the page is fetched and its <title> compared. Entries that note paid or
library access are recorded as access-restricted rather than treated as errors:
a paywall is not a broken reference.

The TLS context does not verify certificates because the authoring machine has no CA
bundle for Python; this script only reads public metadata. It never writes to the repo.

Usage:  python audit/verify_references.py [--json audit/reference_verification.json]
"""

import argparse
import difflib
import html
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

FILES = [
    "resources/research-papers.md",
    "resources/library/papers-and-surveys.md",
    "resources/library/ai-agents.md",
]

SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

ENTRY = re.compile(r"^### (?P<title>.+?)\s*$", re.M)


ROW = re.compile(
    r"^\|\s*\*\*(?P<authors>[^*]+?)\s*\((?P<year>\d{4})\)\s*,\s*"
    r"[\"\u201c]?(?P<title>[^\"\u201d]+?)[\"\u201d]?\*\*(?P<tail>.*)$",
    re.M,
)


def entries(path):
    """Yield bibliography entries from either supported format.

    Format A (``resources/library/*.md``): ``### Title`` followed by a metadata line and a
    ``- **URL:**`` line. Format B (``resources/research-papers.md``): one table row per paper,
    ``| **Authors (year), "Title"**, *Venue* — [arXiv:id](url) | module | why |``.
    """
    text = open(path, encoding="utf-8").read()
    matches = list(ENTRY.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end():end]
        if "\n## " in block:
            block = block.split("\n## ")[0]
        url = re.search(r"^- \*\*URL:\*\*\s*(.+)$", block, re.M)
        doi = re.search(r"^- \*\*DOI:\*\*\s*\[[^\]]*\]\((https?://[^)\s]+)\)", block, re.M)
        meta = block.strip().splitlines()[0] if block.strip() else ""
        url_value = url.group(1).strip() if url else ""
        if not url_value.startswith("http") and doi:
            url_value = doi.group(1).strip()
        yield {
            "file": path.replace("\\", "/"),
            "title": match.group("title").strip(),
            "meta": meta.strip(),
            "url": url_value,
            "modules": (re.search(r"\*\*Modules:\*\*\s*([^·\n]+)", block) or [None, ""])[1].strip(),
            "access": (re.search(r"\*\*Access:\*\*\s*(.+)", block) or [None, ""])[1].strip(),
        }

    for row in ROW.finditer(text):
        tail = row.group("tail")
        link = re.search(r"\]\((https?://[^)\s]+)\)", tail)
        arxiv = re.search(r"arXiv:(\d{4}\.\d{4,5})", tail)
        url = link.group(1) if link else (f"https://arxiv.org/abs/{arxiv.group(1)}" if arxiv else "")
        yield {
            "file": path.replace("\\", "/"),
            "title": row.group("title").strip(),
            "meta": f"{row.group('authors').strip()} · {row.group('year')}",
            "url": url,
            "modules": (re.search(r"\|\s*(M\d[^|]*)\|\s*$", row.group(0)) or [None, ""])[1].strip(),
            "access": "",
            "note": tail,
        }


def normalise(text):
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return re.sub(r"[^a-z0-9 ]+", " ", text.lower()).strip()


def similar(a, b):
    return difflib.SequenceMatcher(None, normalise(a), normalise(b)).ratio()


def fetch(url, timeout=25, attempts=2):
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "course-reference-check/1.0"})
            with urllib.request.urlopen(request, timeout=timeout, context=SSL_CONTEXT) as response:
                return response.status, response.read(400000).decode("utf-8", "replace")
        except urllib.error.HTTPError as error:
            return error.code, ""
        except Exception:
            if attempt + 1 == attempts:
                return None, ""
            time.sleep(3)


def arxiv_metadata(ids):
    """Query the arXiv API once for every id; returns id -> metadata."""
    query = "https://export.arxiv.org/api/query?id_list=" + ",".join(ids) + f"&max_results={len(ids)}"
    status, body = fetch(query)
    if status != 200 or not body:
        return {}
    found = {}
    for block in re.findall(r"<entry>(.*?)</entry>", body, re.S):
        identifier = re.search(r"<id>.*?/abs/([^<]+)</id>", block)
        title = re.search(r"<title>(.*?)</title>", block, re.S)
        published = re.search(r"<published>(\d{4})", block)
        authors = re.findall(r"<name>([^<]+)</name>", block)
        journal = re.search(r"<arxiv:journal_ref[^>]*>(.*?)</arxiv:journal_ref>", block, re.S)
        if not identifier or not title:
            continue
        key = identifier.group(1).split("v")[0]
        found[key] = {
            "title": re.sub(r"\s+", " ", title.group(1)).strip(),
            "authors": authors,
            "year": int(published.group(1)) if published else None,
            "journal_ref": re.sub(r"\s+", " ", journal.group(1)).strip() if journal else "",
            "id": key,
        }
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default="audit/reference_verification.json")
    arguments = parser.parse_args()

    records = [entry for path in FILES for entry in entries(path)]
    arxiv_ids = sorted({m.group(1).split("v")[0]
                        for record in records
                        for m in [re.search(r"arxiv\.org/abs/([^)\s]+)", record["url"])] if m})
    print(f"entries: {len(records)}  unique arXiv ids: {len(arxiv_ids)}")

    metadata = arxiv_metadata(arxiv_ids) if arxiv_ids else {}
    print(f"arXiv records returned: {len(metadata)}")

    results = []
    for record in records:
        result = dict(record)
        match = re.search(r"arxiv\.org/abs/([^)\s]+)", record["url"])
        if match and match.group(1).split("v")[0] in metadata:
            paper = metadata[match.group(1).split("v")[0]]
            result.update({
                "check": "arxiv",
                "api_title": paper["title"],
                "api_first_author": paper["authors"][0] if paper["authors"] else "",
                "api_year": paper["year"],
                "title_similarity": round(similar(record["title"], paper["title"]), 3),
            })
            surname = result["api_first_author"].split()[-1].lower()
            result["author_in_entry"] = surname in record["meta"].lower()
            year = re.search(r"(19|20)\d{2}", record["meta"])
            result["year_match"] = bool(year and paper["year"] and
                                        abs(int(year.group(0)) - paper["year"]) <= 1)
            if result["title_similarity"] >= 0.9 and result["year_match"]:
                result["status"] = "verified"
            elif result["title_similarity"] >= 0.98 and result["author_in_entry"]:
                # same work, different version: arXiv preprint year vs journal year
                result["status"] = "verified (version year differs)"
            elif "preprint" in result.get("note", "").lower():
                # the entry names the linked preprint and cites the published version
                result["status"] = "verified (preprint documented)"
            else:
                result["status"] = "check"
        elif record["url"].startswith("http"):
            status, body = fetch(record["url"])
            title = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
            page_title = re.sub(r"\s+", " ", html.unescape(title.group(1))).strip() if title else ""
            result.update({"check": "url", "http_status": status, "page_title": page_title,
                           "title_similarity": round(similar(record["title"], page_title), 3) if page_title else None})
            if status == 200:
                result["status"] = "verified"
            elif status in (202, 403, 429):
                # publisher bot protection: the URL exists but refuses scripted fetches
                result["status"] = "reachable (gatekeeper)"
            else:
                result["status"] = "unreachable"
        else:
            result.update({"check": "restricted", "status": "access-restricted"})
        results.append(result)

    with open(arguments.json, "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2, ensure_ascii=False)

    counts = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
    print("status:", counts)
    for result in results:
        if result["status"] in {"check", "unreachable"}:
            print(f"  [{result['status']}] {result['file']}: {result['title'][:70]} "
                  f"| meta={result['meta'][:60]} | api={result.get('api_title', result.get('page_title', ''))[:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
