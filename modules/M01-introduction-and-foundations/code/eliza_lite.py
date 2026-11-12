"""A small pattern-matching conversational system, plus transcript cue features.

Companion code for M01 (L01-01, LAB-01-02). Standard library only.

This is deliberately not a language model. It is a rule engine with pronoun
reflection, in the tradition of Weizenbaum's ELIZA (1966), and it exists to make
one point measurable: surface conversational fluency can be produced without any
understanding of the conversation.

Run directly for a scripted demonstration:

    python eliza_lite.py
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

REFLECTIONS = {
    "i": "you",
    "me": "you",
    "my": "your",
    "mine": "yours",
    "you": "I",
    "your": "my",
    "yours": "mine",
    "am": "are",
    "are": "am",
    "was": "were",
    "were": "was",
    "myself": "yourself",
}

# (pattern, responses). The first group, if present, is reflected into the reply.
RULES: list[tuple[str, list[str]]] = [
    (r"i need (.*)", ["Why do you need {0}?", "Would getting {0} change something for you?"]),
    (r"i feel (.*)", ["Tell me more about feeling {0}.", "How long have you felt {0}?"]),
    (r"i am (.*)", ["How long have you been {0}?", "Do you believe being {0} is temporary?"]),
    (r"my (.*) (?:is|was) (.*)", ["Why do you say your {0} is {1}?", "How does your {0} being {1} affect you?"]),
    (r"i want (.*)", ["What would it mean to you to have {0}?"]),
    (r"you are (.*)", ["Why do you think I am {0}?", "Does it matter to you that I am {0}?"]),
    (r"because (.*)", ["Is that the real reason?", "What other reasons come to mind?"]),
    (r"yes", ["You seem certain.", "I see. Tell me more."]),
    (r"no", ["Why not?", "What would change your mind?"]),
    (r"(.*)\?", ["Why do you ask that?", "What is your own answer to that?"]),
]

FALLBACKS = [
    "Please go on.",
    "What does that suggest to you?",
    "Can you say that in another way?",
    "How does that make you feel?",
]


def reflect(text: str) -> str:
    """Swap first- and second-person pronouns so a reply can address the user."""
    words = re.findall(r"[A-Za-z']+", text)
    return " ".join(REFLECTIONS.get(word.lower(), word) for word in words)


@dataclass
class ElizaLite:
    """Deterministic pattern-matching conversational system.

    Responses cycle through the available templates instead of being sampled, so
    two runs on the same transcript produce identical output. That determinism is
    what makes the lab's blind evaluation reproducible.
    """

    rules: list[tuple[str, list[str]]] = field(default_factory=lambda: list(RULES))
    fallbacks: list[str] = field(default_factory=lambda: list(FALLBACKS))
    turn: int = 0

    def respond(self, text: str) -> str:
        """Return the next reply for `text`."""
        cleaned = text.strip().lower()
        for pattern, responses in self.rules:
            match = re.fullmatch(pattern, cleaned)
            if match:
                template = responses[self.turn % len(responses)]
                groups = [reflect(group) for group in match.groups()]
                reply = template.format(*groups) if groups else template
                self.turn += 1
                return reply
        reply = self.fallbacks[self.turn % len(self.fallbacks)]
        self.turn += 1
        return reply


HUMAN_CUES = ("actually", "sorry", "i mean", "hmm", "not sure", "whatever")


def extract_cues(text: str) -> dict[str, float]:
    """Surface features a judge might (wrongly) use to spot a machine.

    Returns counts and ratios, all computed from the raw transcript turn.
    """
    words = re.findall(r"[A-Za-z']+", text)
    n_words = max(len(words), 1)
    return {
        "words": len(words),
        "question_marks": text.count("?"),
        "first_person": sum(word.lower() in {"i", "me", "my", "we"} for word in words) / n_words,
        "hedges": sum(cue in text.lower() for cue in HUMAN_CUES),
        "comma_ratio": text.count(",") / n_words,
        "mean_word_length": sum(len(word) for word in words) / n_words,
    }


def run_transcript(turns: list[str]) -> list[str]:
    """Return the system's replies to a list of user turns."""
    system = ElizaLite()
    return [system.respond(turn) for turn in turns]


if __name__ == "__main__":
    demo_turns = [
        "I need help with my timetable",
        "My supervisor is unhappy",
        "I feel stuck",
        "Are you a real person?",
        "Yes",
    ]
    for user, reply in zip(demo_turns, run_transcript(demo_turns)):
        print(f"user: {user}")
        print(f"sys : {reply}")
    print()
    for user, reply in zip(demo_turns, run_transcript(demo_turns)):
        cues = extract_cues(reply)
        print(f"{cues['words']:3d} words, {cues['question_marks']} questions: {reply}")
