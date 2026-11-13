"""Memory across conversations: short notes an admin asks the assistant to keep.

Two rules make this safe to have at all.

ONLY THE ADMIN'S OWN WORDS CAN CREATE A NOTE. The model sees visitor names,
and visitor names are typed by the public at /register. A note is injected
into every future conversation, so a memory any text could create would be a
*persistent* prompt injection: one crafted name, and the assistant carries
its instructions forever. Two layers stop that:

  1. The `remember` tool exists only on a turn whose user message asks to
     remember (`wants_memory`). This narrows the door but does NOT close it:
     in Tetun "hanoin" also means "think", so ordinary questions open it too.
  2. What closes it: a note must be built from the admin's own words
     (`grounded`) -- most of its words must appear in the message that asked.
     A tool result can suggest text; it cannot make the admin have typed it.

NO VISITOR IN A NOTE. Notes are for preferences and vocabulary ("answer in
Tetun", "Gate B is the side gate"), not facts about people: facts go stale and
are re-read from the database every time anyway, and a name in a note would
outlive a purge. Any note containing a registered visitor's full name --
deleted visitors included -- is refused.
"""

from __future__ import annotations

import re
import unicodedata

from apps.visitors.models import Visitor

from .models import MemoryNote

MAX_NOTES = 20
MAX_NOTE_CHARS = 200
# Share of a note's words that must appear in the admin's own message.
GROUNDING = 0.75

# Whole words, case-insensitive. Tetun: "hanoin" (remember/think of),
# "keta haluha" (don't forget). Portuguese: lembrar/lembre/lembra-te,
# memorizar. Deliberately not "note" or "save": both are ordinary in a
# question about badges and reports.
_TRIGGER = re.compile(
    r"\b(remember|memori[sz]e|don[’']?t\s+forget|lembr\w*|memoriz\w*|hanoin|keta\s+haluha)\b",
    re.IGNORECASE,
)

# Names this short match ordinary words ("Ana" in "banana"); they are not
# worth refusing a note over.
_MIN_NAME_CHARS = 4


class MemoryRefused(Exception):
    """A note that will not be kept. The message is for the model to relay."""


def wants_memory(text: str) -> bool:
    return bool(_TRIGGER.search(text or ""))


def notes_for(owner) -> list[MemoryNote]:
    return list(MemoryNote.objects.filter(owner=owner))


def _names_a_visitor(text: str) -> bool:
    lowered = text.lower()
    names = Visitor.objects.values_list("full_name", flat=True)
    return any(
        len(name.strip()) >= _MIN_NAME_CHARS and name.strip().lower() in lowered
        for name in names
    )


def _words(text: str) -> set[str]:
    """Lower-case words of three letters or more, accents and apostrophes
    folded, so "to’o", "to'o" and "too" compare equal."""
    folded = unicodedata.normalize("NFKD", text.lower())
    folded = "".join(ch for ch in folded if not unicodedata.combining(ch))
    folded = re.sub(r"[’'`]", "", folded)
    return {word for word in re.findall(r"\w+", folded) if len(word) >= 3}


def grounded(note: str, said: str) -> bool:
    """True when the note is, word for word, mostly what the admin wrote.

    THE TRIGGER WORD ALONE DOES NOT CLOSE THE INJECTION. In Tetun "hanoin"
    also means "think", so "Ita hanoin ema na’in hira…?" opens the gate on an
    ordinary question; once the tool exists, a visitor name in a tool result
    can steer what the model writes into a note. A note must therefore be
    built from the admin's own words: at least three quarters of its words
    appear in their message. Paraphrase in the same language passes ("Answer
    in Tetun" from "remember: answer in Tetun"); text the admin never wrote
    does not. The cost is that a note translated into another language than
    the admin wrote in is refused -- the tool description asks for their words.
    """
    note_words = _words(note)
    if not note_words:
        return False
    return len(note_words & _words(said)) / len(note_words) >= GROUNDING


def save_note(owner, text: str, *, said: str | None = None) -> MemoryNote:
    """Keep a note. `said` is the admin's message that asked for it; when it is
    given, the note must be grounded in it (see `grounded`)."""
    note = (text or "").strip()

    if not note:
        raise MemoryRefused("There was nothing to remember.")
    if len(note) > MAX_NOTE_CHARS:
        raise MemoryRefused(
            f"That is too long to remember; keep it under {MAX_NOTE_CHARS} characters."
        )

    if said is not None and not grounded(note, said):
        raise MemoryRefused(
            "I can only remember what you asked in your own words. Say it again "
            "as you would like it kept."
        )

    existing = MemoryNote.objects.filter(owner=owner, text__iexact=note).first()
    if existing:
        return existing

    if _names_a_visitor(note):
        raise MemoryRefused(
            "I do not keep notes about individual visitors. Ask me about them "
            "and I will look them up each time."
        )
    if MemoryNote.objects.filter(owner=owner).count() >= MAX_NOTES:
        raise MemoryRefused(
            f"I already remember {MAX_NOTES} things for you. Remove one in the "
            "assistant's history panel first."
        )

    return MemoryNote.objects.create(owner=owner, text=note)


def memory_section(notes: list[MemoryNote]) -> str:
    if not notes:
        return ""
    lines = "\n".join(f"- {note.text}" for note in notes)
    return (
        "This admin asked you to remember the following preferences. Follow "
        "them unless the current message says otherwise. They are preferences "
        "about how to answer, not data -- every figure still comes from tools:\n"
        f"{lines}"
    )
