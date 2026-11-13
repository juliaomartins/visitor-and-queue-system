"""How the assistant speaks: three specialist languages, every other one well.

English is the conference's working language; Portuguese and Tetun are
Timor-Leste's official languages. Those three get rules and a shared glossary,
so a figure is called the same thing in the chat as on the dashboard and in the
printed report. Any other language is answered in that language, competently,
with the same figures -- the glossary simply does not apply.

THE GLOSSARY'S SPELLINGS COME FROM THE DASHBOARD. Where a term exists in
`vms-dashboard/scripts/generate-locales.py`, it is copied from there -- the
same typographic apostrophe in "to’o", the same "kartaun" for a badge -- so an
admin reading Tetun on the reports page and in the chat sees one vocabulary.
Change a term in both places or neither.

Tetun is the language the model is weakest in (the event's key reaches
gpt-4o-mini only). The glossary and the rules are the part of that which code
can fix; a native read of real answers is the rest.
"""

from __future__ import annotations

SPECIALIST = ("en", "pt", "tet")

_NAMES = {"en": "English", "pt": "Portuguese", "tet": "Tetun"}

# (English, European Portuguese, Tetun Dili)
GLOSSARY: tuple[tuple[str, str, str], ...] = (
    ("visitor", "visitante", "vizitante"),
    ("registered", "inscrito", "rejistadu"),
    ("arrived", "chegou", "to’o"),
    ("arrival", "chegada", "xegada"),
    ("badge", "crachá", "kartaun"),
    ("scan", "leitura", "leitura"),
    ("refused at the door", "recusado à entrada", "rejeita iha odamatan"),
    ("door", "porta", "odamatan"),
    ("entrance report", "relatório de entradas", "relatóriu tama"),
    ("day", "dia", "loron"),
    ("hour", "hora", "oras"),
    ("people", "pessoas", "ema"),
    ("country", "país", "nasaun"),
    ("organisation", "organização", "organizasaun"),
    ("valid", "válido", "válidu"),
    ("duplicate", "duplicado", "duplikadu"),
    ("revoked", "revogado", "revogadu"),
    ("deactivated badge", "crachá desativado", "kartaun dezativadu"),
    ("self-registered", "autoinscrito", "rejista an rasik"),
    ("walk-in desk", "balcão de inscrição", "meza rejistu"),
    ("download", "descarregar", "deskarega"),
    ("Excel workbook", "livro Excel", "livru Excel"),
    ("PDF report", "relatório PDF", "relatóriu PDF"),
)


def language_guide(interface_locale: str) -> str:
    """The system prompt's language section."""
    interface = _NAMES.get(interface_locale, _NAMES["en"])
    glossary = "\n".join(f"{en} | {pt} | {tet}" for en, pt, tet in GLOSSARY)

    return f"""\
Language:
- Answer in the language of the user's latest message. If that message is too \
short to tell (a name, a number, "ok"), use the interface language. The \
interface language is {interface}.
- You are a specialist in three languages:
  - English, for the conference's working language.
  - European Portuguese, as written in Timor-Leste and Lisbon: "registo", \
"ecrã", "telemóvel", "descarregar", "o senhor/a senhora" or impersonal \
phrasing. Never Brazilian forms such as "você", "registro", "tela", "baixar".
  - Tetun Dili, in the INL orthography, with Portuguese loanwords spelled the \
Tetun way ("relatóriu", "rejistu", "xegada", "kartaun"). Write whole sentences \
in Tetun; never switch into Portuguese mid-answer. Count people as \
"ema na’in N" (for example "ema na’in 214 mak to’o").
- Any other language: answer in that language as well as you can, with exactly \
the same figures, names and dates. The glossary below does not apply.
- In every language write dates as dd/mm/yyyy and times on a 24-hour clock \
(02/10/2026, 08:05). Keep visitor names, organisation names and badge serials \
exactly as the tools return them; never translate them.
- Use these terms, so the chat matches the dashboard and the printed report \
(English | Portuguese | Tetun):
{glossary}
- Mention the download button only when you called offer_download in this \
turn; otherwise say nothing about downloading.
- How the two harder languages should read. The figures below are an \
illustration of style only; never quote them -- every figure comes from tools.
  Example answer in Tetun: {_EXAMPLE_TET}
  Example answer in Portuguese: {_EXAMPLE_PT}"""


# Worked answers, one per language the model handles least well. Measured, not
# guessed: with the glossary alone, gpt-4o-mini produced the right figures in a
# Tetun answer wrapped in nonsense ("Husu no to'o tan b leading bukit") and the
# Portuguese "registo" for "rejistu". One correct sentence to imitate does more
# than a rule it has to interpret.
#
# NEITHER EXAMPLE MENTIONS A DOWNLOAD BUTTON, and that is load-bearing: an
# earlier version ended "the button is below", and the model copied it into
# answers that offered no file -- an invented button beside no download.
_EXAMPLE_TET = (
    "Iha loron 02/10/2026, **ema na’in 188 mak to’o**, husi vizitante "
    "rejistadu 258. Oras ne’ebé ema barak liu mak to’o: 08:00. Kartaun 7 mak "
    "rejeita iha odamatan."
)
_EXAMPLE_PT = (
    "No dia 02/10/2026 chegaram **188 pessoas**, de 258 visitantes inscritos. "
    "A hora de maior movimento foi às 08:00. Foram recusados 7 crachás à "
    "entrada."
)
