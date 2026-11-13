"""The retrieval half of the assistant: PostgreSQL in, plain dicts out.

Every function here is a read-only query, and every figure that touches the
entrance log goes through `reports.services.entry_log()` -> `summarise()` ->
`analysis.build()` — the same objects the PDF, the workbook and the reports page
draw from. So a number the assistant says and a number in the file it hands over
cannot disagree. Do not hand-roll a second aggregation here; CLAUDE.md records
what happened the last time one was verified through the wrong path.

WHAT LEAVES THE MACHINE. Whatever these functions return is sent to OpenAI as
context for the answer. They return names, countries, organisations, categories,
serials and times — what an admin needs to ask about — and NEVER a photo URL, a
badge token, a token hash or a database id. A badge token is a working
credential (CLAUDE.md constraint 3); an id is half of one. Adding a field here
is a decision about what an external service receives.

No LangChain in this file, on purpose: these can be exercised against a
throwaway database with no API key and no model.
"""

from __future__ import annotations

import datetime as dt

from django.db.models import Count, Exists, Min, OuterRef, Q, QuerySet
from django.db.models.functions import TruncDate
from django.utils import timezone

from apps.reports import analysis, services
from apps.scans.models import ScanEvent, ScanResult
from apps.visitors.models import Visitor

# Ceilings on what one tool call returns. A list longer than this is useless in
# a chat bubble and expensive as context; the totals are always exact, and the
# model is told when a list was cut so it can offer the Excel file instead.
MAX_ROWS = 40

REFUSED = (ScanResult.INVALID, ScanResult.REVOKED)


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------


def _local(stamp: dt.datetime | None) -> str | None:
    """A timestamp in the event's zone, minute precision — how a person reads it."""
    if stamp is None:
        return None
    return timezone.localtime(stamp, services.event_timezone()).strftime(
        "%Y-%m-%d %H:%M"
    )


def _live_visitors() -> QuerySet[Visitor]:
    """Everyone on the list. Soft-deleted rows are gone as far as anyone asks."""
    return Visitor.objects.filter(deleted_at__isnull=True)


def _has_arrived():
    """Subquery: this visitor has at least one VALID scan, ever."""
    return Exists(
        ScanEvent.objects.filter(visitor=OuterRef("pk"), result=ScanResult.VALID)
    )


def scan_days() -> list[dt.date]:
    """Local dates that saw at least one scan, oldest first."""
    rows = (
        ScanEvent.objects.order_by()  # Meta.ordering must not reach the GROUP BY
        .annotate(day=TruncDate("scanned_at", tzinfo=services.event_timezone()))
        .values_list("day", flat=True)
        .distinct()
    )
    return sorted(day for day in rows if day is not None)


def default_range(
    date_from: dt.date | None, date_to: dt.date | None
) -> tuple[dt.date, dt.date]:
    """Fill a missing end of a range: the whole scanned period, else today.

    A question with no dates in it ("how many arrived?") means the event, not
    today — and the event is over by the time most of these questions are asked.
    """
    days = scan_days()
    first = days[0] if days else services.today()
    last = days[-1] if days else services.today()

    start = date_from or (date_to if date_to and date_to < first else first)
    end = date_to or max(start, last)
    if end < start:
        start, end = end, start
    return start, end


def _visitor_row(visitor: Visitor) -> dict:
    """The one shape a visitor takes on its way to the model."""
    row = {
        "badge_serial": visitor.badge_serial,
        "full_name": visitor.full_name,
        "country": visitor.country,
        "organization": visitor.organization or "",
        "category": visitor.category,
        "source": visitor.source,
        "badge_active": visitor.is_active,
        "registered": _local(visitor.created_at),
    }
    if hasattr(visitor, "first_arrival"):
        row["first_arrival"] = _local(visitor.first_arrival)
        row["passes_through_door"] = visitor.passes
    return row


# --------------------------------------------------------------------------
# Retrievers — one per question shape
# --------------------------------------------------------------------------


def event_overview() -> dict:
    """Orientation: what dates exist, how big the list is, how it was built.

    Cheap, and the first thing the model should read for a vague question —
    it turns "day two" into a date and "Timor Leste" into the spelling stored.
    """
    visitors = _live_visitors()
    days = scan_days()

    by_source = {
        row["source"]: row["n"]
        for row in visitors.order_by().values("source").annotate(n=Count("id"))
    }
    countries = [
        {"country": row["country"], "registered": row["n"]}
        for row in visitors.order_by()
        .values("country")
        .annotate(n=Count("id"))
        .order_by("-n", "country")
    ]

    return {
        "timezone": str(services.event_timezone()),
        "today": services.today().isoformat(),
        "scan_days": [day.isoformat() for day in days],
        "registered_total": visitors.count(),
        "badges_active": visitors.filter(is_active=True).count(),
        "badges_deactivated": visitors.filter(is_active=False).count(),
        "vip_registered": visitors.filter(category="vip").count(),
        "registered_by_source": by_source,
        "arrived_at_least_once": visitors.filter(_has_arrived()).count(),
        "countries": countries[:MAX_ROWS],
        "country_count": len(countries),
    }


def entrance_report(
    *,
    date_from: dt.date | None = None,
    date_to: dt.date | None = None,
    country: str | None = None,
    category: str | None = None,
    result: str | None = None,
) -> dict:
    """The entrance report, exactly as the PDF and the workbook compute it."""
    date_from, date_to = default_range(date_from, date_to)
    queryset = services.entry_log(
        date_from=date_from,
        date_to=date_to,
        country=country,
        category=category,
        result=result,
    )
    summary = services.summarise(queryset)
    facts = analysis.build(queryset, summary)
    lines = analysis.narrative(summary, facts)

    window = facts["window"]
    peak = facts["peak"]
    admitted = facts["categories"]["vip"] + facts["categories"]["normal"]

    return {
        "filters": {
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat(),
            "country": country,
            "category": category,
            "result": result,
        },
        "scans_total": summary["total"],
        # Two different "arrived" figures, named apart so the model cannot mix
        # them. The report's own `arrived` is distinct people with ANY scan --
        # which includes somebody whose deactivated badge was refused at the
        # door. `people_admitted` is distinct people with a VALID scan, which is
        # what the overview and search_visitors call arrived.
        "people_admitted": admitted,
        "registered": facts["registered"],
        "admitted_rate_percent": analysis._percent(admitted, facts["registered"]),
        "people_scanned_incl_refused": facts["arrived"],
        "attendance_rate_percent_as_in_pdf": facts["attendance_rate"],
        "by_result": summary["by_result"],
        "refused": facts["refused"],
        "refusal_rate_percent": facts["refusal_rate"],
        "first_arrival": _local(window["first"]),
        "last_arrival": _local(window["last"]),
        "median_arrival": _local(window["median"]),
        "peak_hour": (
            {
                "hour": peak["hour"][:16].replace("T", " "),
                "scans": peak["total"],
                "share_percent": peak["share"],
            }
            if peak
            else None
        ),
        "by_hour": [
            {
                "hour": bucket["hour"][:16].replace("T", " "),
                "total": bucket["total"],
                "valid": bucket["valid"],
                "duplicate": bucket["duplicate"],
                "refused": bucket["refused"],
            }
            for bucket in summary["by_hour"]
        ][:72],
        "scans_by_country": summary["by_country"][:MAX_ROWS],
        "vip_arrived": facts["categories"]["vip"],
        "normal_arrived": facts["categories"]["normal"],
        "doors": facts["devices"],
        "people_scanned_more_than_once": facts["repeats"]["repeat_people"],
        "registered_not_arrived": facts["not_arrived_count"],
        "narrative": lines,
    }


def search_visitors(
    *,
    text: str | None = None,
    country: str | None = None,
    category: str | None = None,
    source: str | None = None,
    badge_active: bool | None = None,
    arrived: bool | None = None,
    limit: int = 25,
) -> dict:
    """Find people on the list, with whether and when they came through."""
    queryset = _live_visitors().annotate(
        first_arrival=Min("scan_events__scanned_at", filter=Q(scan_events__result=ScanResult.VALID)),
        passes=Count(
            "scan_events",
            filter=Q(scan_events__result__in=(ScanResult.VALID, ScanResult.DUPLICATE)),
        ),
    )

    if text:
        queryset = queryset.filter(
            Q(full_name__icontains=text)
            | Q(organization__icontains=text)
            | Q(badge_serial__iexact=text)
        )
    if country:
        queryset = queryset.filter(country__iexact=country)
    if category:
        queryset = queryset.filter(category=category)
    if source:
        queryset = queryset.filter(source=source)
    if badge_active is not None:
        queryset = queryset.filter(is_active=badge_active)
    if arrived is True:
        queryset = queryset.filter(first_arrival__isnull=False)
    elif arrived is False:
        queryset = queryset.filter(first_arrival__isnull=True)

    limit = max(1, min(limit, MAX_ROWS))
    total = queryset.count()
    rows = [_visitor_row(v) for v in queryset.order_by("full_name")[:limit]]

    return {
        "matching_total": total,
        "returned": len(rows),
        "truncated": total > len(rows),
        "visitors": rows,
    }


GROUPABLE = {
    "country": "country",
    "organization": "organization",
    "category": "category",
    "source": "source",
    "badge_active": "is_active",
}


def visitor_breakdown(*, group_by: str) -> dict:
    """Registered versus arrived, grouped by one field of the visitor."""
    field = GROUPABLE[group_by]
    rows = (
        _live_visitors()
        .annotate(has_arrived=_has_arrived())
        .order_by()
        .values(field)
        .annotate(
            registered=Count("id"),
            arrived=Count("id", filter=Q(has_arrived=True)),
        )
        .order_by("-registered", field)
    )

    groups = [
        {
            group_by: (row[field] if row[field] not in ("", None) else "(blank)"),
            "registered": row["registered"],
            "arrived": row["arrived"],
            "not_arrived": row["registered"] - row["arrived"],
        }
        for row in rows
    ]
    return {
        "group_by": group_by,
        "group_count": len(groups),
        "truncated": len(groups) > MAX_ROWS,
        "groups": groups[:MAX_ROWS],
    }


def not_arrived(
    *,
    date_from: dt.date | None = None,
    date_to: dt.date | None = None,
    country: str | None = None,
    category: str | None = None,
    limit: int = MAX_ROWS,
) -> dict:
    """Registered but no valid scan in the range — the no-show list."""
    date_from, date_to = default_range(date_from, date_to)
    absent = analysis.not_arrived(
        services.entry_log(date_from=date_from, date_to=date_to)
    )
    if country:
        absent = [v for v in absent if v.country.lower() == country.lower()]
    if category:
        absent = [v for v in absent if v.category == category]

    limit = max(1, min(limit, MAX_ROWS))
    return {
        "date_from": date_from.isoformat(),
        "date_to": date_to.isoformat(),
        "not_arrived_total": len(absent),
        "returned": min(limit, len(absent)),
        "truncated": len(absent) > limit,
        "visitors": [_visitor_row(v) for v in absent[:limit]],
    }


def scan_log(
    *,
    date_from: dt.date | None = None,
    date_to: dt.date | None = None,
    result: str | None = None,
    door: str | None = None,
    badge_serial: str | None = None,
    limit: int = 25,
) -> dict:
    """Individual scans, newest first: who, when, which door, what verdict."""
    date_from, date_to = default_range(date_from, date_to)
    # "refused" is not a stored outcome: it is revoked + invalid, which is what
    # anyone asking "who was turned away" means.
    queryset = services.entry_log(
        date_from=date_from,
        date_to=date_to,
        result=None if result == "refused" else result,
    )
    if result == "refused":
        queryset = queryset.filter(result__in=REFUSED)
    if door:
        queryset = queryset.filter(device__name__icontains=door)
    if badge_serial:
        queryset = queryset.filter(visitor__badge_serial__iexact=badge_serial)

    limit = max(1, min(limit, MAX_ROWS))
    total = queryset.count()
    rows = [
        {
            "time": _local(scan.scanned_at),
            "result": scan.result,
            "door": scan.device.name if scan.device_id else None,
            # An `invalid` scan matched no badge, so there is nobody to name.
            "visitor": scan.visitor.full_name if scan.visitor_id else None,
            "badge_serial": scan.visitor.badge_serial if scan.visitor_id else None,
            "country": scan.visitor.country if scan.visitor_id else None,
        }
        for scan in queryset[:limit]
    ]
    return {
        "date_from": date_from.isoformat(),
        "date_to": date_to.isoformat(),
        "matching_total": total,
        "returned": len(rows),
        "truncated": total > len(rows),
        "scans": rows,
    }
