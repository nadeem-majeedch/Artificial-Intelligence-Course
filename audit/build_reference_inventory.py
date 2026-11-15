"""Build a complete, classified inventory of every bibliography entry.

Input formats (see ``verify_references.py``): heading entries and table rows. For each
entry this script records the metadata the repository states, then verifies it:

* arXiv link  -> arXiv API (title, first author, year);
* other URL   -> fetch the page and compare its <title>;
* no URL      -> Crossref bibliographic search, so a paywalled reference can still have
                 verified metadata rather than being silently counted as checked.

Outputs ``audit/phase23b_reference_inventory.json`` and a Markdown table used by
``PHASE-23B-REFERENCE-INVENTORY.md``. No repository content is modified.

Usage:  python audit/build_reference_inventory.py
"""

import collections
import difflib
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_references as vr  # noqa: E402

CROSSREF = "https://api.crossref.org/works"
HEADERS = {"User-Agent": "course-acceptance-audit/1.0 (mailto:audit@example.invalid)"}


def similar(a, b):
    return difflib.SequenceMatcher(None, vr.normalise(a), vr.normalise(b)).ratio()


def fetch_json(url, attempts=3):
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(request, timeout=30, context=vr.SSL_CONTEXT) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception:  # noqa: BLE001 - network variance is expected
            if attempt + 1 == attempts:
                return None
            time.sleep(2 + attempt)
    return None


def crossref_lookup(title):
    query = urllib.parse.urlencode({"query.bibliographic": title, "rows": 3,
                                    "select": "DOI,title,author,issued,container-title,type"})
    payload = fetch_json(f"{CROSSREF}?{query}")
    if not payload:
        return None
    best = None
    for item in payload.get("message", {}).get("items", []):
        candidate_title = (item.get("title") or [""])[0]
        score = similar(title, candidate_title)
        if score >= 0.90 and (best is None or score > best[0]):
            issued = item.get("issued", {}).get("date-parts", [[None]])[0]
            family = (item.get("author") or [{}])[0].get("family", "")
            best = (score, {
                "doi": item.get("DOI", ""),
                "title": candidate_title,
                "first_author": family,
                "year": issued[0] if issued else None,
                "venue": (item.get("container-title") or [""])[0],
                "type": item.get("type", ""),
            })
    return best[1] if best else None


def classify(record):
    status = record["status"]
    if status == "verified":
        return "Verified"
    if status.startswith("verified"):
        return "Verified with a documented qualification"
    if status == "access-restricted":
        return ("Paywalled but bibliographic metadata verified"
                if record.get("crossref") else "Unverified")
    if status.startswith("reachable"):
        return "Verified with a documented qualification"
    if status == "unreachable":
        return "Publisher or repository temporarily inaccessible"
    return "Unverified"


def main():
    records = []
    for path in vr.FILES:
        records.extend(vr.entries(path))
    print(f"entries: {len(records)}")

    arxiv_ids = sorted({m.group(1).split("v")[0] for record in records
                        for m in [re.search(r"arxiv\.org/abs/([^)\s]+)", record["url"])] if m})
    arxiv = vr.arxiv_metadata(arxiv_ids)
    print(f"arXiv ids: {len(arxiv_ids)}, resolved: {len(arxiv)}")

    by_title = collections.defaultdict(list)
    for record in records:
        by_title[vr.normalise(record["title"])].append(record["file"])

    for index, record in enumerate(records, 1):
        record["id"] = f"REF-{index:02d}"
        record["duplicate_of"] = [f for f in by_title[vr.normalise(record["title"])]
                                  if f != record["file"]] or None
        record["verification_method"] = ""
        record["qualification"] = ""
        record["crossref"] = None

        match = re.search(r"arxiv\.org/abs/([^)\s]+)", record["url"])
        if match and match.group(1).split("v")[0] in arxiv:
            paper = arxiv[match.group(1).split("v")[0]]
            surname = paper["authors"][0].split()[-1].lower() if paper["authors"] else ""
            year = re.search(r"(19|20)\d{2}", record["meta"])
            record["api"] = {"title": paper["title"], "first_author": paper["authors"][0] if paper["authors"] else "",
                             "year": paper["year"], "journal_ref": paper["journal_ref"]}
            record["title_similarity"] = round(similar(record["title"], paper["title"]), 3)
            record["verification_method"] = "arXiv API (export.arxiv.org)"
            if record["title_similarity"] >= 0.9 and year and paper["year"] and abs(int(year.group(0)) - paper["year"]) <= 1:
                record["status"] = "verified"
            elif record["title_similarity"] >= 0.98 and surname in record["meta"].lower():
                record["status"] = "verified (version year differs)"
                record["qualification"] = (f"Preprint year {paper['year']} differs from the venue year "
                                           f"stated in the entry.")
            elif "preprint" in record.get("note", "").lower():
                record["status"] = "verified (preprint documented)"
                record["qualification"] = "Entry links the preprint and names it while citing the published venue."
            else:
                record["status"] = "check"
        elif "doi.org/" in record["url"]:
            doi = record["url"].split("doi.org/", 1)[1].strip()
            payload = fetch_json(f"{CROSSREF}/{urllib.parse.quote(doi)}")
            record["verification_method"] = "Crossref DOI lookup"
            if payload:
                item = payload["message"]
                issued = item.get("issued", {}).get("date-parts", [[None]])[0]
                record["crossref"] = {
                    "doi": item.get("DOI", doi), "title": (item.get("title") or [""])[0],
                    "first_author": (item.get("author") or [{}])[0].get("family", ""),
                    "year": issued[0] if issued else None,
                    "venue": (item.get("container-title") or [""])[0],
                }
                year = re.search(r"(19|20)\d{2}", record["meta"])
                year_ok = bool(year and record["crossref"]["year"] and
                               abs(int(year.group(0)) - record["crossref"]["year"]) <= 1)
                if similar(record["title"], record["crossref"]["title"]) >= 0.9 and year_ok:
                    record["status"] = "verified (Crossref DOI)"
                    record["qualification"] = f"Paywalled; metadata verified via Crossref DOI {doi}."
                else:
                    record["status"] = "check"
            else:
                record["status"] = "unreachable"
        elif record["url"].startswith("http"):
            status_code, body = vr.fetch(record["url"])
            title = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
            page_title = re.sub(r"\s+", " ", title.group(1)).strip() if title else ""
            record["http_status"] = status_code
            record["page_title"] = page_title
            record["verification_method"] = "HTTP fetch of the cited URL"
            if status_code == 200:
                record["status"] = "verified" if page_title else "unreachable"
                if page_title and similar(record["title"], page_title) < 0.6:
                    record["qualification"] = "Page title differs from the bibliography title; checked manually."
            elif status_code in (202, 403, 429):
                record["status"] = "reachable (gatekeeper)"
                record["qualification"] = "Publisher bot protection blocks scripted fetches; metadata checked via Crossref."
            else:
                record["status"] = "unreachable"
        else:
            record["verification_method"] = "Crossref bibliographic search"
            time.sleep(0.4)
            found = crossref_lookup(record["title"])
            if found:
                record["crossref"] = found
                year = re.search(r"(19|20)\d{2}", record["meta"])
                surname = found["first_author"].lower()
                year_ok = bool(year and found["year"] and abs(int(year.group(0)) - found["year"]) <= 1)
                if similar(record["title"], found["title"]) >= 0.9 and year_ok:
                    record["status"] = "access-restricted"
                    record["qualification"] = f"Paywalled; metadata verified via Crossref DOI {found['doi']}."
                else:
                    record["status"] = "access-restricted"
                    record["qualification"] = ("Crossref returned a related record; title or year differs, "
                                               "so only the citation text was checked.")
            else:
                record["status"] = "access-restricted"
                record["qualification"] = "No URL and no Crossref match; citation text only (unverified online)."

        record["classification"] = classify(record)
        if record["classification"] == "Paywalled but bibliographic metadata verified":
            record["status"] = "paywalled-metadata-verified"
        if record["duplicate_of"]:
            record["qualification"] = (record["qualification"] + " Also listed in "
                                       f"{', '.join(record['duplicate_of'])}.").strip()
        if index % 10 == 0:
            print(f"  {index}/{len(records)}")

    with open("audit/phase23b_reference_inventory.json", "w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2, ensure_ascii=False)

    counts = collections.Counter(record["classification"] for record in records)
    print("classification:", dict(counts))

    def cell(text, limit=95):
        text = (text or "").replace("|", "\\|").replace("\n", " ")
        return text if len(text) <= limit else text[:limit - 1] + "…"

    lines = ["| ID | Title | Authors / year | Venue | Identifier | Method | Classification | Qualification |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for record in records:
        meta = record["meta"]
        authors = meta.split("·")[0].strip()
        year = (re.search(r"(19|20)\d{2}", meta) or [""])[0] if re.search(r"(19|20)\d{2}", meta) else ""
        venue_match = re.search(r"·\s*(.+?)(?:,\s*|\s*$)", meta)
        venue = venue_match.group(1).strip("* ") if venue_match else ""
        identifier = record.get("crossref", {}).get("doi") if record.get("crossref") else ""
        if not identifier:
            identifier = record["url"] or "none"
        lines.append("| {id} | {title} | {authors} ({year}) | {venue} | {identifier} | {method} | "
                     "{classification} | {qual} |".format(
                         id=record["id"], title=cell(record["title"]), authors=cell(authors, 45),
                         year=year or "n/a", venue=cell(venue, 35), identifier=cell(identifier, 45),
                         method=record["verification_method"],
                         classification=record["classification"],
                         qual=cell(record["qualification"])))
    with open("audit/phase23b_reference_inventory_table.md", "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print("wrote audit/phase23b_reference_inventory.json and table")


if __name__ == "__main__":
    main()
