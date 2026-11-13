"""Visitor business logic. Views stay thin; this is where the rules live.

Two of these functions are load-bearing for the whole security model:

* ``badge_token`` derives the raw token for a visitor. It is deterministic, so
  the same QR can be reprinted and displayed for the life of the event, and it
  is an HMAC under a server secret, so it cannot be forged from the visitor id
  alone (CLAUDE.md constraint #3 — the QR is still opaque, just no longer
  irrecoverable).
* ``rotate_badge_token`` is the only thing that changes a badge's QR. Printing
  no longer does.
* ``deactivate_visitor`` stops a badge scanning without touching its scan
  history, and ``activate_visitor`` puts it back. The QR is unchanged by both:
  the token is derived, so the same printed card resumes working.
* ``purge_visitor`` is the only destructive path. It erases the registration for
  real, and it is not what ``DELETE /visitors/{id}`` does.
"""

import logging
import secrets

from django.db import transaction
from django.utils import timezone

from apps.common.utils import derive_token, hash_token

from .models import Visitor

audit = logging.getLogger("vms.audit")

# Crockford-ish: no 0/O/1/I, because staff read these serials aloud at a desk.
BADGE_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
BADGE_PREFIX = "VMS"
SERIAL_ATTEMPTS = 10


class BadgeSerialExhausted(RuntimeError):
    """Could not find a free badge serial. Effectively impossible at 250 guests."""


def log_visitor_action(actor, action: str, visitor: Visitor, **extra) -> None:
    """Record an admin write against a visitor, with actor and timestamp.

    The timestamp comes from the log formatter. Deliberately a log line and not a
    table: nothing in the app reads this back, it exists for the after-event
    security review.
    """
    who = getattr(actor, "username", None) or "anonymous"
    detail = " ".join(f"{k}={v}" for k, v in extra.items())
    audit.info(
        "visitor.%s actor=%s id=%s serial=%s%s",
        action,
        who,
        visitor.pk,
        visitor.badge_serial,
        f" {detail}" if detail else "",
    )


def generate_badge_serial() -> str:
    """Return an unused human-readable serial, e.g. ``VMS-K7P-3QM``."""
    for _ in range(SERIAL_ATTEMPTS):
        body = "".join(secrets.choice(BADGE_ALPHABET) for _ in range(6))
        serial = f"{BADGE_PREFIX}-{body[:3]}-{body[3:]}"
        if not Visitor.objects.filter(badge_serial=serial).exists():
            return serial
    raise BadgeSerialExhausted(
        f"No free badge serial after {SERIAL_ATTEMPTS} attempts."
    )


def badge_token(visitor: Visitor) -> str:
    """Return the raw token in this visitor's QR. Deterministic and repeatable.

    Safe to call as often as you like: the same visitor at the same
    ``token_version`` always yields the same string, which is what makes a card
    reprintable and lets the dashboard show a working QR at any time.

    ``visitor.id`` is a UUID assigned at instantiation, so this works before the
    row has been saved.
    """
    return derive_token(visitor.id, visitor.token_version)


def issue_badge_token(visitor: Visitor, *, save: bool = True) -> str:
    """Derive the badge token and make sure the stored digest matches it.

    NOT A MINT. This used to generate a fresh random token on every call, which
    is why printing in bulk silently reissued every badge on the sheet. It is now
    idempotent: existing cards keep working no matter how often it runs.

    Use ``rotate_badge_token`` when you actually want the old card to stop.
    """
    raw = badge_token(visitor)
    digest = hash_token(raw)
    if visitor.token_hash != digest:
        visitor.token_hash = digest
        if save:
            visitor.save(update_fields=["token_hash", "updated_at"])
    return raw


def rotate_badge_token(visitor: Visitor, *, actor=None) -> str:
    """Give ``visitor`` a new QR and stop the old one. Returns the RAW token.

    The deliberate counterpart to reprinting. Bumping ``token_version`` changes
    the HMAC input, so the previous card stops matching on the next scan while
    every other badge at the event is untouched.

    It does NOT set ``is_active = False``: that would kill the replacement card
    as well as the lost one.
    """
    visitor.token_version += 1
    raw = badge_token(visitor)
    visitor.token_hash = hash_token(raw)
    visitor.save(update_fields=["token_version", "token_hash", "updated_at"])

    log_visitor_action(actor, "badge_rotated", visitor, version=visitor.token_version)
    return raw


def register_visitor(validated_data: dict, *, actor=None) -> tuple[Visitor, str]:
    """Create a visitor with a serial and a badge token. Returns (visitor, raw token)."""
    visitor = Visitor(**validated_data)
    visitor.badge_serial = generate_badge_serial()
    raw_token = issue_badge_token(visitor, save=False)

    with transaction.atomic():
        visitor.save()

    log_visitor_action(
        actor, "create", visitor, category=visitor.category, source=visitor.source
    )
    return visitor, raw_token


def update_visitor(visitor: Visitor, validated_data: dict, *, actor=None) -> Visitor:
    """Apply an admin edit. The badge itself is untouched — serial and token stand."""
    for field, value in validated_data.items():
        setattr(visitor, field, value)
    visitor.save()

    log_visitor_action(
        actor, "update", visitor, fields=",".join(sorted(validated_data)) or "-"
    )
    return visitor


def deactivate_visitor(visitor: Visitor, *, actor=None) -> Visitor:
    """Stop a badge scanning. The next scan logs `revoked`, not a welcome.

    THE QR IS NOT TOUCHED, which is what makes this reversible. `classify()` in
    apps/scans reads `is_active` at scan time rather than anything baked into the
    code on the card, so the same printed badge starts working again the moment
    `activate_visitor` runs. Nothing has to be reprinted.

    The scan history stays either way: the point of deactivating a lost card is
    that you still want to see where it turns up afterwards.
    """
    if visitor.is_active:
        visitor.is_active = False
        visitor.save(update_fields=["is_active", "updated_at"])

    log_visitor_action(actor, "deactivate", visitor)
    return visitor


def activate_visitor(visitor: Visitor, *, actor=None) -> Visitor:
    """Put a deactivated visitor back on the door, with the card they already hold.

    The counterpart to `deactivate_visitor`, and the reason a wrong click at a
    busy desk is no longer permanent. A soft-deleted registration cannot reach
    here: the viewset's queryset filters `deleted_at__isnull=True`, so this only
    ever sees someone who is simply switched off.
    """
    if not visitor.is_active:
        visitor.is_active = True
        visitor.save(update_fields=["is_active", "updated_at"])

    log_visitor_action(actor, "activate", visitor)
    return visitor


def soft_delete_visitor(visitor: Visitor, *, actor=None) -> Visitor:
    """Remove a registration from the dashboard without dropping the row.

    ``ScanEvent.visitor`` is PROTECT, so a real DELETE would fail the moment the
    visitor has been scanned. The badge is revoked at the same time — a deleted
    registration must not still open the door.
    """
    if visitor.deleted_at is None:
        visitor.deleted_at = timezone.now()
        visitor.is_active = False
        visitor.save(update_fields=["deleted_at", "is_active", "updated_at"])

    log_visitor_action(actor, "delete", visitor)
    return visitor


@transaction.atomic
def purge_visitor(visitor: Visitor, *, actor=None) -> int:
    """Erase a registration for real. Returns the number of scans left orphaned.

    THIS IS NOT `soft_delete_visitor` AND THE TWO ARE NOT INTERCHANGEABLE. A soft
    delete hides a row that can be brought back by hand; this drops it, and the
    photograph with it. It exists for registrations that should never have been
    made -- a test entry, a duplicate, somebody typed in twice -- not for people
    who simply are not coming.

    `ScanEvent.visitor` is PROTECT, so the row cannot go while any scan points at
    it. The scans are detached rather than deleted: `visitor` is nullable exactly
    so a scan of an unrecognised badge still records that something was presented
    at that door at that minute. Deleting them instead would quietly reduce the
    entrance count and the security log, which is a worse outcome than an
    anonymous row. The caller is told how many were affected so the dashboard can
    say so before anybody confirms.

    The photo file is removed from storage too. Leaving it would keep a visitor's
    photograph on the server after their registration is gone, which is the one
    thing a purge is supposed to prevent.
    """
    from apps.scans.models import ScanEvent

    orphaned = ScanEvent.objects.filter(visitor=visitor).update(visitor=None)

    # Read before the row goes, for the audit line.
    log_visitor_action(actor, "purge", visitor, scans_orphaned=orphaned)

    if visitor.photo:
        # save=False: the row is about to be deleted, so there is nothing to save
        # the cleared field back to.
        visitor.photo.delete(save=False)

    # The assistant's saved chats quote names, so the name goes from there too.
    # Imported here: apps.assistant depends on visitors, not the reverse.
    from apps.assistant.services import redact_visitor

    redact_visitor(visitor.full_name)

    visitor.delete()
    return orphaned
