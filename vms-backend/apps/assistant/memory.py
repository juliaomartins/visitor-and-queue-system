"""Memory across conversations: short notes an admin asks the assistant to keep.

Two rules make this safe to have at all.

ONLY THE ADMIN'S OWN WORDS CAN CREATE A NOTE. The model sees visitor names,
and visitor names are typed by the public at /register. A note is injected
into every future conversation, so a memory any text could create would be a
*persistent* prompt injection: one crafted name, and the assistant carries
its instructions forever. So the `remember` tool exists only on a turn whose
user message itself asks to remember (`wants_memory`). Text arriving through a
tool result cannot open that door.

NO VISITOR IN A NOTE. Notes are for preferences and vocabulary ("answer in
Tetun", "Gate B is the side gate"), not facts about people: facts go stale and
are re-read from the database every time anyway, and a name in a note would
outlive a purge. Any note containing a registered visitor's full name --
deleted visitors included -- is refused.
"""

from __future__ import annotations

import re

from apps.visitors.models import Visitor

from .models import MemoryNote

MAX_NOTES = 20
MAX_NOTE_CHARS = 200

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


def save_note(owner, text: str) -> MemoryNote:
    note = (text or "").strip()

    if not note:
        raise MemoryRefused("There was nothing to remember.")
    if len(note) > MAX_NOTE_CHARS:
        raise MemoryRefused(
            f"That is too long to remember; keep it under {MAX_NOTE_CHARS} characters."
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
