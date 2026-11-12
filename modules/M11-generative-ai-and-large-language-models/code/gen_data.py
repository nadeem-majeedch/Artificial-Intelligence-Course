"""gen_data.py -- the module corpus, question sets and a tiny PDF writer (M11).

Everything here is authored for this module and released under CC0-1.0, so the
notebooks and labs can be run, copied and redistributed without a licence
question. The handbook is intentionally fictional: Northfield University does
not exist, and no real institution's policy is described.

Contents
    HANDBOOK       24 short policy documents (id -> {title, text})
    QA             30 answerable questions with a gold answer and source id
    UNANSWERABLE   questions the handbook cannot answer (hallucination probes)
    SENTENCES      40 labelled sentences for LLM sentiment comparison

Run ``python gen_data.py`` to write corpus/*.md, corpus/northfield-handbook.pdf,
the QA files and a summary of the splits.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS_DIR = HERE / "corpus"

# ---------------------------------------------------------------------------
# 1. The corpus
# ---------------------------------------------------------------------------
# Each document is one chunk-sized unit (roughly 90-160 words). Several topics
# are deliberately confusable (library vs IT helpdesk hours, tuition vs
# accommodation fees) so that retrieval has something to get wrong.

HANDBOOK = {
    "hb-01": {
        "title": "Library opening hours",
        "text": (
            "The Hartley Library on the Northfield campus is open from 08:00 to 23:00 "
            "Monday to Friday during term time, and from 10:00 to 18:00 at weekends. "
            "During the summer vacation the library closes at 20:00 on weekdays and is "
            "closed on Sundays. The 24-hour study centre on level two stays open all "
            "night, every day of the year, and is accessible with a valid student card. "
            "Group study rooms can be booked online up to seven days in advance, for a "
            "maximum of three hours per booking."
        ),
    },
    "hb-02": {
        "title": "Book borrowing and renewals",
        "text": (
            "Undergraduates may borrow up to 12 items at a time, postgraduates up to 25, "
            "and staff up to 40. Standard loans last 21 days and renew automatically up "
            "to three times unless another reader has reserved the item. Reserved items "
            "must be returned within seven days. The daily overdue charge is 0.40 GBP per "
            "item, capped at 15 GBP per item. Items borrowed through the inter-library "
            "loan service are held for collection for ten days and cannot be renewed."
        ),
    },
    "hb-03": {
        "title": "IT helpdesk and account support",
        "text": (
            "The IT helpdesk in the Sinclair Building answers calls from 07:30 to 20:00 "
            "Monday to Friday and from 09:00 to 16:00 on Saturdays. It is closed on "
            "Sundays and on public holidays. Password resets can be completed online "
            "through the self-service portal at any time. Hardware faults are logged as "
            "tickets and the target response is one working day for staff and two working "
            "days for students. Lost student cards are replaced at the helpdesk for a fee "
            "of 12 GBP, and the replacement is printed while you wait."
        ),
    },
    "hb-04": {
        "title": "Wi-Fi and network access",
        "text": (
            "The campus wireless network is called Northfield-Secure and requires your "
            "student account credentials. Eduroam is available in all teaching buildings. "
            "Wired connections in halls of residence are provided by the accommodation "
            "provider, not by the university, and faults should be reported to the hall "
            "reception. Streaming services are rate-limited between 18:00 and midnight on "
            "the shared network. Virtual private network access is required for library "
            "databases from off campus, and the client is available for Windows, macOS "
            "and Linux."
        ),
    },
    "hb-05": {
        "title": "Tuition fees and payment deadlines",
        "text": (
            "Undergraduate tuition for home students is 9,250 GBP per year. International "
            "undergraduate tuition is 21,400 GBP per year, and postgraduate taught tuition "
            "is 24,900 GBP per year. Fees may be paid in full at enrolment or in three "
            "instalments due on 15 October, 15 January and 15 April. A late payment charge "
            "of 1.5 percent per month applies to unpaid instalments after 14 days. Students "
            "experiencing financial difficulty should contact the money advice team before "
            "the deadline rather than after it."
        ),
    },
    "hb-06": {
        "title": "Scholarships and bursaries",
        "text": (
            "The Northfield Merit Scholarship pays 3,000 GBP per year to entrants with "
            "three A grades at A level or equivalent, and is renewed automatically if the "
            "student averages 65 percent or higher. The Hardship Bursary is means-tested "
            "and awards between 500 and 2,500 GBP per year; applications open on 1 "
            "September and close on 31 October. Care-leaver support covers accommodation "
            "costs in full for the first year. Scholarships are not repayable and do not "
            "affect eligibility for a student loan."
        ),
    },
    "hb-07": {
        "title": "Accommodation fees and contracts",
        "text": (
            "University-managed halls cost between 128 and 176 GBP per week including "
            "utilities and internet. Contracts run for 44 weeks for undergraduates and 51 "
            "weeks for postgraduates. A deposit of 400 GBP is required to secure a room and "
            "is refunded within 28 days of the end of the contract, less any damage "
            "charges. Cancellation is free within 14 days of accepting the offer. Private "
            "rental accommodation is not covered by the university contract and disputes "
            "are handled by the students' union advice service."
        ),
    },
    "hb-08": {
        "title": "Examination rules",
        "text": (
            "Students must arrive 15 minutes before an examination starts. Admission after "
            "30 minutes past the start time is refused. Only transparent water bottles and "
            "approved calculators may be taken to the desk; bags are left at the back of "
            "the hall. Mobile phones must be switched off and stored, not merely silenced. "
            "A candidate who is ill should submit a mitigating circumstances form within "
            "five working days with medical evidence, rather than sit the examination and "
            "appeal the mark afterwards."
        ),
    },
    "hb-09": {
        "title": "Assessment, marking and grade bands",
        "text": (
            "Undergraduate modules are marked on a percentage scale: 70 and above is a "
            "first, 60 to 69 an upper second, 50 to 59 a lower second, 40 to 49 a third, "
            "and below 40 a fail. Postgraduate modules require 50 percent to pass and 70 "
            "for a distinction. Marks are provisional until the examination board meets in "
            "June. Coursework is returned within 15 working days of the deadline. A module "
            "mark is capped at 40 when it is passed on a resit."
        ),
    },
    "hb-10": {
        "title": "Extensions, late submission and mitigating circumstances",
        "text": (
            "Coursework submitted after the published deadline loses 10 percent of the "
            "available marks per working day, up to a maximum of five days, after which it "
            "scores zero. Self-certified extensions of up to seven days are available once "
            "per academic year for eligible modules. Longer extensions require evidence and "
            "the module leader's approval. Mitigating circumstances are submitted to the "
            "faculty office, not to the module leader, within five working days of the "
            "assessment."
        ),
    },
    "hb-11": {
        "title": "Academic integrity and misconduct",
        "text": (
            "All submitted work must be the student's own. Contract cheating, including "
            "paying another person to write an assignment, is a category one offence and "
            "normally results in exclusion from the programme. Unacknowledged use of "
            "another author's words or ideas is plagiarism, whether the source is a book, a "
            "web page or a generative artificial intelligence tool. Using an AI tool to "
            "produce assessed work without permission is treated as misconduct. The "
            "university's similarity checking service compares submissions against a "
            "database of previous work."
        ),
    },
    "hb-12": {
        "title": "Attendance and leave of absence",
        "text": (
            "Attendance at timetabled sessions is recorded and students on a student visa "
            "must attend at least 80 percent of scheduled contact hours to comply with "
            "sponsorship conditions. Absence through illness of more than seven days needs "
            "a medical certificate. A leave of absence may be granted for one academic year "
            "in exceptional circumstances, and the request must be made before the end of "
            "the second teaching week. Returning students re-enter at the same stage of the "
            "programme."
        ),
    },
    "hb-13": {
        "title": "Student support and counselling",
        "text": (
            "The wellbeing service offers free, confidential counselling and is open from "
            "09:00 to 17:00 Monday to Friday in the Lawson Centre. Appointments can be "
            "booked online or by telephone, and urgent same-day appointments are available "
            "each morning. The service does not provide crisis care outside office hours; "
            "the emergency number for the campus security team operates continuously. "
            "Disability support arranges adjustments such as extra time in examinations, "
            "and applications should be made at least six weeks before the assessment."
        ),
    },
    "hb-14": {
        "title": "Health services and emergencies",
        "text": (
            "The campus health centre is a general practice surgery and requires "
            "registration; it is open 08:30 to 18:00 on weekdays. For emergencies call "
            "999. The campus security team can be reached on the internal extension 2222 "
            "at any hour and can summon an ambulance. A defibrillator is located in the "
            "entrance of every teaching building. International students who pay the "
            "immigration health surcharge are entitled to use National Health Service "
            "treatment on the same basis as residents."
        ),
    },
    "hb-15": {
        "title": "International student office and visas",
        "text": (
            "The international office in the Ashworth Building advises on visas, "
            "immigration and working restrictions. Students on a student visa may work up "
            "to 20 hours per week during term time and full time in the vacations. "
            "Registration with the police is required for nationals of certain countries "
            "and must be completed within seven days of arrival. The office issues "
            "attendance letters for visa applications within three working days. Visa "
            "advice is free; the office cannot give legal advice on immigration appeals."
        ),
    },
    "hb-16": {
        "title": "Clubs, societies and sports",
        "text": (
            "The students' union recognises more than 140 societies. Membership fees are "
            "set by each society and typically range from 3 to 25 GBP per year. The sports "
            "centre offers a student membership of 180 GBP per year or 6 GBP per visit, and "
            "includes the swimming pool, gym and courts. Club transport to away fixtures is "
            "subsidised by 50 percent. New societies need 15 registered members and a "
            "constitution approved by the union, and can apply for a start-up grant of up "
            "to 150 GBP."
        ),
    },
    "hb-17": {
        "title": "Careers service and placements",
        "text": (
            "The careers service runs drop-in sessions from 10:00 to 16:00 on weekdays and "
            "offers one-to-one appointments with a careers adviser. Placement years are "
            "arranged through the faculty placement office and must be approved before the "
            "end of the second year. Students on a placement year pay a reduced tuition fee "
            "of 1,850 GBP. The service reviews applications and runs mock interviews, but "
            "does not guarantee an interview or a placement."
        ),
    },
    "hb-18": {
        "title": "Complaints and academic appeals",
        "text": (
            "A complaint about a service should first be raised informally with the "
            "relevant department. A formal complaint must be submitted within 20 working "
            "days using the online form. Academic appeals are limited to procedural "
            "irregularity, new evidence not available at the time, or bias; disagreeing "
            "with the academic judgement of an examiner is not grounds for appeal. Appeals "
            "must be lodged within 15 working days of the publication of results, and the "
            "outcome is normally issued within 30 working days."
        ),
    },
    "hb-19": {
        "title": "Graduation and awards",
        "text": (
            "Graduation ceremonies are held in July and December in the Northfield "
            "Assembly Hall. Students must have completed all assessments and cleared any "
            "outstanding debt to the university before a certificate is issued. Guest "
            "tickets are limited to two per graduand and additional tickets are allocated "
            "by ballot. Academic dress hire costs 45 GBP and must be ordered at least 14 "
            "days before the ceremony. Degree certificates are posted within eight weeks "
            "of the ceremony."
        ),
    },
    "hb-20": {
        "title": "Parking and campus transport",
        "text": (
            "Student parking permits cost 120 GBP per year and are allocated by lottery "
            "because demand exceeds supply; students living within two miles of campus are "
            "not eligible. Visitors pay 1.60 GBP per hour in the pay-and-display car park. "
            "The campus shuttle runs every 15 minutes from 07:00 to 22:00 between the main "
            "site and the halls. Bicycle storage is free and covered, and a repair stand is "
            "available outside the sports centre. Parking fines are 40 GBP, reduced to 20 "
            "GBP if paid within 14 days."
        ),
    },
    "hb-21": {
        "title": "Printing, copying and study spaces",
        "text": (
            "Students receive a printing credit of 5 GBP per term, which covers "
            "approximately 250 black-and-white pages. Additional credit is purchased "
            "online at 0.02 GBP per page for black and white and 0.08 GBP for colour. "
            "Printers are located on every floor of the library and in the Sinclair "
            "Building. Silent study floors are levels three and four; group discussion is "
            "permitted on level two. Poster printing is handled by the media centre and "
            "requires three working days' notice."
        ),
    },
    "hb-22": {
        "title": "Laboratory and workshop safety",
        "text": (
            "Safety glasses and laboratory coats are mandatory in all wet laboratories. "
            "Food and drink are prohibited. Students must complete the online induction "
            "before their first practical session and must not work alone outside staffed "
            "hours. Accidents, however minor, must be reported to the technician on duty "
            "and recorded in the accident book. Waste chemicals are disposed of in the "
            "labelled containers only; sinks are not for chemical disposal."
        ),
    },
    "hb-23": {
        "title": "Data protection and student records",
        "text": (
            "The university processes personal data under the UK General Data Protection "
            "Regulation. Students may request a copy of their records through a subject "
            "access request, which is answered within one month. Contact details are shared "
            "with the students' union unless the student opts out. Examination scripts are "
            "retained for 12 months and then destroyed. Name changes must be supported by "
            "documentary evidence and are processed within ten working days."
        ),
    },
    "hb-24": {
        "title": "Religious observance and diversity",
        "text": (
            "The multi-faith chaplaincy in the Old Chapel provides prayer rooms, quiet "
            "space and confidential conversation for students of any religion or none. "
            "Prayer facilities are open from 07:00 to 22:00 and include washing areas. "
            "Students may request timetable adjustments for religious festivals by "
            "contacting the faculty office at least 14 days in advance. The equality and "
            "diversity team advises on harassment and discrimination complaints, which can "
            "also be reported anonymously through the online reporting tool."
        ),
    },
}

# ---------------------------------------------------------------------------
# 2. Questions
# ---------------------------------------------------------------------------
# ``source`` is the document that contains the answer; ``span`` is the sentence a
# correct extractive system should return. Single-document questions dominate,
# with a few that need two documents (marked in ``hard``).

QA = [
    {"q": "What time does the Hartley Library open on weekdays in term time?",
     "a": "08:00", "source": "hb-01"},
    {"q": "How many items can an undergraduate borrow at once?",
     "a": "12", "source": "hb-02"},
    {"q": "What is the daily overdue charge for a library item?",
     "a": "0.40 GBP per item", "source": "hb-02"},
    {"q": "When is the IT helpdesk open on Saturdays?",
     "a": "09:00 to 16:00", "source": "hb-03"},
    {"q": "How much does a replacement student card cost?",
     "a": "12 GBP", "source": "hb-03"},
    {"q": "What is the international undergraduate tuition fee per year?",
     "a": "21,400 GBP", "source": "hb-05"},
    {"q": "When is the second tuition instalment due?",
     "a": "15 January", "source": "hb-05"},
    {"q": "How much does the Northfield Merit Scholarship pay per year?",
     "a": "3,000 GBP", "source": "hb-06"},
    {"q": "When do hardship bursary applications close?",
     "a": "31 October", "source": "hb-06"},
    {"q": "How much is the accommodation deposit?",
     "a": "400 GBP", "source": "hb-07"},
    {"q": "How many weeks is an undergraduate hall contract?",
     "a": "44 weeks", "source": "hb-07"},
    {"q": "How early must a student arrive before an examination?",
     "a": "15 minutes", "source": "hb-08"},
    {"q": "What percentage is needed for a first-class undergraduate mark?",
     "a": "70", "source": "hb-09"},
    {"q": "How many working days does coursework marking take?",
     "a": "15 working days", "source": "hb-09"},
    {"q": "How much is deducted per working day for late coursework?",
     "a": "10 percent of the available marks", "source": "hb-10"},
    {"q": "How long are self-certified extensions?",
     "a": "up to seven days", "source": "hb-10"},
    {"q": "Where are mitigating circumstances submitted?",
     "a": "the faculty office", "source": "hb-10"},
    {"q": "What happens to a student who pays someone to write an assignment?",
     "a": "normally exclusion from the programme", "source": "hb-11"},
    {"q": "What attendance rate must a student on a student visa maintain?",
     "a": "80 percent of scheduled contact hours", "source": "hb-12"},
    {"q": "What are the counselling service opening hours?",
     "a": "09:00 to 17:00 Monday to Friday", "source": "hb-13"},
    {"q": "How many hours may a student on a student visa work per week in term time?",
     "a": "20 hours", "source": "hb-15"},
    {"q": "How much is the annual student sports centre membership?",
     "a": "180 GBP", "source": "hb-16"},
    {"q": "How many members are needed to start a new society?",
     "a": "15", "source": "hb-16"},
    {"q": "What tuition fee is charged during a placement year?",
     "a": "1,850 GBP", "source": "hb-17"},
    {"q": "How many working days are allowed to submit a formal complaint?",
     "a": "20 working days", "source": "hb-18"},
    {"q": "How many guest tickets does each graduand receive?",
     "a": "two", "source": "hb-19"},
    {"q": "How much is a student parking permit?",
     "a": "120 GBP per year", "source": "hb-20"},
    {"q": "What is the printing credit per term?",
     "a": "5 GBP", "source": "hb-21"},
    {"q": "How long are examination scripts retained?",
     "a": "12 months", "source": "hb-23"},
    {"q": "How far in advance must religious festival adjustments be requested?",
     "a": "14 days", "source": "hb-24"},
]

HARD_QA = [
    {"q": "I am an international undergraduate in halls: what will tuition and "
          "accommodation cost me in total for a 44-week year?",
     "a": "21,400 GBP tuition plus 44 weeks of hall fees (128-176 GBP per week), so "
          "between 27,032 and 29,144 GBP",
     "sources": ["hb-05", "hb-07"]},
    {"q": "Which two services can I contact outside normal office hours?",
     "a": "The 24-hour study centre (library, with a student card) and campus security "
          "on extension 2222",
     "sources": ["hb-01", "hb-14"]},
    {"q": "What is the difference between a self-certified extension and mitigating "
          "circumstances?",
     "a": "A self-certified extension is up to seven days, once per year, for eligible "
          "modules; mitigating circumstances are evidence-based and go to the faculty "
          "office within five working days",
     "sources": ["hb-10"]},
]

# Questions the corpus cannot answer. A grounded system must refuse or say it does
# not know; an ungrounded one will produce a confident, wrong answer.
UNANSWERABLE = [
    "What is the deadline for the computer science dissertation?",
    "How many PhD scholarships does the chemistry department offer?",
    "What is the university's policy on emotional support animals?",
    "Which professor teaches the advanced robotics module?",
    "How much does a parking fine cost in the city centre?",
    "When was Northfield University founded?",
    "What is the acceptance rate for the medical school?",
    "How do I transfer to a different university?",
]

# ---------------------------------------------------------------------------
# 3. Sentiment set (used in LAB-11-03, project 5)
# ---------------------------------------------------------------------------
# Deliberately hard: negation, contrast, sarcasm, and neutral cases that a
# lexicon gets wrong. Labels: 1 positive, 0 negative.

SENTENCES = [
    ("The library was quiet and the staff were genuinely helpful.", 1),
    ("I waited forty minutes for a password reset and nobody apologised.", 0),
    ("Not a bad lecture, though the slides were dense.", 1),
    ("The food is not good.", 0),
    ("The food is not bad.", 1),
    ("I would not recommend this module to anyone.", 0),
    ("I would not say I disliked it.", 1),
    ("Great, another 9am lecture on a Monday.", 0),
    ("Absolutely brilliant, the projector failed again.", 0),
    ("The room was fine.", 1),
    ("The room was fine, I suppose.", 0),
    ("Wonderful support from the disability office, they solved it in a day.", 1),
    ("The exam was fair and matched the learning outcomes.", 1),
    ("The exam was impossible and nothing like the practice paper.", 0),
    ("The accommodation is expensive but the location is unbeatable.", 1),
    ("Cheap and cheerful, and it does the job.", 1),
    ("The seminar was cancelled twice with no explanation.", 0),
    ("Supervision was inconsistent, although my second supervisor was excellent.", 0),
    ("I learned more in this module than in any other this year.", 1),
    ("The marking was slow, but the feedback was detailed and useful.", 1),
    ("The timetable clashes every single week and nobody fixes it.", 0),
    ("The careers adviser gave me three concrete leads.", 1),
    ("There is no way anyone could enjoy this assessment.", 0),
    ("It is hard to imagine a better induction week.", 1),
    ("The lab equipment was broken for most of the term.", 0),
    ("The new study spaces are a real improvement.", 1),
    ("I expected to hate the group project and ended up enjoying it.", 1),
    ("The reading list was never updated and half the books are missing.", 0),
    ("The shuttle bus was late, as usual.", 0),
    ("The shuttle bus was unusually on time today.", 1),
    ("The lecture was long.", 1),
    ("The lecture was long and pointless.", 0),
    ("Support was responsive and clear.", 1),
    ("Support was responsive, eventually.", 0),
    ("No complaints at all about the labs.", 1),
    ("Not the worst canteen I have eaten in.", 1),
    ("The website is unusable on a phone.", 0),
    ("The website works now that they fixed the login page.", 1),
    ("Fees are high, but the teaching is worth it.", 1),
    ("Fees are high and the teaching does not justify them.", 0),
]


# ---------------------------------------------------------------------------
# 4. A minimal PDF writer (no external library, text is extractable)
# ---------------------------------------------------------------------------

def _pdf_escape(s: str) -> str:
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def make_pdf(path: Path, title: str, paragraphs, width: int = 88,
             lines_per_page: int = 46) -> Path:
    """Write a small, valid PDF with one standard font, paginated.

    The text stream uses the ``BT /F1 11 Tf ... (line) Tj ... ET`` operators, so
    any PDF text extractor (including ``pypdf``) returns the original words --
    which is what the PDF ingestion path in LAB-11-02 needs.
    """
    lines = [title, ""]
    for para in paragraphs:
        lines.extend(textwrap.wrap(para, width=width) or [""])
        lines.append("")

    pages = [lines[i:i + lines_per_page] for i in range(0, len(lines), lines_per_page)]
    objects: list[str] = []

    def add(body: str) -> int:
        objects.append(body)
        return len(objects)

    font_id = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids = []
    content_ids = []
    # Reserve: 1 catalog, 2 page tree -- filled in after the page objects exist.
    objects.insert(0, "")   # placeholder catalog
    objects.insert(1, "")   # placeholder pages tree

    for page_lines in pages:
        stream_parts = ["BT", "/F1 11 Tf", "14 TL", "56 780 Td"]
        for line in page_lines:
            stream_parts.append(f"({_pdf_escape(line)}) Tj T*")
        stream_parts.append("ET")
        stream = "\n".join(stream_parts)
        cid = add(f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream")
        content_ids.append(cid)
        pid = add(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {cid} 0 R >>"
        )
        page_ids.append(pid)

    objects[0] = f"<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{p} 0 R" for p in page_ids)
    objects[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>"

    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n{body}\nendobj\n".encode("latin-1")
    xref_at = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_at}\n%%EOF\n").encode("latin-1")
    path.write_bytes(bytes(out))
    return path


# ---------------------------------------------------------------------------
# 5. Writers
# ---------------------------------------------------------------------------

def write_corpus(out_dir: Path = CORPUS_DIR) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for doc_id, doc in HANDBOOK.items():
        (out_dir / f"{doc_id}.md").write_text(
            f"# {doc['title']}\n\n{doc['text']}\n", encoding="utf-8")

    (out_dir / "qa.json").write_text(
        json.dumps({"answerable": QA, "multi_document": HARD_QA,
                    "unanswerable": UNANSWERABLE}, indent=2), encoding="utf-8")
    (out_dir / "sentiment.json").write_text(
        json.dumps([{"text": t, "label": y} for t, y in SENTENCES], indent=2),
        encoding="utf-8")

    sections = [f"{d['title']}. {d['text']}" for d in HANDBOOK.values()]
    make_pdf(out_dir / "northfield-handbook.pdf",
             "Northfield University Student Handbook (fictional)", sections)


def main() -> None:
    write_corpus()
    words = sum(len(d["text"].split()) for d in HANDBOOK.values())
    chars = sum(len(d["text"]) for d in HANDBOOK.values())
    print(f"documents      : {len(HANDBOOK)}")
    print(f"words          : {words}")
    print(f"characters     : {chars}")
    print(f"mean words/doc : {words / len(HANDBOOK):.1f}")
    print(f"QA answerable  : {len(QA)}  multi-document: {len(HARD_QA)}  "
          f"unanswerable: {len(UNANSWERABLE)}")
    print(f"sentiment      : {len(SENTENCES)} "
          f"({sum(y for _, y in SENTENCES)} positive / "
          f"{len(SENTENCES) - sum(y for _, y in SENTENCES)} negative)")
    pdf = CORPUS_DIR / "northfield-handbook.pdf"
    print(f"pdf            : {pdf.name} {pdf.stat().st_size} bytes")

    try:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf))
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
        print(f"pdf pages      : {len(reader.pages)}  extracted chars: {len(text)}")
        print("extracted head :", " ".join(text.split())[:90])
    except ImportError:
        print("pypdf not installed: skipping extraction check")


if __name__ == "__main__":
    main()
