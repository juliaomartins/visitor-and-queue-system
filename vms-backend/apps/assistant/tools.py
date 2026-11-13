"""The LangChain tools: each one retrieves from PostgreSQL through `retrieval`.

This is the R in the RAG. The model never sees the database and never writes a
query; it picks a tool and fills in typed arguments, the tool reads PostgreSQL
through the same services the reports use, and the rows come back as context
for the answer. Pydantic validates every argument before it reaches the ORM, so
a hallucinated `category="VIP guests"` is rejected rather than silently
matching nothing.

Every tool is READ-ONLY. The model's context includes visitor names, and
visitor names are typed by the public at `/register`, so they are untrusted
text that can contain instructions. Nothing here can deactivate, edit or
delete anything — keep it that way, or put a human confirmation in front.

Tools are built per request (`build_tools`) so that the downloads one answer
offers are collected on that request's own `Session` and nowhere shared.
"""

from __future__ import annotations

import datetime as dt
import json
import threading
from dataclasses import dataclass, field
from functools import wraps
from typing import Literal

from django.db import connections
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from . import retrieval

Category = Literal["normal", "vip"]
Result = Literal["valid", "invalid", "revoked", "duplicate"]
Source = Literal["admin", "desk", "self"]

MAX_DOWNLOADS = 3


@dataclass
class Session:
    """What one chat turn accumulates besides the answer text."""

    downloads: list[dict] = field(default_factory=list)
    tools_used: list[str] = field(default_factory=list)
    origin_thread: int = field(default_factory=threading.get_ident)


def _encode(value) -> str:
    """Tool output is text to the model. Compact JSON, dates as ISO strings."""
    return json.dumps(value, ensure_ascii=False, default=str, separators=(",", ":"))


def _retriever(session: Session, name: str, fn):
    """Wrap a retrieval function as a tool body.

    Two jobs. It records which tools ran, for the audit line. And it closes the
    database connection when LangGraph ran the tool on one of its own worker
    threads: Django opens one connection per thread and only cleans up the
    request's own, so without this each parallel tool call would leave a
    Postgres connection open until the server restarts.
    """

    @wraps(fn)
    def run(**kwargs):
        session.tools_used.append(name)
        try:
            return _encode(fn(**kwargs))
        except Exception as error:  # the model gets a sentence, not a traceback
            return _encode({"error": f"{type(error).__name__}: {error}"})
        finally:
            if threading.get_ident() != session.origin_thread:
                connections.close_all()

    return run


# --------------------------------------------------------------------------
# Argument schemas — these become the JSON schema OpenAI sees
# --------------------------------------------------------------------------


class DateRange(BaseModel):
    date_from: dt.date | None = Field(
        None, description="First day, YYYY-MM-DD, inclusive. Omit for the whole event."
    )
    date_to: dt.date | None = Field(
        None, description="Last day, YYYY-MM-DD, inclusive. Omit for the whole event."
    )


class EntranceReportArgs(DateRange):
    country: str | None = Field(
        None, description="Exact country name as stored (see event_overview)."
    )
    category: Category | None = None
    result: Result | None = Field(
        None, description="Only scans with this outcome. Omit for all outcomes."
    )


class SearchVisitorsArgs(BaseModel):
    text: str | None = Field(
        None, description="Part of a name or organisation, or an exact badge serial."
    )
    country: str | None = None
    category: Category | None = None
    source: Source | None = Field(
        None,
        description="admin = registered by staff, desk = walk-in desk, self = self-registered.",
    )
    badge_active: bool | None = Field(
        None, description="false = deactivated badges only."
    )
    arrived: bool | None = Field(
        None, description="true = has a valid scan; false = never came through."
    )
    limit: int = Field(25, ge=1, le=retrieval.MAX_ROWS)


class BreakdownArgs(BaseModel):
    group_by: Literal["country", "organization", "category", "source", "badge_active"]


class NotArrivedArgs(DateRange):
    country: str | None = None
    category: Category | None = None
    limit: int = Field(retrieval.MAX_ROWS, ge=1, le=retrieval.MAX_ROWS)


class ScanLogArgs(DateRange):
    result: Result | Literal["refused"] | None = Field(
        None, description="refused = revoked + invalid together."
    )
    door: str | None = Field(None, description="Part of the scanner device's name.")
    badge_serial: str | None = None
    limit: int = Field(25, ge=1, le=retrieval.MAX_ROWS)


class DownloadArgs(DateRange):
    report: Literal["entrance_report", "visitor_list"] = Field(
        description=(
            "entrance_report = the entrance report (PDF, Excel or CSV), takes the "
            "date range and filters. visitor_list = every registered visitor with "
            "photo and QR, Excel only, no filters."
        )
    )
    format: Literal["pdf", "xlsx", "csv"]
    country: str | None = None
    category: Category | None = None
    result: Result | None = None


# --------------------------------------------------------------------------
# The download tool — offers a file, never builds one
# --------------------------------------------------------------------------


def _offer_download(session: Session):
    """The file itself comes from the existing export views, not from here.

    The tool only records which file, with which filters; the dashboard turns
    that into a button that calls `/reports/entries.{fmt}` or
    `/badges/roster.xlsx` with the admin's own token. So the assistant needs no
    file storage, the file is byte-for-byte the one the Reports page produces,
    and the badge tokens in the roster never pass through the model.
    """

    def offer(
        *,
        report: str,
        format: str,
        date_from: dt.date | None = None,
        date_to: dt.date | None = None,
        country: str | None = None,
        category: str | None = None,
        result: str | None = None,
    ) -> dict:
        if report == "visitor_list":
            if format != "xlsx":
                return {"error": "The visitor list exists only as Excel (xlsx)."}
            filters = {
                "date_from": None,
                "date_to": None,
                "country": None,
                "category": None,
                "result": None,
            }
        else:
            start, end = retrieval.default_range(date_from, date_to)
            filters = {
                "date_from": start.isoformat(),
                "date_to": end.isoformat(),
                "country": country,
                "category": category,
                "result": result,
            }

        offer = {"report": report, "format": format, "filters": filters}
        if offer in session.downloads:
            return {"status": "already offered", **offer}
        if len(session.downloads) >= MAX_DOWNLOADS:
            return {"error": f"At most {MAX_DOWNLOADS} files per answer."}

        session.downloads.append(offer)
        return {
            "status": "A download button for this file is shown under your answer.",
            **offer,
        }

    return offer


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------


def build_tools(session: Session) -> list[StructuredTool]:
    specs = [
        (
            "event_overview",
            "Orientation: today's date, the days that had scans, registration totals, "
            "and every country spelled exactly as stored. Call this first when the "
            "question names a day ('day two'), a country, or is vague.",
            None,
            retrieval.event_overview,
        ),
        (
            "entrance_report",
            "Arrival figures for a date range: scans, people arrived, attendance rate, "
            "refusals, peak hour, hourly flow, load per door, VIPs, no-show count and "
            "the report's written findings. Same numbers as the PDF/Excel report.",
            EntranceReportArgs,
            retrieval.entrance_report,
        ),
        (
            "search_visitors",
            "Find registered visitors by name, organisation, serial, country, category, "
            "registration source, badge state, or whether they arrived. Returns the "
            "exact matching total plus up to `limit` rows.",
            SearchVisitorsArgs,
            retrieval.search_visitors,
        ),
        (
            "visitor_breakdown",
            "Registered vs arrived counts grouped by country, organization, category, "
            "registration source, or badge state.",
            BreakdownArgs,
            retrieval.visitor_breakdown,
        ),
        (
            "not_arrived",
            "Registered visitors with no valid scan in the date range (no-shows).",
            NotArrivedArgs,
            retrieval.not_arrived,
        ),
        (
            "scan_log",
            "Individual scans, newest first: time, outcome, door, visitor. Use for "
            "'who was refused', 'what happened at door X', or one badge's history.",
            ScanLogArgs,
            retrieval.scan_log,
        ),
        (
            "offer_download",
            "Attach a downloadable file to your answer when the user asks for a PDF, "
            "Excel or CSV. Use the same filters you used for the figures.",
            DownloadArgs,
            _offer_download(session),
        ),
    ]

    return [
        StructuredTool.from_function(
            func=_retriever(session, name, fn),
            name=name,
            description=description,
            args_schema=schema,
        )
        for name, description, schema, fn in specs
    ]
