# VMS — Visitor Management System

Event badge system for ~250 visitors, running on a closed LAN behind one router.

**The event:** Díli Regional Cooperative Conference and Ministerial Dialogue 2026,
Díli, 2–3 October 2026. Two organisers (RDTL and SECoop) plus the event mark; all
three appear on the dashboard, the lobby screen and the scanner splash. That is why
the palette and the plume motif are sampled from the supplied logos rather than
chosen — see `lib/theme.ts` in the screen and `app/globals.css` in the dashboard.

**Flow:** admin registers visitor → prints ID card with QR → guard scans with phone →
lobby screen shows welcome with photo, name, country.

This is NOT an office visitor system. There are no appointments, no hosts, no approval
workflow, no check-out. Badges are printed in advance and stay valid for the event. A
scan is simply an arrival event. Visitors can also register themselves from a phone at
`/register` — with no approval step either; see **PUBLIC SELF-REGISTRATION**.

---

## Monorepo layout

```
vms/
├── CLAUDE.md               this file
├── .venv/                  shared Python venv (gitignored)
├── vms-backend/            Django + DRF + Channels + PostgreSQL
├── vms-dashboard/          Next.js — admin
├── vms-scanner/            React Native + Expo — guard
├── vms-screen/             Next.js — lobby display
├── vms-desktop/            PySide6 — the control centre that starts the rest
└── vms-contracts/          generated TypeScript types (OpenAPI → TS)
```

Frontends consume contracts by relative path:
`"@vms/contracts": "file:../vms-contracts"` — no submodule, no npm publishing.

### THE THREE FRONTENDS WERE THEIR OWN GIT REPOSITORIES, AND WERE MERGED IN

`vms-dashboard/`, `vms-screen/` and `vms-scanner/` each used to contain a `.git`
of their own. They were *not* submodules — no gitlink, no `.gitmodules` — so from
the root repository they looked like untracked directories and their contents
were invisible to it. A push from the root would have sent the backend, the
contracts and the desktop app and **none of the three frontends**, silently,
because as far as the root repo was concerned there was never anything there.

They are now one repository. Each was merged with `git read-tree --prefix=`
against a `-s ours` merge, which grafts the app's tree in at its folder while
leaving the working tree untouched — so `node_modules` survived and nothing had
to be reinstalled.

**All 623 commits are reachable from `HEAD` and every one of them is pushed.**
But be precise about what that gives you:

```bash
git log --oneline                      # 623 commits, frontends included
git show 2bc9385                       # a dashboard commit, intact
git log --oneline -- vms-dashboard/    # only 1 — the merge
```

The last line is not a bug and not fixable without rewriting history. Those
commits were made *inside* the dashboard repo, so their paths are
`app/(auth)/login/page.tsx`, not `vms-dashboard/app/(auth)/login/page.tsx`. Git
filters by path, and the old paths do not carry the prefix. The commits are all
there; only path-scoped log cannot associate them.

To read a frontend's own history, filter by the pre-merge path instead:

```bash
git log --oneline -- 'app/(auth)/login/page.tsx'
```

The three merge commits claim `git log -- vms-dashboard/` reads the real
history. **That claim is wrong** — it was written before the behaviour was
checked. This paragraph is the accurate one.

Backups of the three original repositories were taken as `git bundle` files
before the merge. They are not in this repo; if the pre-merge history is ever
needed as a standalone thing, that is where it is.

---

## Stack

| Part | Tech |
|---|---|
| Backend | Django, DRF, djangorestframework-simplejwt, **Django Channels**, PostgreSQL |
| Channel layer | `InMemoryChannelLayer` — **no Redis** |
| Background jobs | none — **no Celery** |
| Dashboard | TypeScript, Next.js 16 (App Router), Tailwind v4, TanStack Query, `qrcode`, `react-image-crop` |
| Scanner | TypeScript, React Native, Expo SDK 57, expo-router, expo-camera, expo-sqlite, reanimated, react-native-safe-area-context, `@expo/vector-icons` |
| Scanner on web | localStorage for the queue AND the token — pairs; the camera needs a secure context |
| Screen | TypeScript, Next.js 16, Tailwind v4, GSAP |
| Desktop | Python, **PySide6** (Qt 6), packaged with PyInstaller |
| Badge PDF | **ReportLab** + qrcode — pure Python, no native libraries |
| Spreadsheets | openpyxl — the roster and the credential export |
| Schema | drf-spectacular → openapi.yaml → openapi-typescript |
| Languages | English, Portuguese, Tetun — hand-rolled, generated dictionaries, no i18n library |
| Chat assistant | LangChain (`create_agent`) + langchain-openai, OpenAI `gpt-4o-mini` by default — **needs internet** |

Pinned versions live in `vms-backend/requirements.txt` and each frontend's
`package.json`. Django is 6.1 and Next is 16.3.2 at the time of writing; read the
files rather than trusting this line.

**Dashboard type is Plus Jakarta Sans (display), Inter (body) and JetBrains Mono.**
All three are self-hosted by `next/font`, which matters on a machine with no
internet. The printed card uses ReportLab's built-in Helvetica and Courier, so the
card is close to the preview but not identical — see the badge section.

---

## HARD CONSTRAINTS — do not "fix" these

**1. The backend runs as ONE process. Always.**

```bash
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers 1
```

`InMemoryChannelLayer` stores group membership in a Python dict inside the process. With
multiple workers, a scan handled by worker 2 never reaches a screen connected to worker 1
— and it fails *intermittently*, the worst kind of bug at a live event. Never add
`--workers N`. Never use gunicorn with multiple workers.

**2. No Docker. Postgres is installed natively. No Redis, no Celery, no containers.**

Deliberate for a 250-visitor LAN event on one machine. Postgres runs as a native
service on the server; there is no `docker-compose.yml` and there should not be one.
Do not introduce any of these without being asked.

**3. The QR contains an opaque DERIVED token — never a bare ID.**

```python
raw = hmac_sha256(BADGE_TOKEN_SECRET, f"{visitor.id}:{visitor.token_version}")
visitor.token_hash = sha256(raw.encode()).hexdigest()   # what the scan looks up
```

If the QR held the visitor id, anyone who saw a badge — or a dashboard URL, which
already contains that id — would hold a working credential forever. The HMAC keeps
the QR unguessable while making it **reproducible**, which is the point: the same
card can be reprinted and shown on screen for the life of the event.

This replaced a random `secrets.token_urlsafe(32)` that was stored only as a digest.
That was safe but irrecoverable, so a card could never be reprinted and printing a
second sheet silently revoked the first — indistinguishable, at the desk, from the
QR expiring.

`BADGE_TOKEN_SECRET` is now a crown jewel: leaking it makes every badge mintable,
and changing it invalidates every printed card at once. It is deliberately separate
from `SECRET_KEY` so that rotating Django's key does not void 250 badges.

**The QR is issued once, at registration, and nothing in the dashboard changes it.**

`rotate_badge_token()` is still the only function that can — it bumps
`token_version` — and `POST /api/v1/badges/reissue` still calls it. But no client
calls that endpoint any more: the wrapper was removed from `vms-dashboard/lib/badges.ts`
and the "Replace badge" button with it, because a control that silently re-mints a
credential does not belong next to one that prints it. Printing, exporting and
editing all leave the token alone.

A badge therefore stays valid from registration until the visitor is **deactivated**
or **deleted**, and both of those are reversible in the sense that matters: the token
is never touched, so activating a visitor puts the card already in their hand back to
work with nothing to reprint. `classify()` in `apps/scans/services.py` reads
`is_active` at scan time rather than anything baked into the code.

If you ever need rotation back in the UI, put it behind its own confirmation and say
plainly that every card already printed for that visitor stops scanning.

**4. The scanner app has no login — but the API is not open.**

Devices pair once with a 6-character code from the dashboard, then store a permanent
device token in `expo-secure-store`. After pairing, the app opens straight to the camera
forever. Do not add a login screen. Do not make `/scans` public.

**5. `group_send` goes inside `transaction.on_commit`.** Otherwise a rolled-back scan
still broadcasts, and the screen shows a visitor who isn't in the database.

**6. The screen uses BOTH WebSocket and polling.** See the real-time section. Do not
remove the polling endpoint "because we have WebSocket now".

**7. Apps live in an `apps/` package**, so every `apps.py` needs the full dotted path:
`name = "apps.visitors"`. Without it, `makemigrations` silently ignores the app.

**8. `vms-contracts/src/schema.d.ts` is generated. Never hand-edit it.** Regenerate from
the backend. Nothing hand-written goes in that package — no helpers, no formatters.

**9. LAN uses `http://`, not `https://`.** An HTTPS page cannot open a `ws://` socket —
browsers block it as mixed content, and certs for a LAN IP aren't worth the fight inside
a closed network.

---

## Real-time architecture (Django Channels)

The lobby screen uses **WebSocket for speed and polling for recovery**. Both. This is
intentional, not leftover from an earlier design.

```
Guard scans QR
  → POST /api/v1/scans                    (HTTP, device token)
  → validate token → write ScanEvent row
  → transaction.on_commit → group_send("lobby_screens", ...)
  → ScreenConsumer pushes JSON over WS
  → screen renders welcome card           (~200ms)

Screen reconnects after any drop or server restart
  → GET /api/v1/screen/feed?since=<last_id>
  → backfills missed events, dedupe by id
```

`InMemoryChannelLayer` has no queue behind it. Restart the server and every group
membership is gone, along with any scan during those seconds. The backfill is ~15 lines
and removes that entire failure class.

`ScanEvent.id` is a `BigAutoField` and serves as the monotonic `event_id`.

### Files that make up this layer

```
vms-backend/
├── config/
│   ├── settings/base.py         daphne first in INSTALLED_APPS, CHANNEL_LAYERS
│   └── asgi.py                  ProtocolTypeRouter: http + websocket
└── apps/
    ├── devices/middleware.py    DeviceAuthMiddleware (WebSocket auth)
    └── scans/
        ├── routing.py           ws/screen/
        ├── consumers.py         ScreenConsumer
        ├── services.py          log_valid_scan() → group_send
        └── views.py             ScanView, ScreenFeedView
```

### settings/base.py

```python
INSTALLED_APPS = [
    "daphne",                    # MUST be first, before staticfiles
    "channels",
    "django.contrib.admin",
    ...
    "rest_framework",
    "drf_spectacular",
    "apps.accounts", "apps.visitors", "apps.badges",
    "apps.devices", "apps.scans", "apps.reports",
]

ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
}
```

### config/asgi.py

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django_asgi_app = get_asgi_application()      # MUST run before any model import

from channels.routing import ProtocolTypeRouter, URLRouter
from apps.devices.middleware import DeviceAuthMiddleware
from apps.scans.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": DeviceAuthMiddleware(URLRouter(websocket_urlpatterns)),
})
```

Import order matters. `get_asgi_application()` before model imports, or you get
`AppRegistryNotReady`.

### apps/scans/routing.py

```python
from django.urls import path
from .consumers import ScreenConsumer

websocket_urlpatterns = [
    path("ws/screen/", ScreenConsumer.as_asgi()),
]
```

### apps/scans/consumers.py

```python
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ScreenConsumer(AsyncJsonWebsocketConsumer):
    group_name = "lobby_screens"

    async def connect(self):
        device = self.scope.get("device")
        if not device or device.kind != "screen":
            return await self.close(code=4401)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def visitor_arrived(self, event):        # "visitor.arrived" → visitor_arrived
        await self.send_json(event["payload"])
```

Dots in the `type` become underscores in the method name. A mismatch fails **silently** —
no error anywhere. This is the most common cause of "events aren't arriving".

### apps/devices/middleware.py

```python
from urllib.parse import parse_qs
from channels.db import database_sync_to_async

class DeviceAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        qs = parse_qs(scope.get("query_string", b"").decode())
        token = (qs.get("token") or [None])[0]
        scope["device"] = await self._get(token) if token else None
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def _get(self, token):
        from .models import Device
        return Device.objects.filter(
            token_hash=hash_token(token), is_active=True).first()
```

The browser `WebSocket` API cannot set headers, so the device token goes in the query
string. Keep it out of access logs.

### apps/scans/services.py — the publish

```python
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction

def log_valid_scan(visitor, device, scanned_at):
    scan = ScanEvent.objects.create(
        visitor=visitor, device=device, scanned_at=scanned_at, result="valid")

    payload = ScreenEventSerializer(scan).data
    transaction.on_commit(lambda: async_to_sync(get_channel_layer().group_send)(
        "lobby_screens",
        {"type": "visitor.arrived", "payload": payload},
    ))
    return scan
```

### vms-screen/hooks/useArrivalFeed.ts

```typescript
const connect = () => {
  const ws = new WebSocket(`${WS_URL}/ws/screen/?token=${token}`);

  ws.onopen = async () => {
    setConnected(true);
    const res = await fetch(`${API_URL}/api/v1/screen/feed?since=${lastId.current}`, {
      headers: { Authorization: `Device ${token}` },
    });
    if (res.ok) (await res.json()).events.forEach(add);   // backfill
  };

  ws.onmessage = (e) => add(JSON.parse(e.data));
  ws.onclose = () => { setConnected(false); setTimeout(connect, 2000); };
};
```

`add()` dedupes by `id`, so an event arriving on both paths is harmless.
Reconnect re-runs `onopen`, which re-runs the backfill automatically.

Send a ping every 30s — idle sockets get dropped, and mornings have quiet stretches
between arrival waves.

---

## Data model

```python
class Visitor(BaseModel):
    full_name     = CharField(max_length=200)
    country       = CharField(max_length=100)
    organization  = CharField(max_length=200, blank=True)
    photo         = ImageField(upload_to="visitors/")
    category      = CharField(choices=[("normal","Normal"), ("vip","VIP")])
    badge_serial  = CharField(max_length=20, unique=True)   # human-readable, printed
    token_hash    = CharField(max_length=64, unique=True, db_index=True)
    token_version = PositiveIntegerField(default=1)         # only rotation bumps it
    source        = CharField(choices=[("admin","Admin"), ("desk","Desk"), ("self","Self")])
    is_active     = BooleanField(default=True)              # deactivate / activate
    deleted_at    = DateTimeField(null=True, db_index=True) # soft delete

class ScanEvent(TimeStampedModel):
    id          = BigAutoField(primary_key=True)            # this is your event_id
    client_uuid = UUIDField(null=True, unique=True)         # the scanner's idempotency key
    visitor     = ForeignKey(Visitor, null=True, on_delete=PROTECT)
    device      = ForeignKey("devices.Device", on_delete=PROTECT)
    scanned_at  = DateTimeField(db_index=True)
    result      = CharField(choices=["valid","invalid","revoked","duplicate"])

class Device(BaseModel):
    name         = CharField(max_length=100)
    kind         = CharField(choices=[("scanner","Scanner"), ("screen","Screen")])
    token_hash   = CharField(max_length=64, unique=True, db_index=True)
    is_active    = BooleanField(default=True)
    last_seen_at = DateTimeField(null=True)

class PairingCode(BaseModel):
    code       = CharField(max_length=8, unique=True)
    kind       = CharField(choices=[("scanner","Scanner"), ("screen","Screen")])
    expires_at = DateTimeField()
    used_at    = DateTimeField(null=True)

class User(AbstractUser):    # admins only
    pass
```

`ScanEvent` logs invalid attempts too, with `visitor` null. One table gives you both the
entrance report and the security audit.

`client_uuid` is generated on the phone before the row leaves it, so the offline queue
can retry a scan without producing two arrivals when the first attempt actually landed
and only the response was lost.

**`visitor` is nullable for a second reason now.** A permanent delete detaches the
visitor's scans (`visitor = None`) rather than deleting them, so the entrance log keeps
its totals and timestamps while losing the identity. Deleting the rows instead would
quietly shrink the security log — see `purge_visitor` in `apps/visitors/services.py`.

Three states, and they are not the same thing:

| State | Set by | Badge scans? | On the visitor list? | Reversible |
|---|---|---|---|---|
| active | registration | yes | yes | — |
| deactivated | `POST /visitors/{id}/deactivate` | no, logs `revoked` | yes, marked | yes, `/activate` |
| soft-deleted | `DELETE /visitors/{id}` | no, logs `revoked` | no | by hand only |
| purged | `DELETE /visitors/{id}/permanent` | row is gone | no | **never** |

---

## API surface

```
POST   /api/v1/auth/token                    admin login           → JWT pair
POST   /api/v1/auth/token/refresh
POST   /api/v1/auth/token/blacklist

GET    /api/v1/health                        LAN address + liveness

GET    /api/v1/visitors                      list/filter/search    [admin]
       ?category= &is_active= &country= &source= &search= &ordering=
       ?with_tokens=true                     adds `badge_token` to every row
POST   /api/v1/visitors                      register              [admin]
GET    /api/v1/visitors/{id}                 detail + scans + token[admin]
PATCH  /api/v1/visitors/{id}                 edit                  [admin]
DELETE /api/v1/visitors/{id}                 soft delete           [admin]
POST   /api/v1/visitors/{id}/deactivate      badge stops scanning  [admin]
POST   /api/v1/visitors/{id}/activate        badge scans again     [admin]
DELETE /api/v1/visitors/{id}/permanent       erase for good        [admin]

POST   /api/v1/badges/card                   one card PDF, from a raw token
POST   /api/v1/badges/reissue-sheet          a run of cards, one per page. Non-destructive.
GET    /api/v1/badges/roster.xlsx            badge printing worklist
POST   /api/v1/badges/export                 worklist + photo + QR + payload
POST   /api/v1/badges/reissue                ROTATES TOKENS. No client calls it.

POST   /api/v1/devices/pairing-code          generate setup code   [admin]
GET    /api/v1/devices                       list paired devices   [admin]
POST   /api/v1/devices/{id}/revoke           kill a lost phone     [admin]
POST   /api/v1/devices/pair                  redeem setup code     [public, throttled]

POST   /api/v1/desk/registrations            walk-in registration  [desk device, throttled]
GET    /api/v1/desk/qr                       that badge's QR, PNG  [desk device, throttled]

POST   /api/v1/public/registrations          register yourself     [public, throttled, switch]
GET    /api/v1/public/registrations/status   is the form open?     [public, throttled]
GET    /api/v1/registration-settings         read the switch       [admin]
PATCH  /api/v1/registration-settings         open or close it      [admin]

POST   /api/v1/scans                         guard scans a badge   [scanner device]
GET    /api/v1/screen/feed?since={id}        reconnect backfill    [screen device]

WS     /ws/screen/?token=<device_token>      live push             [screen device]

GET    /api/v1/reports/entries?from=&to=     entrance log          [admin]
GET    /api/v1/reports/entries.csv           export                [admin]
GET    /api/v1/reports/entries.xlsx          export                [admin]
GET    /api/v1/reports/entries.pdf           export                [admin]

POST   /api/v1/assistant/chat                ask the data assistant [admin, throttled]
GET    /api/v1/assistant/status              is a key configured?  [admin]
GET    /api/v1/assistant/conversations       this admin's chats    [admin]
GET    /api/v1/assistant/conversations/{id}  one chat + messages   [admin, own only]
DELETE /api/v1/assistant/conversations/{id}  delete a chat         [admin, own only]
GET    /api/v1/assistant/memories            remembered notes      [admin]
DELETE /api/v1/assistant/memories/{id}       forget one            [admin, own only]
```

**Route names drifted from this document once already.** `POST /visitors/{id}/revoke`,
`GET /visitors/{id}/badge` and `POST /badges/bulk` were all documented here and none of
them existed. If you are unsure, ask the URLconf rather than this list:

```powershell
..\.venv\Scripts\python.exe manage.py spectacular --file openapi.yaml
```

and read the paths, or `curl http://<server>:8000/api/v1/schema/` against the running
process — which also tells you whether it has your latest code loaded.

**EXPORT FILENAMES COME FROM THE SERVER, NOT THE DASHBOARD.** `download()` in
`vms-dashboard/lib/badges.ts` reads `Content-Disposition` and uses its own
string only as a fallback, so renaming a file means editing
`_export_name` / `_visitor_slug` in `apps/badges/views.py`. Editing the
dashboard alone changes nothing — that is worth knowing before spending an
afternoon on it.

| from | filename |
|---|---|
| `/visitors` export | `visitors-2026-10-02.xlsx` |
| `/badges` export, nothing selected | `visitors-badges-2026-10-02.xlsx` |
| `/badges` export, one selected | `visitors-badges-2026-10-02-ana-maria-sousa.xlsx` |
| `/badges` export, twelve selected | `visitors-badges-2026-10-02-12-visitors.xlsx` |

Three decisions inside that, each of which has a wrong answer that looks fine:

- **`timezone.localdate()`, never `date.today()`.** Storage is UTC and the doors
  are in Asia/Dili, so for the first nine hours of every local day they
  disagree — an export at 09:00 on the 2nd would be filed as the 1st.
- **ISO order**, so a downloads folder sorted by name is sorted by date.
  `apps/reports` already named its files this way.
- **The suffix keys off whether `visitor_ids` was sent, not off the count.** It
  describes a deliberate selection: exporting everyone by selecting nobody gets
  no suffix; selecting all of them explicitly gets `250-visitors`. A single
  visitor gets their name, several get a count — a filename cannot carry forty
  names, and electing one to stand for the rest reads as though the file were
  about that person. The name is `slugify`d because the header is the plain
  `filename="..."` form with no RFC 5987 `filename*`, so a raw accent makes it
  malformed; and a name in a non-Latin script folds to nothing, so the badge
  serial stands in.

The reports exports (`vms-entrance-report-{date}.xlsx`) and the badge PDFs
(`badge-{serial}.pdf`) still carry the older names and are inconsistent with
these.

**`visitor_ids` on `POST /badges/export` is capped at 250 elements**
(`max_length=250`, `apps/badges/serializers.py`), and the event expects about
250 visitors. Select-all-then-export therefore fails with a 400 —
*"Ensure this field has no more than 250 elements"* — the moment there are 251
registrations. Measured, not guessed. Nothing in the dashboard anticipates that
error, so raise the cap or chunk the request before the event rather than
finding it at the desk.

`/scans` returns `200` with a `result` field for bad badges, not `4xx`. A deactivated
badge is a business outcome, not an HTTP error — it keeps the app's error handling clean.
The `result` value is still `revoked`; the enum is what the scanner and the reports are
built on, and renaming it would be a schema change for a word.

**`with_tokens` is opt-in and every other list call goes without it.** A badge token is
a working credential, so the flag turns one request into a set of usable badges. The
print queue asks for it because it draws the real QR on every card and a frame saying
"on the printed card" verifies nothing. The `.xlsx` export already hands the same admin
the same codes, so the boundary it crosses is convenience, not secrecy — but do not
sprinkle it onto other callers for tidiness.

**`roster.xlsx` now crosses that same boundary, and it used to be the one export
that did not.** It is laid out as the printing worklist the organisers already
circulate: the shared report header over rows 1-3 (see **EVERY EXCEL AND PDF
REPORT CARRIES ONE HEADER** below), titled `VISITOR LIST AND QR CODE PRINTING
LIST`, column headings on row 4, data from row 5, frozen at `A5`. Columns are `No. | Name | Country | Organization | Photo | QR Code |
Registered` — so the file is a set of working badges — one click
from `/visitors`, with no confirmation in front of it. Two things make that
defensible and it is worth knowing which: the QR is `badge_token(visitor)`, the
code **already** on that person's card, so exporting reissues nothing and breaks
nothing; and the admin who can click it can already read every token from
`?with_tokens=true`. What changed is convenience, again — but a spreadsheet gets
forwarded in a way a query string does not. If that ever needs tightening, the
confirmation dialog in front of `POST /badges/export` is the shape to copy.

`Category` and `Badge state` were dropped from that sheet to make room. A
deactivated visitor is therefore shown with a QR that will not scan, and the only
cue is that their name is set grey and italic — `DIM_FONT` in `exports.py`. If
somebody asks why a badge in the spreadsheet was refused at the door, that is
the answer.

Two things about that sheet that will bite whoever edits it next:

- **Style the merged banner's ANCHOR cell only.** `Worksheet._clean_merge_range`
  replaces every cell but the top-left with a fresh `MergedCell` and its
  `format()` restores *borders* and nothing else — because Excel draws a merged
  range from the top-left cell's fill, font and alignment, but does not carry its
  border around the outside. A fill written to the other six is discarded on
  merge whichever order you write it in, so painting them is wasted work, and a
  test that asserts G1 is navy is asserting the wrong thing.
- **Image anchors are looked up by heading, not written as letters**
  (`_roster_column`). Photo and QR moved three columns right when this layout
  was reshaped and nothing else had to change; a literal anchor would have put
  every image in the wrong cell, silently, in a file nobody opens until the
  morning they print from it.

**BOTH exports share that banner now**, and the paragraph here said the
opposite for one session: `build_credential_workbook` was asked to match, so
`_write_header` and its two graphite constants are gone and `_write_banner` has
two callers. `POST /badges/export` carries the wider table — `No. | Name |
Country | Organization | Category | Badge Serial | Photo | QR Code | Registered
| QR payload` — because it is the card producer's sheet: the serial is printed
on the card, the category decides the amber VIP ring, and the payload is the
exact string the QR encodes so it can be re-rendered at another size.

**EVERY EXCEL AND PDF REPORT CARRIES ONE HEADER**, written by
`apps/common/report_header.py` and nowhere else: the event logo in a white cell of
its own at the left, a navy bar with the report's title, then `DRCC AND
MINISTERIAL DIALOGUE 2026` and `2–3 OCTOBER 2026 · DÍLI, TIMOR-LESTE`. Only the
title belongs to the caller:

| file | title |
|---|---|
| `GET /badges/roster.xlsx` (`/visitors` Export Excel) | VISITOR LIST AND QR CODE PRINTING LIST |
| `POST /badges/export` (`/badges` Export Excel), every tab | VISITOR BADGE & QR CODE PRINTING LIST |
| `GET /reports/entries.xlsx`, all six tabs | ENTRANCE REPORT |
| `GET /reports/entries.pdf`, every page | ENTRANCE REPORT |

**CSV and the badge PDFs have no header, on purpose.** A CSV is read by other
programs and banner rows break them; the card pages ARE the badges.

Four things about it that are not obvious:

- **The logo sits on white, never on the navy bar.** It is a full-colour emblem
  with a blue plume and a black ribbon, and both vanish on `#00309C`.
- **`apps/common/brand/logo.png` is a copy** of `vms-dashboard/public/brand/logo.png`,
  trimmed of its transparent border and scaled to 320 px — duplicated for the
  same reason as the badge artwork. Replace both together.
- **Write a sheet's column widths BEFORE the header.** The header centres the logo
  in column A's final width (widening it to 14 if narrower — which is why "No." is
  wider than it was) and sizes the banner from the widths it can see.
- **The banner runs past a narrow table.** A merged cell clips its text rather than
  overflowing, so a three-column tab would cut the date line off;
  `_banner_last_column` keeps spanning until the text fits. And every table tab's
  data starts at row 5, so the hourly chart reads its series names from row 4 —
  reading from row 1 would title the series with the event name.

**`POST /badges/export` IS NOT DESTRUCTIVE, and three separate places said it
was.** `collect_badge_tokens` recomputes the derived token and
`issue_badge_token` is idempotent — its own docstring says "NOT A MINT" — so
exporting retires nothing and exporting twice produces an identical file. The
stale claim had reached:

| where | said |
|---|---|
| `BadgeCredentialExportView` docstring | "by reissuing every one" |
| its `@extend_schema` description, **so `openapi.yaml` too** | "DESTRUCTIVE… invalidates the QR on any card already printed" |
| the workbook's own "Read me" tab | *"collect and destroy the old cards"* |
| the dashboard's export dialog | "Nothing is changed by exporting" — the only correct one |

The tab is the one that mattered: it instructed whoever opened the file to
destroy 250 working badges, on the strength of a sentence nobody revisited after
tokens became derived. All four now agree, and the tab keeps the warning that IS
true — anyone holding the file can produce a badge that scans.

Only `/devices/pair` and the two `/public/registrations` routes are reachable without a
token — see **PUBLIC SELF-REGISTRATION**. The two `/desk/*` routes take no login
either, but they are not open: each requires a paired **desk** device token, the same
kind of credential a scanner or a screen carries — see **THE WALK-IN DESK**.

---

## Security

- Access token in memory only. Refresh token in an httpOnly cookie. **Never localStorage**
  — this app holds every visitor's photo and passport-adjacent data.
- simplejwt: 15-minute access, rotating refresh, blacklist after rotation.
- Rate limit `/api/v1/scans` to 30/min per device. A real guard does ~10.
- Rate limit `/api/v1/devices/pair` to **20/hour per IP, counting FAILED attempts
  only** — a success clears the count. Not 5, and not all attempts: every device at
  the event shares the router's address, so that budget is shared. See the comment
  beside `DEFAULT_THROTTLE_RATES` in `settings/base.py`, which is the authority.
- Visitor photos via signed, expiring URLs — not a public `/media/` directory.
- Screen device tokens are read-only, scoped to one endpoint and one WS path. Assume
  extraction; the screen is physically accessible.
- Log every admin CRUD action on `Visitor` with actor and timestamp.
- Suppress a repeat of the same visitor within 60s on the screen, but still log it as
  `duplicate`.

---

## Backend structure

```
vms-backend/
├── config/
│   ├── urls.py
│   ├── asgi.py                 THE entry point
│   ├── wsgi.py                 kept for manage.py only
│   └── settings/{base,dev}.py  NO prod.py, NO test.py — see Tests
└── apps/
    ├── common/     BaseModel, permissions, throttling, hash_token(), storage
    ├── accounts/   User + simplejwt views. Admins only.
    ├── visitors/   Visitor CRUD, issue_badge_token(), activate/deactivate, purge
    ├── badges/     ReportLab PDF. NO MODELS, no templates — it draws.
    ├── devices/    Device, PairingCode, authentication.py (HTTP), middleware.py (WS)
    ├── scans/      ScanEvent, consumers.py, routing.py, services.py, views.py
    ├── desk/       The walk-in desk. TWO routes, no login, paired device token.
    ├── reports/    Aggregation + CSV export. NO MODELS.
    └── assistant/  The chat assistant: LangChain + OpenAI over `reports`.
                    Models: Conversation, ChatMessage, MemoryNote — per admin.
```

`badges/` and `reports/` have no models on purpose — they read from `visitors` and
`scans`. This stops `visitors/views.py` absorbing every feature.

Business logic lives in `services.py`. Views stay thin.

**Badges are drawn with ReportLab, not rendered from HTML.**

WeasyPrint was the original choice and could not run: it reaches Pango and Cairo
through GTK, native libraries that are not installable with pip and are absent on
the Windows server this event runs on. The result was a badge feature that
returned 503 on the only machine that mattered. ReportLab is pure Python and
renders identically everywhere, so `apps/badges/services.py` holds explicit
millimetre geometry instead of CSS. Do not reintroduce an HTML renderer without
first checking it runs on the server, not just on a developer's machine.

Fonts are ReportLab's built-in Helvetica — vector, always present, no font file
to ship. See **THE PRINTED CARD IS THE ORGANISERS' PRODUCTION FILE** below for
what that costs and how the sizes were chosen.

**THE PRINTED CARD IS THE ORGANISERS' PRODUCTION FILE, MEASURED OFF IT.**

`ID CARD PVC SECOOP.pdf` is the file the organisers had 80 PVC cards made from:
**80 pages, one card per page, 95 × 130 mm**, no A4 sheet and no cut marks. Every
number in `apps/badges/services.py` was read out of that file's *content stream*
— the hem is its cubic bezier, the bands are its rectangles, the navy is its
CMYK — rather than eyeballed off a screenshot.

**IT IS NOT IN THIS REPOSITORY, AND `ID CARD*.pdf` IS GITIGNORED SO IT CANNOT
WANDER IN.** It is 55MB, and every page carries a real visitor's name, country
and photograph — the passport-adjacent data this system is careful with
everywhere else. Committing it would put 80 people into the history permanently.
Ask the organisers for it if you need to re-measure; the numbers it yielded are
all recorded here and in `services.py`.
Rendered against it at 300 dpi, every measured element (hem at eight columns,
mark, both title lines, both theme lines, photo, name, country, QR, role band,
address line) is **within 0.5 percentage points of the card**, which is 0.48 mm
across and 0.65 mm down. The hem matches exactly at all eight columns.

Top to bottom: the navy field with its curved hem, the event mark top-left, the
conference name and theme beside it, a 30 × 40 mm rounded photograph with a
black keyline, the name underlined over the country in the right-hand column, a
27.5 mm QR under them, a red role band, the address on navy, and the woven tais.

**Two things are deliberately NOT identical to that file:**

- **The typefaces.** The artwork is Araboto and Open Sans; neither ships with
  ReportLab nor installs with pip, and shipping a font file is the exact
  dependency that cost this app WeasyPrint. So it is Helvetica — and the point
  sizes in `services.py` are **not** the artwork's. They are the sizes at which
  Helvetica sets each fixed string to the artwork's measured **width**. Matching
  width rather than height is the choice: this layout is width-constrained
  where it matters, so a block 6% wider overflows while one 6% shorter merely
  looks a shade lighter. The ratios came out 0.92–1.05 of the artwork's sizes.
- **The event mark.** The artwork's copy is stretched about 3.5% wide of the
  emblem's true proportion. Ours is fitted into the same box undistorted and
  centred. Reproducing a client's logo at the wrong proportion is not fidelity.

**`MARK_ALPHA_FLOOR` is 8 and not 0, and that is worth 8% of the mark's width.**
`drcc-event.png` carries 32 px of all-but-invisible fringe down its right edge —
alpha above 0 but below 9 — so `getbbox()` on the raw channel returns 411 × 401
where the visible emblem is 377 × 396. Trim to the raw box and the mark is
scaled to fit a third of an inch of nothing, rendering visibly small with no
clue why.

**`assets/tais-strip.png` is cut from that same PDF at 600 dpi**, 2244 × 190 px
= exactly 95 × 8.043 mm, so it is drawn 1:1 and never resampled. It is a
photograph because the artwork's is: the band is built in the source from 109
placed raster tiles, and a drawn approximation of a real textile reads as a
pattern rather than as cloth. **The tais stops 4.574 mm above the trim with navy
below it** — running it to the bottom edge is the single most visible way to get
this card wrong, and `components/badge-card.tsx` still does exactly that.

**The QR carries the event mark in its middle, and the error-correction level did
NOT change to make room for it.** The level is still `ERROR_CORRECT_M` and the
grid is still 39 modules. **The module is now 0.705 mm, up from 0.359**, because
the artwork's code is 27.5 mm where the CR80 card's was 14 — the one part of the
card change that makes the badge easier to scan rather than merely correct.

The folklore is that a centre logo needs Q or H. On this payload it needs
neither, because the level alone decides the grid: the badge token is a fixed 64
lowercase hex characters, taken in byte mode, so M gives 39 modules, Q gives 43
and H gives 47 — and the artwork fixes the code's size, so the grid is the only
free variable. A bigger grid therefore buys redundancy *with module size*, and
module size is what a phone at a doorway is short of. Measured over 250 distinct tokens
rasterised at 300 dpi and degraded, at the capture size where scanning begins to
fail:

| config | decoded |
|---|---|
| M, no logo — the card before | 250/250 |
| M, this logo — the card now | 250/250 |
| **Q, no logo at all** | **180/250** |
| Q, this logo | 138/250 |

The level would have cost most of the margin; the mark costs none of it. The
arithmetic is that `QR_LOGO_FRACTION = 0.18` with its pad covers about 4.5% of
the code's area, well inside what M already rebuilds. **Do not "harden" this to
Q or H** — that makes the badge worse, and the comment beside
`QR_ERROR_CORRECTION` in `services.py` is the authority.

That measurement was made at 14 mm, on the CR80 card. Every margin in it got
wider when the code grew to 27.5 mm; the arithmetic is unchanged because the
grid did not move. Decoded off the 300 dpi render of the new card, the QR reads
back byte-identical down to a **71 px** crop.

What the mark does cost is one step at the very bottom of the range: rasterised
from the old card PDF, the bare code decoded down to a 57 px QR and the marked
one down to 62 px, so the card had to fill about 240 px of the camera frame
instead of 220. Above that they are identical. There is also one stacked
condition — heavy blur *and* low contrast *and* a steep angle together — where
50/250 became 1/250; that regime already fails 80% of the time with no logo, and
no mark size recovers it.

**And the mark changes nothing about the credential.** It is composited over the
finished code, never encoded into it, so the string a scanner reads is
byte-identical. No printed badge was invalidated, `token_version` was not
touched, and **nothing had to be migrated**: no QR is stored anywhere in this
system, so all 250 visitors picked the mark up the next time their card was
drawn. At this size the wordmark ring is not legible and is not meant to be —
what survives is the silhouette.

The artwork is duplicated at `apps/badges/assets/drcc-event.png` rather than read
from `vms-dashboard/public/brand/`, because a backend-only deploy does not check
that folder out. `lib/badge-geometry.ts` mirrors the level and the fraction so
the preview and the print cannot drift.

**BULK PRINT IS ONE CARD PER PAGE NOW. THERE IS NO A4 SHEET AND NO CUT MARKS.**
It used to be nine to an A4 sheet, 3 across by 3 down, with cut marks in the
margins. That went when the card became 95 × 130: three of them across is 285 mm
on a 210 mm page, and more to the point these cards are not cut out of paper —
they come off a card printer, which is why the organisers' own file is 80
separate pages. `render_a4_sheet_pdf` is therefore `render_card_set_pdf`, and a
run of one is no longer a special case, just a one-page document.

`apps/badges/services.py` holds the geometry as millimetre constants and
`components/badge-card.tsx` mirrors it as percentages. **They agree on the
design now — both are the organisers' ID card — but they were measured from
different sources and three numbers still differ.** The component was measured
off `ID CARD OFFICIAL.jpg`, a flattened export; `services.py` was read out of
the production PDF's vectors, which is the better source. The component's card
ratio is 748 : 1024 = 0.7305 against the card's true 95 : 130 = 0.7308, which is
nothing, but these three are visible:

| | `badge-card.tsx` | the card, measured |
|---|---|---|
| hem goes flat at | 30.6% of the width | **40.0%** |
| hem curve | quadratic, control point at half span | **cubic**, two control points |
| tais band | runs to the bottom edge | **stops at 96.45%**, navy below |

Fixing them is three constants and an SVG path — the cubic is
`M0 0 H100 V29.73 H40.0 C16.9 30.72 10.3 26.12 0 21.38 Z` reversed into the
preview's coordinate space — and it has not been done, so the preview's foot and
hem are still a little wrong against what prints.

Two details of the rebuild worth keeping, both measured rather than guessed:

- **The hem is drawn in a `preserveAspectRatio="none"` box, and that is right
  here** even though it is the opposite of the rule the charts follow: there is
  no stroke or radius to distort, and the curve is defined in percentages of the
  card, so stretching the box IS the reproduction. (The curve the component
  draws is a parabola fitted to points read off the flattened JPEG. The real one
  is the cubic in the table above — **this bullet used to claim the parabola was
  the curve**, which it never was; it was the best fit available from a raster.)
- **The artwork mixes two type widths, and which line gets which is measurable.**
  Long lines are condensed and short ones are not: the name is 24 characters in
  421px (0.43em each, which is Arial Narrow) while the role band is 18 in 478px
  (0.60em, which is Arial). The exact faces are not identified — Arial Narrow
  matches the metrics to within 3px of every measured line, and that is the claim.

---

## Dashboard (vms-dashboard)

Login, visitor CRUD (normal + VIP), photo upload with crop, badge print queue, device
pairing codes, entrance reports, and an overview page.

```
app/(auth)/login
app/(dashboard)/dashboard          overview: arrivals curve, outcome split, recent
app/(dashboard)/visitors           list — right-click a row for actions
app/(dashboard)/visitors/new       register + badge receipt
app/(dashboard)/visitors/[id]      detail: live QR, scan history, lifecycle buttons
app/(dashboard)/visitors/[id]/edit
app/(dashboard)/badges             print queue, one card per page, real QR on every card
app/(dashboard)/devices            pairing codes + paired device list
app/(dashboard)/reports            entrance log + CSV/XLSX/PDF export
app/(dashboard)/settings           server address + clock check, registration switch, theme, language
app/(public)/register              public self-registration form — no session, always light
app/(public)/desk/[key]            walk-in desk — no login, paired device token, unguessable path
```

**`/settings` is deliberately three panels and no more** — the third, the public
registration switch, is event-wide state with a database row behind it, which is what the
"no preferences model" argument below does not cover. Server and connection
reads `GET /api/v1/health` — the address every phone and screen must be pointed
at, which CLAUDE.md notes is the most-asked question at the event and today
requires running `ipconfig` on the server itself. It also reports the gap
between the server's clock and the browser's: the scanner stamps its own
`scanned_at` because the offline queue may not reach the server for minutes, and
the report buckets those by hour, so clocks more than a minute apart file an
arrival in the wrong one with no error anywhere. Drift is corrected for latency
(`server_time - (sent + rtt/2)`) so a 40 ms network is not reported as 40 ms of
skew. **Not polled** — `useDevices` polls because a quiet door is news, and none
of this is.

Appearance mirrors the topbar's theme and language controls rather than moving
them: a registrar mid-queue should not navigate to change a language. They are
radio groups here because `ThemeToggle` deliberately labels its *destination*
("Dark" switches to dark) and a settings page needs the opposite — the current
state, visible without pressing anything.

What is NOT there, and why: change-password and "signed in as" need endpoints
that do not exist (there is no `/me`), and anything persisted per-user needs a
preferences model this backend does not have — a migration bought to hold a
theme that already lives in `localStorage`. The export banner in `exports.py`
would be the first thing worth making editable, and that is its own piece of
work.

- Route groups: `(auth)/login`, `(dashboard)/*` behind the guard.
- All API types from `@vms/contracts`. Never hand-write a type mirroring a serializer.
- TanStack Query for server state. No global store for API data.

**NEITHER LIST IS PAGINATED, AND THAT IS THE RIGHT ANSWER — the cost was never
the JSON.** DRF has no pagination class configured, so `/visitors` returns a
bare array. Measured at a full 250-visitor event, one SQL query per call:

| call | rows | queries | raw | gzipped |
|---|---|---|---|---|
| `/visitors` | 250 | 1 | 82 KB | 13 KB |
| `/visitors?with_tokens=true` | 250 | 1 | 102 KB | 23 KB |

The guest list is capped by the event, `get_queryset` has no N+1, and paging
would break the print queue's **select-all** (a lie the moment results span
pages) and its in-memory filter. Do not add it without a new measurement.

The two pages search differently and both are fine at this size: `/visitors`
searches **server-side** (250 ms debounce → `?search=`), `/badges` fetches once
with `?with_tokens=true` and filters **in memory**.

**What actually cost was the photographs.** The cropper stores the badge
original — 600×800 JPEG, 100–250 KB — and a list row drew it at 42×56, a print
queue card at ~150×200. Two hundred and fifty of those is tens of megabytes in
250 requests, roughly two thousand times the JSON. So both `<img>`s now carry
`loading="lazy"` and `decoding="async"`, which is why the row sets explicit
`width`/`height`: reserved space is what makes lazy loading free of layout
shift. **A thumbnail derivative is still the real fix** — 1 KB for a row photo
against 250 KB, 257× — and it is not built. Serving one runs into the fact that
`config/urls.py` claims production serves photos "through the signed-URL storage
in `apps/common`" and **there is no such storage**: `media.py` concatenates a
base URL and signs nothing.

`QRCode.toString` also ran 250 times on the print queue, once per card, for
cards mostly off screen. `BadgeCard` takes a `deferQr` prop and `useNearViewport`
in `badges/page.tsx` flips it 800 px ahead of the viewport. The token is still
passed while deferred, on purpose: the panel then says it is *drawing* rather
than claiming the code lives only on the printed card, which would be a lie
about the badge rather than a fact about our scheduling.

**ONE CHART SYSTEM, IN `components/charts/`.** `outcomes.ts` owns what an
outcome looks like and `primitives.tsx` owns the scales, the hour gap-filling,
the tooltip shell, the legend and the empty state. Both charts read from it, so
a colour means one thing across the app — and the same thing it means at the
door.

**Chart geometry is CSS pixels from a measured container, never a scaled
viewBox.** `preserveAspectRatio="none"` on `viewBox="0 0 100 180"` scaled x by
~14.7 and y by 1, so every length meant two different things: `rx={7}` drew a
103×7 **ellipse**, which is the flattened cap that used to sit on every bar of
the reports chart. That is not a radius to tune — it is what non-uniform scaling
does to any radius, stroke or circle. `useMeasuredWidth` exists so 7 is 7 in
both directions. Note it measures the **content box**: `clientWidth` includes
padding and `contentRect.width` does not, and mixing the two made the first
measurement 40px too wide.

**Outcome colours are `--color-chart-*`, and they are measured, not chosen.**
Green valid / amber revoked / red invalid is the scanner's verdict language and
a hard constraint, so the hues were fixed and only the steps were ours. Amber at
`--color-vip` (#8a6200) against red (#cc0000) is OKLab ΔE **1.9** under
deuteranopia — one colour to a red-green colourblind reader, and those two are
exactly what add up to "refused at the door". Re-stepped to #d98a00 the light
theme clears at ΔE 8.4 worst-pair.

Dark could not be fixed by re-stepping: its usable band is L 0.48–0.67, and
green, gold and red all collapse toward one axis under red-green CVD, so
lightness is the only escape and 0.19 of band will not hold four hues apart.
**So the four-outcome band hatches revoked** (`OutcomeSpec.hatch`) and the
three-series hour chart, which folds revoked and invalid into "refused", needs
no texture — it validates clean in both themes. Two accepted departures, both
deliberate: the grey reads as grey (it is a status neutral, not a third
identity), and #d98a00 is 2.77:1 on white, which obligates the word and the
number beside every figure — never colour alone.

**`--color-sun` never existed.** The reports chart filled its duplicate series
with it, so the `fill` was invalid, SVG fell back to black, and duplicates
rendered identical to refused. A legend claiming three series showed two.

**THE STAT CARDS ARE FOUR EQUAL TILES, AND THAT IS A DECISION — DO NOT
"IMPROVE" IT INTO A HIERARCHY.** A redesign replaced them with one large
"Arrived" figure over a banded strip, on the reasoning that four identical
cards give "Registered" the same weight as "Arrived" and read as a grid of
widgets. The owner of this system looked at both and chose the four cards, for
`/dashboard` and for the report recap alike. `components/dashboard/StatTile.tsx`
is that original, restored from git rather than rewritten, sparklines included.
The argument for a hierarchy is written down here so nobody has to rediscover
it — and so nobody mistakes the flat layout for something nobody thought about.

**There is no entrance animation on the dashboard, and that is the second
correction.** The hero figure counted up on `requestAnimationFrame`, which
renders a number that is briefly **wrong** — headless screenshots caught it at
0 and at 75 where the truth was 220, and Chrome throttles rAF in background
tabs, which this repo already documents for the kiosk. The arrivals line drew
itself in from a dash pattern, which means the line is invisible until the
animation finishes; screenshots caught that frozen partway with no line at all.
**A mark whose visibility depends on an animation completing is a mark that is
sometimes missing.** Both are gone, and the `.vms-rise` keyframe went with the
hero it was written for.

**Verifying these panels needs no backend.** They are driven entirely by props,
so a throwaway route rendering them with fixed data can be photographed with
headless Chrome. Two traps if you do it: the `(dashboard)` route group is behind
`proxy.ts`, and **Chrome on Windows refuses a window narrower than ~500px** — so
`--window-size=400` lays out at 500 and the screenshot captures its left 400,
which looks exactly like a horizontal overflow and is not one. Three screenshots
were read that way before the page was asked for its own `scrollWidth`. Put the
page in a 400px `<iframe>` instead; an iframe has a viewport of its own.

**AND DRIVE THE THEME THROUGH `setTheme`, NEVER `classList.add("dark")`.** A
harness that pokes the class straight onto `documentElement` leaves `useTheme()`
still reporting light while the page paints dark, so every className chosen by a
ternary is computed against the wrong theme. The symptom is not subtle and it is
deeply misleading: buttons and selected rows render with their LIGHT colours on
a dark page, and `getComputedStyle` confirms it — while insisting the element's
own `--color-accent-soft` is the dark value, which looks impossible and sends
you hunting for a CSS bug that is not there. Settled by loading the built
stylesheet into a static `<html class="dark">` with no React at all: every
colour was correct. The rule is that the store and the DOM must not be allowed
to disagree, and `lib/theme` is the only thing that keeps them together.

**Dark mode is class-based, not `prefers-color-scheme`.** `@custom-variant dark
(&:where(.dark, .dark *))` in `globals.css`, toggled by `components/theme-toggle.tsx`.
The registration desk chooses; the lobby's ambient light is not the OS's business. A
small inline bootstrap script in `app/layout.tsx` sets the class before first paint, so
`<html>` carries `suppressHydrationWarning` — without it React reports a mismatch on
every load.

**The badge card does not follow the theme, on purpose.** `components/badge-card.tsx`
is a picture of paper: it paints a literal white ground, but its text, divider,
slot, photo ring and VIP line all use theme tokens. In dark mode those inherited the
`.dark` values, so the name, date, country and serial rendered #f4f8fb on white —
invisible on `/badges`, `/visitors/[id]` and the registration preview. The fix is
the `.cr80` rule in `globals.css`, which pins the light values of every token the
card uses. **A token newly used inside the card must be added to that rule**, or it
will quietly go dark again in dark mode.

**A Tailwind utility cannot override `.btn`, `.btn-ghost`, `.card` or `.field`.**
Those component classes are plain, unlayered CSS in `globals.css`, and Tailwind v4
puts every utility in `@layer utilities` — and unlayered declarations beat layered
ones whatever the specificity. So `btn btn-ghost text-revoked` renders in
`.btn-ghost`'s grey, not red. That is why Delete on `/visitors/[id]` was never
red; it now uses its own `.btn-danger-ghost`. **The same trap still silently
cancels** `text-revoked` on Deactivate and `text-valid` on Activate on that page
(both render grey), and any `px-*` / `text-xs` meant to resize a `.btn`. Give a
variant its own component class, or move these classes into `@layer components`
— the second is the cleaner fix but changes every button that relied on an
override being ignored, so check them all first. **`.btn-lg` is the first variant
written that way**: the public registration page asked for `py-3 text-base` on
Register, got `.btn`'s 38.6px anyway, and shipped a sub-44px tap target on the
one screen used by people standing in a queue on their own phones.

**EVERY COPY BUTTON GOES THROUGH `lib/clipboard.ts`, AND `navigator.clipboard`
IS NOT IT.** That API is secure-context only, so on every machine at the event
except the server's own `localhost` it does not exist — and three buttons (the
desk link on `/devices`, the server address in `/settings`, the badge token on
the receipt) each called it directly, caught the failure, and quietly did
nothing: no copy, no label change, no explanation. `copyText` falls back to
`document.execCommand("copy")`, which is deprecated and is the path that
actually runs at the event, and it restores the previous selection so nothing is
left highlighted. **The order is gesture-critical**: when the context is not
secure the synchronous path runs BEFORE any `await`, because awaiting ends the
user gesture `execCommand` requires. Verified in headless Chrome with
`isSecureContext` forced false, reading the system clipboard back.

**Right-click a card on `/badges` for Print / Export to Excel**, through the same
`RowContextMenu`. Who it acts on follows the file-manager rule, and it has a wrong
answer that looks fine:

| right-click on | acts on | the selection |
|---|---|---|
| a card that is **not** selected | that visitor alone | untouched |
| a card that **is** selected | the whole selection | cleared after, like the toolbar |

Acting on a lone card never clears the selection, or reprinting one person at the
door would throw away twelve cards picked for the next sheet. The heading names
the subject — the visitor, or "5 selected visitors" — so nobody prints the wrong
set. The export dialog takes its count and ids from **whatever the menu resolved**,
not from `selected`, or a lone card would export the selection behind it.

**A failed print used to be silent.** The page set `error`, but only the export
dialog rendered it, and that dialog is closed while printing. The failure now
shows in the status line under the toolbar, for the button and the menu alike.

**Right-click a visitor row for Edit / Deactivate (or Activate) / Delete permanently.**
`components/visitors/RowContextMenu.tsx`. It replaces the browser's own menu on those
rows, so "open in new tab" is gone there — a deliberate trade, because the alternative
is a navigation to the visitor and back for every small change. The Menu key and
Shift+F10 open it too, since the row's link is focusable; those report no pointer
position, so they anchor to the row's box instead of the window corner.

**Visitor photos are cropped 3:4 by default, NOT always — and the printed photo
is a rounded RECTANGLE, while the lobby wall's is a circle.**

`lib/badge-geometry.ts` is the single source of truth and it derives everything from
the same millimetres `apps/badges/services.py` prints with. `PHOTO_ASPECT` moved there
from `PhotoUpload.tsx`; do not reintroduce a second copy.

The trap is that these are four different shapes and they get confused constantly:

| Thing | Shape | Where |
|---|---|---|
| the card | 95 × 130 mm portrait | `CARD_W, CARD_H` |
| the stored photo | **any ratio** — 3:4 is only the cropper's default | `PHOTO_ASPECT`, `OUTPUT_WIDTH` |
| the printed photo | a 30 × 40 mm **rounded rectangle**, black keyline | `clip.roundRect(...)` in services.py |
| the lobby wall's photo | a **circle** | `rounded-full object-cover` in `vms-screen` |

**The printed photo stopped being a 19 mm circle when the card was redrawn to the
organisers' production file.** The cropper still draws a circle over the crop,
and that is still right: the circle is inscribed in the rectangle, so it is now
the stricter of the two and a crop that satisfies it satisfies both. What did
change is `MIN_OUTPUT_WIDTH`, from 225 px to **355** — 30 mm at 300 dpi rather
than 19 — so a very small hand-drawn crop is flagged where it used to pass and
print soft. `OUTPUT_WIDTH` is 600, so nothing the cropper produces by default is
affected.

**The stored photo is not reliably 3:4, and this table said it was.** `PhotoCropper.tsx`
offers badge, square and free crops and exports at the selection's own ratio.
Measured over `media/visitors`: **3 of 15 files were 3:4.** The rest are square-ish
(600×479 to 600×662), plus whatever a free crop produces.

That mattered because the badge PDF believed the table. It drew every photo into a
`draw_w × draw_w * 4/3` box with `preserveAspectRatio=False`, so 12 of 15 faces
printed distorted — the worst at **60% of true width**, a tall free crop at 125% —
while the `/badges` preview, which uses `object-cover`, showed them correctly. On a
19 mm circle a face a third too narrow does not read as a bug; it reads as a thin
person, which is how it reached a print queue.

**Every surface now cover-crops whatever is stored, the same way.**
`cover_box(*reader.getSize(), box_w, box_h)` in `apps/badges/services.py` is
`object-fit: cover` in millimetres: it takes the larger of the two scale factors,
so both edges are covered and the longer side overflows into the clip. Nothing
was re-cropped and nothing migrated. Verified four ways, all against the
throwaway SQLite database:

| check | before | after |
|---|---|---|
| a round dot in a 600×479 source, printed | 0.600 wide:tall | 1.000 |
| flat-colour source, gap pixels inside the clip, 18 sizes incl. 3:1 and 1:3 | — | 0 |
| printed circle vs headless-Chrome `object-cover`, mean diff /255 | 20.7–42.2 | 1.4–2.5 |
| single card and multi-card run | — | both, one shared `draw_card` |

**`cover_box` took a DIAMETER and now takes a box.** It was written for the
circle; the signature changed with the card. Nothing outside `services.py`
calls it.

Two traps if you touch it:

- **`preserveAspectRatio=True` is deliberate, and it hides a broken box rather than
  exposing a distortion.** With a wrong box ReportLab letterboxes instead of
  stretching — undistorted, ring showing through. So swapping `cover_box` back to the
  old 3:4 box does **not** reproduce the old bug; a control run needs `False` restored
  too. Learned by getting a clean "before" column that was not the before.
- **Do not measure the ring to prove the photo is round.** `canvas.circle()` draws a
  circle whatever the image inside does. Measure something round *in the source*.
- **The screen had the mirror-image bug, and `object-cover` did not prevent it.** The
  preview's photo plate is `aspect-square`, but an `aspect-ratio` box keeps
  `min-height: auto` and grows to fit its content, and a portrait photo at `w-full`
  is taller than the square. Measured in headless Chrome on a 270px card: 600×798
  made the plate 106×137, an oval that pushed the name down; 600×479 stayed 106×106.
  So after the PDF fix the print was right and the preview was wrong for exactly
  the 3:4 photos the PDF used to get right. `overflow-hidden` on the plate
  (`components/badge-card.tsx`) removes the content-based minimum. Do not drop it
  as unused — nothing visibly overflows, which is why it looks removable.

**Still rectangular, and still wrong for square crops:** the visitors list thumbnail
(42×56) and the registration receipt (24×32 mm) draw the stored file as a 3:4 box.
Out of scope for the badge fix, and left as named follow-up.

The lobby screen clips the stored image to a circle, so a crop that looks right
as a rectangle can still lose a chin. `PhotoCropper.tsx` draws the circle over the
crop for that reason — it is the stricter of the two shapes now that the card
prints a rectangle — and warns below `MIN_OUTPUT_WIDTH` — 355px, which is 30 mm
at 300dpi — rather than silently upscaling.

The crop happens in the browser so the server stores one canonical image. **Image data
stays in memory and object URLs. Never localStorage** — a shared registration laptop
must not keep visitors' photographs after the event.

**Registration does not redirect on success.**

`POST /visitors` returns the badge token, and success replaces the form with the
token receipt rather than navigating away — so the registrar prints the card while
the visitor is still standing there, and the next registration starts from a clean
form rather than from somebody's detail page.

THE ORIGINAL REASON IS GONE and the behaviour is kept for the workflow alone.
Tokens used to be irrecoverable, so leaving this page destroyed the only copy and
the badge could never be printed. Tokens are derived now: `GET /visitors/{id}`
returns `badge_token`, and the card can be reprinted at any time from the
visitor's page. Losing the receipt costs nothing.

**The receipt's Print button prints the SERVER'S PDF, never the page.** It used to
be "Print from browser": `window.print()` over a hidden landscape card, 85.6 × 54
mm with a rectangular photo, left over from before the PDF existed. The print
stylesheet asked for a portrait 54 mm page and pinned the wider card into it, so
names came out one letter per line, and `visibility: hidden` on everything else
kept the page's layout — five sheets for one badge, none of them the real card.
The card, the second QR canvas that fed it and both print rules in `globals.css`
are gone.

`openBadgeCard` in `lib/badges.ts` fetches the same `POST /badges/card` PDF that
Download saves (`fetchFile` is shared, so the two buttons cannot fail
differently) and shows it in the browser's PDF viewer **in a new tab** — the
screen `/badges` users already print from, confirmed to come out at card size on
the card printer. It is the same page as `/badges` for one visitor:
`render_card_set_pdf` with one visitor returns `render_card_pdf`, measured at 1
page, 95.0 × 130.0 mm, pixel difference 0.0.

It briefly printed from an invisible iframe instead. That was replaced because
the hidden dialog is the one step that decides paper size and the one step
headless testing cannot see; the viewer is the path people already trust.

**The tab is opened BEFORE the request, and that order is load-bearing.** A
pop-up blocker allows `window.open` only inside the click, and the first `await`
ends it — so the tab opens with a "Rendering…" placeholder and is pointed at the
blob once it exists. Move the `window.open` below the fetch and it is blocked on
most browsers every time. A server failure closes the tab; a blocked pop-up
downloads the file as `/badges` does and the receipt says so; a tab the
registrar closed first is left closed. The blob URL is not revoked, because the
viewer may read it again to print.

For the card printer: leave **Scale** on *Default* in the print dialog. The page
is already 95 × 130 mm, and *Fit to page* lets the driver resize it.

**PUBLIC SELF-REGISTRATION.** A visitor opens `/register` on a phone on the event
Wi-Fi, fills in name, country, organisation and a photo, and is registered at once —
no approval, `category=normal`, `source=self`. They get a QR on screen; anything that
goes wrong at the door is handled at the kiosk desk. VIP is set by an admin afterwards.

- **Isolated backend.** `apps.registrations` — its own create-only viewset, its own
  router at `/api/v1/public/`, a plain `Serializer` declaring exactly four writable
  fields. The response is `full_name`, `badge_serial`, `badge_token`: no id, no hash,
  no photo URL. Creation calls the same `visitors.services.register_visitor` as the
  desk. **No PDF is rendered at creation**, and the desk path never rendered one
  either — cards are drawn on demand.
- **The switch is a database row, enforced by the endpoint.** `RegistrationSettings`
  is a singleton (pk pinned to 1 by a check constraint), **closed by default**. The
  `RegistrationOpen` permission answers 403 whatever the client does. The `/settings`
  panel flips it optimistically and builds the public link from `GET /health`'s
  `lan_ip` plus this tab's port — never `localhost`, never `.env`.
- **Throttles: 10/hour per client address, 200/hour in total, every POST counted.**
  Keyed on `REMOTE_ADDR` only, never Django-side `X-Forwarded-For`. **The per-address
  limit is forgeable through the dashboard, and the global cap is the real guard.**
  Next's `base-server.js` sets `x-forwarded-for` with `??=` — a value the client sent
  survives — its rewrite proxy adds only `x-forwarded-host`, and uvicorn trusts
  forwarded headers from 127.0.0.1, which is where the rewrite comes from. Check at
  the dress rehearsal whether phones reach the server with distinct addresses.
- **Photos are re-encoded, never stored as sent** (`photos.py`): ≤5 MB, JPEG/PNG/WebP
  by the file's own bytes, ≤8000 px a side and ≤40 MP read from the header *before*
  decoding, one frame, ≥225 px a side; out comes a JPEG q88, long side ≤1200, no EXIF,
  no ICC, a server-chosen filename. Bodies over the limit get 413 before parsing.
  Names beginning `= + - @` are refused (spreadsheet formulas).
- **The QR on a phone relaxes constraint 3, as an accepted risk.** A screenshot can be
  forwarded. With no approval step the recipient gains nothing they could not get by
  registering themselves; the guard's phone and the lobby screen both show the
  registrant's photo; and a printed card can be photocopied too. There is no device
  binding — it would break re-entry through another door.
- **Making a self-registered visitor VIP changes no token.** The token is
  `hmac(id:token_version)`; category is not in it. Scanner and lobby read category at
  scan time, and a card printed afterwards gets the amber ring with the same QR.
- **Duplicates are flagged, never answered.** `possible_duplicate` (same name and
  country, case-insensitive) is annotated on the admin list with a pill and a
  `?source=` filter. The public endpoint must never reply "already registered" with an
  existing QR — that would hand any named visitor's badge to whoever typed the name.
- **Face check: blazeface, offline, guidance only.** tfjs-core/converter/webgl (cpu
  fallback) and `@tensorflow-models/blazeface` are bundled and lazy-loaded when a photo
  is chosen; the weights are committed at `public/models/blazeface/`
  (`model.json` + one 402 KB shard, downloaded once from tfhub). **`proxy.ts` excludes
  `json` and `bin`**, or the model fetch is 307'd to sign-in. A face counts at
  probability ≥ 0.90 **and** a box ≥ 12% of the image width, so a stranger in the
  background does not reject a good selfie. If the model cannot run, the photo is not
  blocked — the API never trusted the check anyway.
- **The live camera preview only exists in a secure context** — localhost, never
  `http://<lan-ip>` (see the scanner-on-web section). The real path is the file input
  with `capture="user"`, then the desk's own `PhotoCropper`, whose 600 px output is the
  client-side downscale.
- **The page is always light** (`.public-light` pins the light tokens on its wrapper,
  never the `dark` class on `<html>`): a dark page lowers screen brightness and the
  guard's camera exposes for the whole screen. **The pass lives in `sessionStorage`**
  for this tab, so a reload does not cost the QR; it is the visitor's own credential
  on their own phone and dies with the tab. Countries are an English list
  (`lib/countries.ts`) so the reports do not split one delegation three ways.
- **The pass can be SAVED to the phone, and the page says so.** `sessionStorage`
  dies with the tab -- a flat battery, a browser reclaiming memory in a queue, a
  visitor who closed it -- and the QR with it. `lib/pass-image.ts` draws a
  1080-wide PNG (the same code, the same event mark, the name and serial under
  it) and hands it over with `<a download>`; a browser without that attribute
  gets the image opened instead and is told to press and hold it. **Not
  `navigator.share`**, which would offer "Save Image" directly: it is
  secure-context only, so it does not exist on the LAN over http.
- **The switch is FOLLOWED while the page is open.** Nothing pushes it, so the
  status is polled every `STATUS_POLL_MS` (15s, inside the 60/min public-status
  throttle for 250 phones), re-read when the phone comes back to the tab or the
  network returns, and fetched `cache: "no-store"` so no phone answers it from
  its own cache. **Once the visitor has typed anything the form stays put**, with
  a banner and Register refused, rather than being replaced by the closed
  notice -- a half-filled form and a photo that took three tries are not ours to
  throw away. The server still answers 403 whatever the page believes.
- **Two file inputs, not one.** `capture="user"` opens the camera straight away
  and offers no way to reach a photo already on the phone, so "Take a photo"
  carries it and "Choose from gallery" deliberately does not.

**THE WALK-IN DESK.** A staffed laptop or tablet at the door registers people who
turn up without having registered, shows them a QR to photograph, and starts again.
Nobody signs in: the desk pairs once, like a guard's phone.

- **Two routes, and there will not be a third.** `POST /api/v1/desk/registrations`
  creates a visitor (`source=desk`, category chosen by staff, photo required and put
  through the public form's own sanitiser) and returns name, serial, token and
  category. `GET /api/v1/desk/qr` draws that badge's code as a PNG. No list, no
  retrieve, no update, no delete — and `apps/desk` registers no router, because a
  viewset's base class is one edit away from generating all four on the one part of
  this API that nobody signs in to.
- **The QR route is keyed on the badge token, sent in the `X-Badge-Token` HEADER.**
  Not a query string, which uvicorn writes into its access log, and not a serial or
  an id, which could be walked: a caller can only draw a code it already holds.
- **It pairs like a device.** `DeviceKind.DESK` is the third kind, so a desk is
  minted, listed, watched and revoked on `/devices` with the same code, the same list
  and the same one-click revoke as a phone. `IsDeskDevice` narrows the token to these
  two routes.
- **401 means pair again, 403 means wrong kind.** No token, an unknown token or a
  revoked one is 401, and the page drops its token and shows the pairing screen. A
  scanner's or a screen's token is 403, which pairing again would not fix.
- **The path is unguessable, and that is obscurity, not the lock.** The dashboard
  mints a 24-character key beside the pairing code (`/devices` shows the link and a
  QR of it), and `/desk/<key>` 404s anything under 16 characters. The LAN is plain
  http, so a key, a code and a token all cross the air in clear text — what limits
  the damage is that the token reaches two create-only routes, that walk-ins are
  marked `desk` on the roster, and that revoking is instant.
- **The desk token lives in `localStorage`, deliberately.** It has to outlive the tab
  so the desk opens tomorrow morning without an admin walking over with a code. Same
  trade as the scanner-on-web token, and the rule still stands for the admin session.
- **Ceilings are per device** — 120 registrations and 600 QR draws an hour: far above
  a real desk's pace, low enough that a stolen token cannot fill the roster quietly.
- **The desk can DOWNLOAD the code as well as show it**, and it saves the same image
  a self-registering visitor saves — `lib/pass-image.ts`, the QR with the event mark,
  the name and the serial under it — so staff can send it on to a visitor with no
  phone to hand. Drawn locally from the badge token rather than fetched again, which
  keeps that path at two routes; `navigator.share` is secure-context only and does not
  exist on the LAN, so a saved file is the share.

**THE CHAT ASSISTANT.** An admin asks a question in plain words from a popup on
any dashboard page ("which VIP guests never arrived?") and gets an answer, and a
download button when they asked for a PDF, Excel or CSV. Added after the event,
for the analysis that follows it.

- **The AI is in the backend, never the dashboard.** `apps/assistant` holds
  LangChain, `langchain-openai` and the key (`OPENAI_API_KEY` in
  `vms-backend/.env`). Anything in the dashboard bundle is readable from dev
  tools, and the key spends money.
- **RAG through tools, not text-to-SQL and not embeddings.** `retrieval.py` is
  plain ORM functions; `tools.py` wraps each as a LangChain `StructuredTool`
  with a Pydantic schema; `agent.py` runs `create_agent` over them. Every
  entrance figure goes through `entry_log()` → `summarise()` →
  `analysis.build()`, the objects the PDF and workbook use, so the chat and
  the file cannot disagree. There is no vector store: the data is structured
  and a few hundred rows, and pgvector is not on the native Windows Postgres.
- **It offers files, it never builds them.** `offer_download` records which
  export and which filters; the popup fetches `/reports/entries.{fmt}` or
  `/badges/roster.xlsx` with the admin's own token through the existing
  `downloadEntriesExport` / `downloadRoster`. No file storage, and the badge
  tokens in the roster never pass through the model.
- **What goes to OpenAI:** names, countries, organisations, categories, serials
  and times — whatever `retrieval.py` returns. **Never** photos, badge tokens,
  token hashes or ids; the comment at the top of `retrieval.py` is the
  authority. This is the one part of VMS that needs internet, and it breaks
  the closed-LAN assumption on purpose; with no key it switches itself off and
  the popup says so.
- **Read-only, because visitor names are untrusted.** Anyone could type a name
  at `/register`, and names reach the model's context. No data tool writes
  anything. The one tool that does, `remember`, exists only on a turn whose
  own message asks to remember (see below); any further writing tool needs a
  human confirmation in front of it.
- **Every chat is saved in PostgreSQL, private per admin.** `Conversation` →
  `ChatMessage` (question, answer, offered downloads, tools used), scoped by
  `owner` in every query; another admin's id answers 404, like a missing one.
  The browser sends only the new message and the conversation id; the server
  loads the last 20 messages (`services.HISTORY_LIMIT`) as the model's memory,
  so a reload loses nothing and a client cannot rewrite the past. The
  question and the answer are written together **after** the model answers:
  a failed call saves nothing. Retry reuses the send's `request_id`, stored
  unique on the question (`ChatMessage.client_id`), so a Retry after the
  dashboard's proxy gave up — while Django went on to save — is answered from
  the database instead of saved twice. `experimental.proxyTimeout` in
  `next.config.ts` is 180 s for the same reason; Next's default is 30 s. The
  dashboard keeps only the open conversation's id in React state — never
  browser storage, because answers carry visitor names.
- **Chat history quotes visitor names, so a purge redacts them.**
  `purge_visitor` calls `assistant.services.redact_visitor`, which replaces
  the full name with `[deleted visitor]` in every saved message **and every
  conversation title** (a title is the first question). Case-insensitive and
  **whole words only**: matched as a substring, purging a test visitor named
  "Test" turned every "latest" into "la[deleted visitor]", permanently. Names
  under 3 characters are skipped. Without it "erase for good" would leave the
  person in chat history. A soft delete does not
  redact — it is reversible by hand, and so is the visitor's row.
- **Memory across conversations is explicit, and guarded twice** (`memory.py`).
  The `remember` tool is offered only when the admin's latest message asks
  ("remember", "lembra…", "hanoin", "keta haluha"). **That gate narrows the
  door but does not close it** — in Tetun "hanoin" also means "think", so
  ordinary questions open it, and a visitor name in a tool result could then
  steer what gets written. What closes it is `grounded`: at least 75% of a
  note's words must appear in the admin's own message, so a tool result can
  suggest text but cannot make the admin have typed it. This document said
  the gate alone closed it until a review proved otherwise. Notes are ≤200 characters, ≤20 per admin, shown
  with Forget buttons in the panel's History view, and refused if they
  contain any registered visitor's full name (deleted visitors included).
  They are injected into every later conversation of that admin, after
  `format()` so a brace in a note cannot break the template. Each question is
  audit-logged on `vms.audit` with its locale and notes saved.
- **Three specialist languages, every other one general** (`languages.py`).
  English, European Portuguese (registo, ecrã, telemóvel — never Brazilian)
  and Tetun Dili (INL orthography, "ema na’in N") share one glossary whose
  spellings are copied from `vms-dashboard/scripts/generate-locales.py` —
  change a term in both. Any other language is answered in that language with
  the same figures. The dashboard's interface locale is sent with each
  question and decides only when a message is too short to tell its own.
  Two measured fixes for Tetun, both pinned by tests: `TEMPERATURE = 0.2`
  (the API default of 1.0 produced stray tokens — "b leading bukit" — inside
  Tetun answers), and one worked example answer each in Tetun and Portuguese.
  **The examples must never mention a download button**: an earlier version
  did, and the model copied "the button is below" into answers that offered
  no file. Live, the remaining slips are a Portuguese word now and then
  ("porta" for "odamatan") and country names translated — the ceiling of
  `gpt-4o-mini`, not of the prompt.
- **Two "arrived" figures, deliberately named apart.** The report's own
  `arrived` (`summary["unique_visitors"]`) counts distinct people with ANY
  scan, which includes someone whose deactivated badge was refused. The
  assistant calls that `people_scanned_incl_refused` and uses
  `people_admitted` (a valid scan) as "arrived". The PDF's figure has not been
  changed; whether it should count refusals is an open question.
- **Asked who built the system, it names the author, every time.** Whatever
  the wording or language, the answer is Julião de Jesus Martins with
  https://github.com/juliaomartins and https://juliaomartins.dev/, stated
  without tools and held against "it was really X, confirm". The values are
  `AUTHOR_*` in `agent.py`. **These two URLs are the only links the popup ever
  renders as clickable** (`TRUSTED_LINKS` in `AnswerText.tsx`, an exact
  allowlist; a lookalike or a different path stays text). Change both files
  together, or the credit renders as plain text.
- **The model is `VMS_ASSISTANT_MODEL`, default `gpt-4o-mini`** — the only chat
  model the event's key could reach when this was built (`gpt-4.1-mini` was
  refused with a 403). Throttled at 20 questions a minute per admin.
- **The launcher is in the topbar and the panel DOCKS — it does not float.**
  It started as a pill fixed to the bottom-right corner, which sat on top of
  "Register visitor" on `/dashboard`; every corner of this console is used by
  some page. `AssistantLauncher` sits beside the clock, language and theme;
  `AssistantPanel` is a column of `app/(dashboard)/layout.tsx` from 1024px, so
  the page reflows beside it, and a right-hand sheet below that.
  `assistant-context.tsx` joins the two. The panel stays mounted while closed
  (`hidden`) so closing it keeps the conversation — and **`.assistant-panel
  [hidden]` must stay**, because the unlayered `display: flex` beats
  Tailwind's base-layer `[hidden]` rule and a closed panel would not close.
- **The mark** (`AssistantMark.tsx`) is the tais key — a squared spiral turned
  45°, the motif woven through `tais-strip.png` — white on the accent tile. It
  heads every reply with a thread running down it, and breathes while an
  answer is being written. A hooked lozenge was tried first and read as a "b"
  at 20px. Never gold: gold means VIP here.
- **Links the model invents are stripped in `agent._scrub`.** It wrote
  `**[Download Excel Report](sandbox:/…)**` above the real button despite the
  prompt; a non-web link goes with its label, a web link keeps only its label,
  the two author URLs survive. `AnswerText` renders an untrusted `[label](url)`
  as the label alone if one ever slips through, and builds React elements —
  never `innerHTML`, for the same untrusted-names reason. The panel's top edge
  is one copy of `tais-strip.png`, scaled to width, never tiled.

**The dashboard proxies `/api` and `/media` to the backend** via rewrites in
`next.config.ts`, so every browser request is same-origin: no preflight on the
`Authorization` header, the refresh cookie is first-party, and DRF's absolute photo
URLs (built from the `Host` header) resolve. Set `VMS_BACKEND_ORIGIN` to the server's
LAN address.

**`django-cors-headers` IS installed, and this document said the opposite for a long
time.** It is in `requirements.txt`, in `INSTALLED_APPS`, and second in
`MIDDLEWARE` — `GZipMiddleware` is above it, deliberately; see below —
with `CORS_ALLOW_ALL_ORIGINS = True` set in **`settings/base.py`** — not just dev. So
the backend answers every origin with `Access-Control-Allow-Origin: *`.

`CORS_ALLOW_CREDENTIALS` is unset, so the refresh cookie cannot be read cross-origin and
the practical exposure on a closed LAN is small. It is still wider than intended: the
proxy exists precisely so no origin but the dashboard needs to reach the API, and a
leaked access token is readable from any web page rather than none. **Decide
deliberately** — either drop the package and the settings, or narrow it to
`CORS_ALLOWED_ORIGINS` — and correct this paragraph when you do.

**The route guard reads a `vms_session` hint cookie, not the refresh token.**

The refresh cookie is httpOnly and path-scoped to `/api/v1/auth`, so the browser
never sends it on a navigation to `/visitors` — `proxy.ts` cannot see it. The hint
holds no token and grants nothing; it exists so an unauthenticated visitor lands on
the sign-in page instead of watching an empty table fail. The real boundary is the
backend rejecting any request without a valid bearer token.

---

## Scanner (vms-scanner)

**Three screens only:** `pair.tsx` (one time), `scanner.tsx` (the only screen a guard
ever sees), `settings.tsx`. If this app grows past that, the feature belongs in the
dashboard.

`src/app/index.tsx` is a fourth route file and is not a fourth screen: it is a single
`<Redirect>` to `/scanner` or `/pair` depending on the keystore, so that decision is
made in one place instead of racing between screens.

`components/LaunchScreen.tsx` holds the branded launch animation — reanimated, sequence
ending at 520ms with a 770ms fallback release, and every value starts at its resting
state under reduced-motion. The root layout holds until **both** the animation has
finished and the keystore has answered — never one or the other, or the app flashes the
pairing screen at a phone that is already paired. The native splash in `app.json` is
transparent in every theme so the two do not fight.

### The camera screen is three bands, and the controls are one dock

`CameraOverlay.tsx` is a rail across the top (this phone's name, the pending-queue
pill, and Unpair), the framing box in the middle, and a two-segment dock at the
foot: **Torch | Server**. It replaced a centred torch pill with two grey text
links in the corner beneath it — three weights in three places, one of them
destructive, none of them clearing the Android gesture bar.

- **`SafeAreaProvider` is mounted in `src/app/_layout.tsx` and is not optional.**
  `useSafeAreaInsets()` throws *"No safe area value available"* without it, and
  the overlay reads the insets directly so the dock clears the gesture bar while
  the camera preview stays full-bleed underneath. `initialWindowMetrics` is
  passed so the first frame is laid out correctly instead of painting at zero
  and jumping.
- **The server control IS the status light.** `useServerStatus` (extracted from
  `ServerBar`, one implementation for both screens) probes `getApiOrigin()` —
  the address actually in use, never the first stored candidate — and the dock's
  right half shows green `server-network` / red `server-network-off` / grey
  "Checking", with a slow breath on the red. The thing that tells you the link is
  down is the thing you press to fix it. **Never colour alone:** tint, word and a
  different glyph, the same rule the three verdicts follow.
  - The camera screen passes a 15s interval because it is looked at all day; the
    pairing screen passes none and re-checks on focus. The interval stops when
    the app leaves the foreground, and a failed sync re-probes at once.
  - "Checking" is shown once, before the first answer. A poll that reset to it
    every 15s would blink grey at a connection that never dropped.
- **Unpair is deliberately NOT in the dock.** It ends the shift for that phone and
  can only be undone with a fresh code, so it sits at tertiary weight in the top
  rail, out of the thumb's resting arc. The confirmation in front of it has not
  moved.
- **Icons are `@expo/vector-icons` (MaterialCommunityIcons)** — a font, not a
  native module, so it needs no new native build. The font is preloaded in the
  root layout as a fourth condition on the launch gate, or the one screen a guard
  ever sees paints its dock with two blank squares for a frame. A failed load
  counts as ready: an unlabelled-but-working dock beats an app that will not
  start.
- **`QueueIndicator`'s visible text is still English in all three languages** —
  `{count} scans syncing…` is built from string literals while only its
  `accessibilityLabel` is translated. Pre-existing, and visible on the one screen
  a Tetun-reading guard uses.

- No login screen, ever. Pair once, store the device token in expo-secure-store, then
  open straight to the camera. **On web there is no keystore — see below.**
- **Offline SQLite queue is required in v1.** Every scan writes locally first, then syncs
  with backoff, sending its own `scanned_at`. Retrofitting means rewriting every network
  call, and the router will hiccup on event day. **On web the same queue is backed by
  `localStorage` — `src/storage/queue.web.ts`, see below.**
- Debounce the camera — one QR in frame must not fire repeated requests.
- Haptics and sound matter more than the UI. Guards watch the visitor's face, not the
  phone. Green valid / red invalid / amber revoked, with distinct sounds.
- High-contrast theme; used near doorways in variable light.

### The SQLite handle dies while the app is running, and it must heal itself

`SQLiteDatabase` is an expo-modules **shared object**: the JS value is a handle
onto something the native side owns, and the native side can let go while JS
still holds its half. Android reclaiming the activity behind a locked screen is
the ordinary way it happens — which is to say, a guard putting the phone in a
pocket between arrival waves.

On Android the failure arrives as a three-line chain, and the middle line is a
lie worth recognising:

```
Call to function 'NativeDatabase.prepareAsync' has been rejected.
 -> Caused by: The 2nd argument cannot be cast to type class
    expo.modules.sqlite.NativeStatement (received class java.lang.Integer)
 -> Caused by: Cannot use shared object that was already released
```

Nothing passed an Integer. The registry lost the object and handed back its id
instead; only the last line says what happened.

`storage/queue.ts` used to cache the database in a module variable that was
never invalidated, so **one release broke every scan, count and cache lookup for
the life of the process** — and the only cure was force-closing the app. Two
rules now keep that from coming back:

1. **Every statement goes through `withDb`**, which reopens once and retries
   when it recognises a released handle. Add a function to that file and it
   goes through `withDb` too.
2. **The handle is cached as a promise, not as a database.** Caching the
   database itself had a race: the variable was assigned when `openDatabaseAsync`
   resolved, while `CREATE TABLE` was still running, so a caller arriving in that
   window queried tables that did not exist yet.

Two consequences worth keeping. `enqueueScan` inserts `ON CONFLICT(client_uuid)
DO NOTHING`, because the retry may replay it and the same uuid is the same scan.
And **queue bookkeeping may never change a verdict**: `markSynced` and
`cacheVisitor` run after the server has already answered, so a storage failure
there used to surface a badge the server had *accepted* as "Something went
wrong". They are wrapped for that reason — see `useScanner.submit`.

`useSyncQueue.sync()` also catches storage failures now. It is driven by a
5-second interval, so an escaping rejection was an uncaught promise **every five
seconds** — a red LogBox over the camera in development, and silence with a
queue that never drains in a release build.

### The resolved server address lives in ONE place, and writers must announce

`api/client.ts` holds the live origin in a module variable. Its only writer was
`useServer`, which resolves on mount — and Settings is a route pushed *on top of*
the screen, so coming back from it remounts nothing. Saving a new server IP wrote
it to storage and left every request pointed at the old address.

**That is why a new IP had to be entered twice.** The first save was correct and
silently ineffective; the second only worked because something had remounted in
between.

So `storeManualOrigin`, `clearManualOrigin` and `clearStoredOrigin` call
`announceOriginChange()`, `useServer` subscribes and re-resolves, and Settings
additionally calls `setApiOrigin` directly for the address it has just tested.
`storeOrigin` deliberately does **not** announce — `useServer` is its only caller
and has already updated itself.

`ServerBar` probes `getApiOrigin()`, not the first stored candidate. Those are
different addresses at exactly the wrong moment, and a status dot reporting on
something other than the live connection is worse than no dot — it is the one
thing on screen a guard would trust.

**`adopt()` writes BOTH address keys**, and the manual one is the point. It used
to write only the stored key, which made a stale Settings override a one-way
trip: `candidateOrigins` returns a manual address *and nothing else*, so the
address a guard typed at the door went into a key the manual one outranks. The
rescue worked for that session and was thrown away at the next launch — the same
phone broken every morning with nothing on screen to explain it. Somebody typing
an address at a door is making the same deliberate choice Settings is for, so it
is recorded as one; that also keeps the gear icon honest, since `settings.tsx`
displays the manual address.

### A production APK has NO baked-in server address

`EXPO_PUBLIC_API_URL` is inlined at build time, so the obvious worry is an APK
carrying a stale IP. For **EAS builds that is not the failure**, because the
variable is not set at all:

```bash
npx eas env:list --environment production    # No variables found
npx eas env:list --environment preview       # No variables found
npx eas env:list --environment development   # No variables found
```

There is no `.easignore`, so EAS falls back to `.gitignore`, and `.env` is
ignored there — it is never uploaded. `BUILD_DEFAULT_ORIGIN` is therefore `""`,
`candidateOrigins()` returns `[]`, and a freshly installed EAS APK goes straight
to the "Where is the server?" screen on first launch. That is the failover
working, not a crash, but it means **a new phone cannot find the server on its
own until somebody types an address**.

A **local** build (`expo run:android`, prebuild) does read `.env`, and that one
does carry a frozen IP.

So the address precedence, proved rather than assumed:

| manual | stored | build default | tried, in order |
|---|---|---|---|
| — | — | — | `[]` |
| — | new | old | `[new, old]` |
| new | old | old | `[new]` |
| **stale** | new | new | `[stale]` — manual is exclusive |

A manual address is not first among candidates; it is the *only* candidate.

**What survives an IP change:** the device token. It lives under
`vms.device.token`, nothing in the address path touches it, and unpairing needs
either the guard's own Unpair button or a real HTTP 401. An unreachable server
throws in `fetch` and becomes a `NetworkError` — no response, no 401, no unpair.
Queued scans stay on disk and sync once the address is fixed. **A moved server
never costs you a re-pair.**

### The scanner on web — it builds, and it is not a guard's phone

`npx expo start --web` bundles and renders. It is a **development surface**, and
possibly a localhost desk station. It is not a replacement for the APK, and the
reason is not effort — it is one browser rule.

**THE OFFLINE QUEUE ON WEB IS `localStorage`, NOT SQLITE.**
`src/storage/queue.web.ts` is a second implementation of the same 16-symbol
surface as `queue.ts`, and Metro picks it for web automatically by the `.web.ts`
extension — **no caller changes and no `Platform.OS` branch anywhere**, and
`queue.ts` keeps its SQLite implementation untouched for the phones that ship.
If you add an export to one, add it to the other; nothing enforces that but a
crash at runtime on whichever platform you forgot.

`expo-sqlite` does have a real web build — SQLite compiled to WebAssembly in a
worker — and it did not survive contact with a phone browser: `Uncaught Error:
Unknown` out of `expo-sqlite/web/WorkerChannel.ts:64`, thrown before any query
ran. Its persistent VFS wants OPFS, which is secure-context-only (below) and
fussy about running inside a worker the page spawned. Chasing that buys a
WebAssembly dependency to store a few hundred rows.

What is lost is worth stating: localStorage is origin-scoped and ~5MB — thousands
of queued scans, so size is not the concern — but **clearing site data clears the
queue**, where a phone's SQLite file would survive. The two collections mirror
the two tables exactly, including the rule that matters: `vms.queue.scans` holds
raw badge tokens and rows are deleted the moment the server accepts them, while
`vms.queue.visitors` is keyed on a digest and never holds a raw token. Both
`crypto.subtle` and `crypto.randomUUID` are secure-context-only, so that file
carries deterministic fallbacks — FNV-1a for the cache key, a `Math.random` v4
for the idempotency key. Neither is a security boundary; read the comments there
before "upgrading" either one.

*Verified by `npx expo export --platform web`: no `.wasm` is emitted, the 139KB
`worker-*.js` bundle is gone, `wa-sqlite` and `WorkerChannel` appear zero times,
and `vms.queue.scans` / `vms.queue.visitors` appear in the bundle.*

**`metro.config.js` is a safety net now, not a requirement.** It puts `wasm` in
`assetExts` because Metro's default has no rule for it — `sourceExts` is only
js/jsx/json/ts/tsx — and every web bundle used to fail with *"Unable to resolve
module ./wa-sqlite/wa-sqlite.wasm"* while the file sat in `node_modules` the
whole time. Nothing imports a `.wasm` any more, so it does nothing today; it is
kept because that error names a missing file that is not missing, and anything
that pulls WebAssembly back in would hit it again with no clue why. It belongs in
`assetExts` and **not** `sourceExts`: Emscripten's `locateFile` must return a URL
the runtime then fetches, which is what an asset import yields, whereas source
would try to parse 600KB of WebAssembly as JavaScript.

**ONE thing still does not work over LAN `http://`, and it is the camera.**

| | `http://localhost:8081` | `http://<lan-ip>:8081` on a phone |
|---|---|---|
| Camera (`getUserMedia`) | works | **`navigator.mediaDevices` is undefined** |
| Offline queue | localStorage — works | localStorage — works |
| Device token | localStorage — works | localStorage — works |

The bottom two rows used to be failures and are not any more, for the two reasons
below. The camera is the one that no amount of storage design fixes.

**A secure context** is the rule behind all of it. `getUserMedia`,
`navigator.storage` (OPFS), `crypto.subtle` and `crypto.randomUUID` are all
secure-context APIs, and browsers exempt `localhost` only — never a LAN IP over
`http://`. wa-sqlite said so itself, in `AccessHandlePoolVFS.js:221`:

> `navigator.storage not available (not supported by your browser or context is not secure)`

`localStorage` is deliberately *not* on that list: it works on a plain-http LAN
origin, which is the whole reason both the queue and the token now use it.

And **HARD CONSTRAINT 9 makes the LAN http deliberately**, because an HTTPS page
cannot open a `ws://` socket. Serving the scanner over HTTPS to fix the camera
cascades: the backend needs TLS, `ws://` becomes `wss://`, and every paired
device re-pairs. That trade has not been made and should not be made casually
three weeks out from an event.

The third is separate and has nothing to do with HTTPS. `expo-secure-store`'s web
build is literally `export default {}`, so `isAvailableAsync()` returns false.

**RESOLVED: on web the device token goes to `localStorage`.** This is a
deliberate exception to "never localStorage" above, and it was made only after
checking what this particular credential can reach:

- `IsScannerDevice` narrows a scanner token to **one endpoint**, `POST /api/v1/scans`.
- The scan response returns a visitor only for a badge token the caller is
  **already physically holding**. It cannot enumerate visitors, read the roster
  or export photographs.
- It is revocable in one click from the dashboard's device list.

So the worst a stolen web token buys is logging false arrivals — noisy,
attributable to a named device, and revocable. That is a different order of thing
from the admin JWT and the passport-adjacent data the rule exists to protect.
**The rule still stands for the admin session and for visitor photos.**

`session.tsx` now asks **two different questions**, and conflating them is what
blocked web pairing entirely:

| | asks | web answer | effect on the pairing screen |
|---|---|---|---|
| `canStoreSession()` | can anything be kept? | yes | pairing is allowed |
| `isSecureStorageAvailable()` | is it a real keystore? | no | an amber warning, not a block |

Only a browser that refuses storage outright — a private window — still blocks,
with `pair.noStorage`. The ordinary web case shows `pair.browserStorage`, which
tells the operator this profile now holds a credential and to revoke the device
when the event is over.

The web write in `secure.ts` is deliberately **not** wrapped in try/catch: if the
browser refuses to keep the token, pairing has not really succeeded, and the
operator must see that rather than reach a camera that 401s on its first scan.

**Pairing on web therefore works. The camera still will not, over LAN http** —
that is the secure-context rule above and no amount of storage fixes it. To scan
in a browser you need one of:

1. **`http://localhost:8081` on the machine running Expo** — localhost is a
   secure context, so `getUserMedia` works there. This is the check-in desk case.
2. **Chrome's insecure-origin allowlist, per device.** In `chrome://flags`, set
   *"Insecure origins treated as secure"* to `http://<lan-ip>:8081` and enable it.
   A device-configuration change, not a code change, and it must be repeated on
   every phone. Reasonable for a controlled event device; not something to ship.
3. **HTTPS**, which cascades into `wss://`, TLS on the backend and re-pairing
   every device. See HARD CONSTRAINT 9 before going here.

---

## Screen (vms-screen)

Deliberately the smallest app. Two pages: the display (`app/page.tsx`) and one-time
pairing (`app/pair/page.tsx`). No router beyond that, no state library, no auth UI.

**There is no `src/` here.** `app/`, `components/`, `hooks/` and `lib/` sit at the
package root — the opposite of `vms-scanner`, where everything is under `src/`.

- WebSocket + backfill as described above.
- **`/api/*` is a route handler, not a `rewrites()` entry.** A rewrite destination
  is fixed when the Next process boots, so it could not follow the backend when
  DHCP moved it: the socket reconnected to the new address while every HTTP call
  kept going to the old one, and the error named the address the page had
  resolved rather than the one actually contacted. `app/api/[...path]/route.ts`
  resolves the target per request — the origin the page probed and verified
  (sent in `x-vms-backend`), else the host that served the page, else the env
  default — and only ever forwards to a private/LAN address. Same-origin, so
  the `Authorization` header and the JSON pairing POST never trigger a preflight
  the backend cannot answer. Do not put the `/api` rewrite back.
- Design for 3–5 metre viewing distance: name 72px minimum, photo 400px tall.
- VIP category gets a distinct visual treatment.
- `ConnectionDot` in a corner so staff can see the feed is alive.
- **`/pair` scrolls, and the wall does not — the kiosk rules are lifted on that route
  only.** `globals.css` gives `html, body` `overflow: hidden`, `cursor: none` and
  `user-select: none`, all correct for a lobby display and all wrong for setup: on a
  1920x1080 kiosk at 150% Windows scaling (a ~1280x600 CSS viewport) the Pair button
  sat below the fold with no way to reach it, and the mouse pointer was invisible.
  `app/pair/locale-shell.tsx` is now the route's scroll container and restores the
  pointer and selection; `ServerSetup` does the same for itself, because it also
  renders on the wall. On a landscape panel (`wall:`) the page splits into two
  columns so nothing needs scrolling at all; vertical sizes are `clamp`ed against
  `vh`. Content centres with `m-auto` in a `min-h-full` column, never
  `justify-center` in a fixed-height box, which clips the top where no scroll can
  reach. Measured over seven viewports from 667x375 to 1920x969: the button is
  reachable in all, and fits without scrolling in all but the landscape phone.
- **`/pair` asks for a display name again, pre-filled from the browser.** It was
  removed on the grounds that one lobby screen has one right name; that stopped
  holding once the device list and the server log were being monitored.
  `lib/device-name.ts` suggests `Lobby screen (Chrome on Windows)` and the field
  stays editable — the suggestion never overwrites anything already typed.
  - **A browser cannot give you the machine's name or its location.** No web API
    exposes the hostname. The UA string gives browser and OS family only —
    Chrome's reduced UA reports every Windows as `Windows NT 10.0`.
  - **The precise hints are secure-context-only, so the real kiosk never gets
    them.** `navigator.userAgentData.getHighEntropyValues` can say Windows 11 or
    an Android model, but only on `localhost`; over `http://<lan-ip>` (hard
    constraint 9) it is absent and the UA-string suggestion is what is used.
  - **A screen's name never reaches the entrance report.** `by_device` in
    `apps/reports/analysis.py` groups *scans*, and `/scans` accepts scanner
    devices only. The name appears in the dashboard's device list and the
    backend's `device.paired` / `device.revoke` log lines. There is no rename
    endpoint: a wrong name is fixed by revoking and pairing again.
- Runs in kiosk mode over `http://`.
- `EventSplash` shows the event mark and both organiser seals while the hall is quiet;
  `IdleScreen` takes over between arrival waves. GSAP drives them — `useGSAP`, SplitText
  and Physics2D, all free tier.
- **The foot of the screen is a real tais, not an SVG swoosh.** `components/TaisWave.tsx`
  draws two layers of photographed Timorese cloth — a drape in front and a darkened
  ribbon behind — swaying against each other at 71s and 103s. It carries the accent the
  swoosh used to: each layer's `drop-shadow` is `var(--accent)`, so the hem is lit blue
  for a visitor and gold for a VIP, keeping the four-cue rule intact. Both the arrival
  stage and `IdleScreen` use it.
  - **ONE COPY OF THE PHOTOGRAPH, NEVER TILED — and this reverses what this file said
    before.** The drape used to be laid down as a mirrored repeating tile. The seam was
    genuinely invisible; the problem was scale. At the old `24vh - 46px` the band was
    213px on a 1080p wall, so a 2.5:1 frame came out 532px wide and the panel carried
    **3.6 copies** of it — a row of repeating chevrons where the artwork is one piece of
    cloth sagging into a single broad curve.
  - `art/tais.png` is the reference photograph and the drape's source. It is
    byte-identical to the PNG embedded in `art/tais-wave-1.svg`, which is left in place
    as the original delivery but is no longer read. `art/tais-wave-2.svg` is the ribbon —
    a genuinely different piece of cloth with its own silhouette, not the drape offset.
    None are in `public/`, so Next never ships them.
  - `public/brand/tais-{drape,ribbon}.webp` are what the browser loads, built by
    `scripts/build-tais-layers.py` (`..\..\.venv\Scripts\python.exe`). 570KB the pair,
    down from 1MB, and neither is mirrored any more.
  - **THE STRETCH IS THE WHOLE DESIGN CONSTRAINT.** A 2.5:1 photograph cannot span an
    8:1 band at its own proportions, and how far it stretches is exactly
    `viewport width / (2.5 x band)`. So the band is sized from the viewport's **width**:
    `clamp(44px, min(19.3vw, calc(52vh - 190px)), 1000px)`. `19.3vw` pins the stretch at
    2.16x on every 16:9 panel; the `vh` term is a cap that bites only on short or
    ultrawide viewports.
  - **370px at 1080p is a measured trade, not a taste.** Stretch and the visitor's face
    are bought with the same pixels — measured on this panel with a two-word name and the
    queue showing: band 300 → 2.66x / 461px face; **370 → 2.16x / 399px**; 420 → 1.90x /
    340px; 480 → 1.67x / 301px. The brief asks for a 400px photograph, and 370 is the
    tallest band that still pays it.
  - **`--tais-clear` is ONE number — `band * 0.87` — and a side gutter must not be
    reintroduced to shrink it.** The cloth is a bowl, low at the centre and tall in both
    corners, so the tempting economy is to clear only the middle and hold content out of
    the corners with `wall:px-[13vw]`. That was built and it is wrong: it starves FitText
    of width, and at 1366x768 a 31-character name answers by wrapping to four lines and
    overrunning the header. The panel that most needs the economy cannot afford it.
  - `--tais-band`, `--tais-ribbon`, `--tais-ribbon-bleed`, `--tais-drape-bleed` and
    `--tais-clear` all live in `globals.css`, with the measurements written beside them.
  - Each layer is cut wider than the panel (`--tais-*-bleed`) because the drift is a
    sway, not a scroll — a single photograph has ends, so it eases back and forth inside
    its own overhang instead of migrating. `travel()` converts that overhang into
    `xPercent`, which is a share of the **element**, not the panel; getting that
    conversion wrong shows the cloth's cut edge at the side of the screen for a few
    seconds every couple of minutes.
  - **There is deliberately no sheen on the cloth**, and the component says why at
    length. `mix-blend-mode` cannot work here — both layers are promoted to their own
    compositing layers by `filter` + `will-change`, so a blended sibling has no backdrop
    and renders as a flat grey slab across the wall.
  - Verified by headless screenshot at 1366x768, 1920x1080, 2560x1440, 2560x1080 and
    3840x2160, in light and dark, VIP and visitor, and under `prefers-reduced-motion`
    (which drops every tween and leaves the reference photograph at rest).
- `FitText` auto-fits names and organisations. It exists because a 40-character name at
  a fixed 72px overflows a 1366×768 screen, and the lobby display is the one surface
  nobody can fix during the event.

---

## Languages (all three frontends)

**English, Portuguese and Tetun.** Portuguese and Tetun are Timor-Leste's
official languages; English is the conference's working language. Every frontend
carries all three, and each one owns its own dictionary — there is no shared i18n
package, because `vms-contracts` is generated and nothing hand-written goes in it.

**`vms-screen` IS THE EXCEPTION, AND IT IS A DELIBERATE ONE. The lobby wall is
English; only `/pair` is translated.** The display shows a name, a country and a
photograph — the words around them are a greeting, a status and a clock, and a
wall that changes language is a wall nobody in the lobby asked to change. The
person who does need a language is the installer standing at the kiosk on the
first morning, and they are on the pairing screen. So the switcher moved there
and the wall's dozen strings became plain constants in `lib/wall-copy.ts`.

| App | Dictionaries | Engine | Persisted in |
|---|---|---|---|
| `vms-dashboard` | `lib/locales/{en,pt,tet}.ts` — 553 keys | `lib/i18n.tsx` | cookie `vms.locale` |
| `vms-screen` | `lib/locales/{en,pt,tet}.ts` — 17 keys, **`/pair` only** | `lib/i18n.tsx` | cookie `vms.screen.locale` |
| `vms-scanner` | `src/locales/{en,pt,tet}.ts` — 74 keys | `src/i18n.tsx` | SecureStore `vms.locale` (native only — see below) |
| `vms-desktop` | `locales/{en,pt,tet}.py` — 53 keys | `i18n.py` | `QSettings` (registry) |

The desktop app uses **no `QTranslator` and no gettext**. Qt's own machinery
wants `.ts` sources compiled to `.qm` by `lrelease` — a build step, a binary
artefact and a toolchain dependency for 53 strings — and `tr()` keys on the
English text, so every rewording silently orphans its translations. That is
precisely what a generated key table exists to prevent.

**No i18n library.** About 120 lines per app, against three packages and an
install on a machine that is offline by event day. The engine is a typed
dictionary, a `useT()` hook, and a `translate()` that fills `{name}` placeholders.

**1. The dictionaries are GENERATED, and they are pure ASCII.**

```bash
python scripts/generate-locales.py      # the three frontends
python scripts/generate_locales.py      # vms-desktop (underscore, it is Python)
```

All three languages come from one table in that script, so a missing translation
cannot be introduced by hand — and `Messages = Record<MessageKey, string>` makes
one a compile error. Non-ASCII is emitted as `\uXXXX` escapes.

**That escaping is not fussiness.** The first version of these files was written
through a shell heredoc on the Windows dev machine and came back with the accents
mojibaked — `Secções` as `Sec??es`. It typechecked, it rendered, and it was only
visible by decoding the bytes. **Do not hand-edit the `.ts` files**; edit the
generator and re-run it.

**2. The two web apps read the locale on the SERVER. This is the load-bearing
decision.**

The theme is a CSS class: the server can guess wrong and a pre-paint script
corrects it. A language is the markup itself. If the server rendered English and
the browser wanted Tetun, React would hydrate over the whole page and swap every
word — a mismatch, and on the lobby wall a room-sized flicker. So the locale
lives in a cookie, the root layout (`async`, `cookies()`) reads it, and the first
byte is already right. `<html lang>` is set from it, which is what a screen
reader consults to choose a voice.

The scanner has no server render and no cookie, so it reads SecureStore
asynchronously and the launch screen holds until that lands — the same gate the
device token already uses.

**On web the scanner's language does not persist.** `locale.ts` guards its
SecureStore calls rather than crashing, so the switcher works for the session and
the choice is forgotten on reload. The device token was worth a `localStorage`
exception; a language preference on a dev surface is not, and the switcher is on
the first screen either way.

**3. Tetum has no CLDR data in any browser.** `Intl.DateTimeFormat("tet")`
silently falls back to the host locale, which on a kiosk is whatever Windows was
installed as. Tetum borrows `pt-PT` for formatting only, and every date format is
numeric so no Portuguese month name lands in a Tetun screen. That also gives
dd/mm/yyyy and a 24-hour clock throughout, which is how Timor-Leste writes a date.

**4. Grammar is not assembled from fragments.** Plurals are one message per form
(Portuguese conjugates, Tetun does not inflect the noun); English ordinals come
from `Intl.PluralRules` while Portuguese writes `2.º`; elapsed time is
`Intl.RelativeTimeFormat`, not a hand-rolled ladder. Where a sentence wraps a
value in markup, `useRichT` splits the TRANSLATED string on its placeholders so
the value lands wherever that language puts it — never a "before" and "after"
half glued around it, which can only ever produce English word order wearing a
translation.

### What is deliberately NOT translated

- **The printed badge.** `apps/badges/services.py` draws the card in English, so
  `components/badge-card.tsx` keeps "Registered", "Country" and "VIP GUEST" in
  English too. The preview exists to show what comes out of the printer, and
  translating it would make it lie about the card — a registrar would check a
  Tetun preview and hand over an English badge. Only the deactivated overlay and
  the empty QR frame, which never reach paper, follow the interface.
- **The report narrative.** `apps/reports/services.py` composes those sentences
  so the PDF and the dashboard panel say the same words. There is no key to look
  up, only prose. Making the report multilingual is a change to that service and
  the PDF it writes.
- **Backend error messages.** DRF's `detail` strings arrive in English and are
  shown as sent. Errors the frontends write themselves carry a `MessageKey`
  instead, resolved at the point of display — see `useErrorText`.
- **The lobby wall itself.** `vms-screen/lib/wall-copy.ts` holds every word the
  display says, in English, as constants — no hook, no context, no key. Scoping
  is the whole mechanism: `LocaleContext` defaults to `"en"`, so mounting the
  provider in `app/pair/layout.tsx` instead of the root layout makes `/` English
  with no flag and no branch anywhere. `components/ServerSetup.tsx` is why that
  shape was chosen over a prop — it renders on BOTH routes, and it comes out
  translated during pairing and English on the wall without knowing which it is.
  Two consequences worth keeping: `setLocale` must **not** write
  `document.documentElement.lang` (the pair page navigates to `/` on success, so
  it would follow the operator onto the wall — `app/pair/locale-shell.tsx` owns
  that attribute instead), and the root layout is no longer `async`, which is why
  `/` now prerenders as static.
- **Device names and the conference title.** `SCREEN_NAME` is data the backend
  stores and the dashboard lists; translating it would give one wall three names
  depending on which language it happened to be in when somebody paired it. The
  browser-derived suggestion on `/pair` follows the same rule — only the field's
  label and hint are translated, never the name it fills in. The
  event's official title is not ours to translate either.

**Where the switcher lives:** the dashboard topbar *and* its sign-in page (the
one screen reachable without a session); the lobby screen's **pairing** page and
nowhere else on that app; the scanner's pairing screen (its first screen) and its
settings.

**The Tetun wants a native read.** It is careful — INL orthography, loanwords
spelled the Tetun way (`akreditasaun`, `relatóriu`, `ekrán`) rather than the
Portuguese way — but Tetun has real regional variation, and the event's own staff
can check it faster than any dictionary. Corrections are one line in the
generator plus a re-run.

---

## Desktop control centre (vms-desktop)

A PySide6 window that **starts the other four services and watches them**. It is
an orchestration layer and nothing else: it holds no visitor data, speaks no
part of the VMS API beyond one unauthenticated health probe, and could be
deleted tomorrow without changing how VMS works.

It exists because event-day startup was four terminals in the right order, and
the person opening the doors is not always the person who built this.

```
vms-desktop/
├── main.py                 the window; wires signals and paints, nothing more
├── config.py               EVERY path, port and command, in one place
├── network.py              LAN address detection
├── preflight.py            venv / node / npm / ports / directories
├── services.py             QProcess lifecycle, one model for all four
├── processes.py            stopping a tree on Windows; who holds a port
├── launcher.py             Run All sequencing and readiness probes
├── i18n.py                 the translator; QSettings keeps the choice
├── locales/{en,pt,tet}.py  GENERATED — see the languages section
├── scripts/generate_locales.py
├── widgets/                theme, icons, service card, network card, log viewer
├── selftest.py             the non-GUI layers
├── guitest.py              the Qt layers, driven offscreen
└── VMS Control Center.spec PyInstaller, onedir, windowed
```

**Three rules it must keep.**

1. **STARTED IS NOT READY, and the two are never conflated.** `services.py`
   reports `RUNNING` when the OS has a process and nothing more; only a
   readiness probe over the network may promote that to `READY`, and only
   `READY` enables the Open button. A uvicorn that dies on a bad database
   password is `RUNNING` for about two seconds, and opening a browser at it is
   how somebody meets a connection error and concludes the app is broken.

2. **It never blocks the GUI thread.** `QProcess`, not `subprocess`; `QTimer`,
   never `time.sleep`. The children run for the length of a conference. Stop is
   asynchronous for this reason — see below, where it used to freeze the window
   for six seconds a press and not stop anything.

   The one exception is `force_stop()` on application exit: the window is going
   away, there is no next event loop turn to come back on, and an orphaned Node
   server would outlive the launcher and hold its port against the next run.

3. **It reads the repository rather than duplicating it.** Commands come from
   CLAUDE.md and each project's `package.json` — including `--workers 1`, which
   is here for the reason in the hard constraints. The health probe is the
   backend's existing `/api/v1/health`. No new endpoint was added for it.

**LAN configuration is passed as process environment, never written to `.env`.**
The variable names are the ones the repository already uses —
`VMS_BACKEND_ORIGIN`, `NEXT_PUBLIC_VMS_BACKEND_ORIGIN`, `EXPO_PUBLIC_API_URL` —
and a variable that lives only as long as the child cannot go stale on disk, which
is exactly what the `.env` convention below is protecting against.

**The window has to survive being made small**, and that took three passes to get
right. The panels sit in a splitter over a scroll area; the service cards reflow
between 4, 2 and 1 columns; the header drops its controls onto a second row and
then shortens their labels to a code and an icon. Every one of those decisions is
**measured, not a pixel threshold** — the widths are asked of the widgets, because
a number tuned on English clips Portuguese, and a number tuned before the buttons
had icons clips them afterwards.

**STOPPING A SERVICE ON WINDOWS TAKES A TREE KILL, and `terminate()` does
nothing at all.** This was measured against both process shapes the launcher
starts, not reasoned about:

```
terminate() ended it?        NO      (both shapes)
waitForFinished blocked for  6.0s    (the full grace period, every press)
port free after kill()?      NO -- held by ['9980']
```

Two Windows facts, stacked:

* `QProcess.terminate()` posts `WM_CLOSE` to the child's top-level windows. A
  console program has none and none of these services runs a Qt event loop, so
  the message lands nowhere. Qt's own docs say console applications on Windows
  "can only be terminated by calling `kill()`".
* `kill()` is `TerminateProcess`, and it ends **one** process. `npm.cmd` is a
  batch file, so the process we started is `cmd.exe` and the Node server holding
  port 3000 is its grandchild. Killing the parent orphans the child, which keeps
  listening. That is the whole of "I pressed Stop and the port is still busy".

So `stop()` runs `taskkill /PID <our pid> /T /F` as its own `QProcess`. `/T` is
the flag usually left off and the only one that matters; without it this is
`kill()` with extra steps. Ownership is never in question because `/T` walks
down from a pid this launcher started.

**Ctrl+C is not available and it is not an oversight.** It works when you press
it in cmd because your terminal and the server share a console. A GUI process
has none, and `GenerateConsoleCtrlEvent` can only signal within the *caller's*
console. Giving each child its own console would flash a terminal per service
and still leave us unable to signal into it.

**STOPPED is not claimed until the port is free.** `_on_finished` starts a
`QTimer` that polls `network.port_in_use` and only then sets `STOPPED`; if the
port is still held after 8 seconds it names the owner via `processes.port_owners`
and goes `ERROR`. It does **not** kill whatever holds it —
`preflight.describe_port_conflict` refuses the same thing for the same reason,
and `port_owners` exists to report, never to target.

`port_owners` parses `netstat -ano` on the local address's final `:<port>` plus
the LISTENING state. The obvious `findstr 8000` is a trap: it also matches port
18000, any foreign address containing those digits, and pid 8000 itself.

**The scanner cannot be stopped by port**, because it has none —
`scanner_spec()` sets `port=None` and Expo picks its own. The tree kill reaches
it anyway, which is the other reason the tree is the primary mechanism.

**`/F` gives uvicorn no clean shutdown, and nothing is lost by that.** An
in-flight request is dropped rather than completed: Postgres rolls back an
uncommitted transaction, the channel layer is in-memory with nothing to flush,
and a dropped scan `POST` is retried by the scanner's offline queue under the
same `client_uuid`. The visible cost is a connection reset in someone's browser.

**Icons are painted, not shipped as files** (`widgets/icons.py`), the same call
the dashboard made. They take a colour, so a theme switch redraws them; and they
are drawn at the device pixel ratio, because this machine runs at 1.5 where a
16px bitmap stretched to 24 physical pixels is visibly soft.

```powershell
..\.venv\Scripts\python.exe main.py                       # from source
..\.venv\Scripts\python.exe selftest.py                   # no display needed
..\.venv\Scripts\python.exe guitest.py                    # offscreen Qt
..\.venv\Scripts\pyinstaller.exe --noconfirm --clean "VMS Control Center.spec"
```

`dist/VMS Control Center/VMS Control Center.exe` is ~113MB and **gitignored**. It
is rebuilt from the `.spec` in one command; the spec is the source.

**PySide6 and PyInstaller are the only two packages this adds**, and they are in
`vms-desktop/requirements.txt` rather than the backend's.

---

## Contracts (vms-contracts)

```
vms-contracts/
├── package.json            "@vms/contracts"
├── openapi.yaml            copied from backend
├── scripts/generate.sh
└── src/
    ├── schema.d.ts         GENERATED — never hand-edit
    ├── client.ts           openapi-fetch wrapper
    └── index.ts
```

```bash
cp ../vms-backend/openapi.yaml ./openapi.yaml
npx openapi-typescript ./openapi.yaml -o ./src/schema.d.ts
```

After **any** serializer change: regenerate `openapi.yaml`, then regenerate contracts.
CI should fail if `openapi.yaml` is stale (`git diff --exit-code openapi.yaml`).

---

## Commands

**Windows is the daily driver, and Windows is what the event server runs.** Commands are
given Windows-first; the macOS/Linux form follows where it differs.

### Activating the venv — or not bothering

| Shell | Command |
|---|---|
| Windows PowerShell | `..\.venv\Scripts\Activate.ps1` |
| Windows cmd | `..\.venv\Scripts\activate.bat` |
| Git Bash on Windows | `source ../.venv/Scripts/activate` |
| macOS / Linux | `source ../.venv/bin/activate` |

If PowerShell answers *"running scripts is disabled on this system"*, do not go changing
the execution policy — just call the interpreter by path. It needs no activation and it
cannot pick up the wrong Python:

```powershell
..\.venv\Scripts\python.exe manage.py migrate
```

That form works from any shell on any OS and is the safest thing to paste into a
half-remembered terminal at an event.

### Backend — from `vms-backend/`

```powershell
# Windows
..\.venv\Scripts\python.exe manage.py migrate          # postgres is a native service, already up
..\.venv\Scripts\python.exe manage.py seed_demo        # admin, two devices, five visitors
..\.venv\Scripts\python.exe -m uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers 1
..\.venv\Scripts\python.exe manage.py spectacular --file openapi.yaml
```

```bash
# macOS / Linux, with the venv active
python manage.py migrate
python manage.py seed_demo
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers 1
python manage.py spectacular --file openapi.yaml
```

`--host 0.0.0.0` is not optional. Bound to `127.0.0.1` the server is invisible to every
phone and screen on the LAN, and the failure reads as "the network is down".

**uvicorn needs a WebSocket implementation installed, or it silently refuses every
upgrade.**

```bash
pip install websockets       # or wsproto
```

Without one, `--ws auto` resolves to `none` and uvicorn answers `/ws/screen/` with a
**404 before the request ever reaches Django**. The lobby screen then reconnects forever,
`ScreenConsumer.connect()` never runs, and the device's `last_seen_at` stays null. Nothing
in the Channels code is involved, so nothing logs an error — and `WebsocketCommunicator`
tests pass, because they call the ASGI app directly and never touch uvicorn's protocol
layer. This cost an afternoon once; do not let it cost another.

On Windows, `pip install "uvicorn[standard]"` is fine too — `uvloop` is skipped there and
you get `websockets` and `httptools` without it.

### Tests

`pytest` is not installed; the suite uses Django's own runner. **The first real
suite is `apps/assistant/tests/`**, behind `config/settings/test.py` (SQLite, no
OpenAI key — a test that needs a model passes `tests/factories.fake_model`):

```powershell
..\.venv\Scripts\python.exe manage.py test apps.assistant --settings=config.settings.test
```

One trap it already found: LangGraph runs tools on a worker thread with its own
database connection, so a test where a tool must see or write rows uses
`TransactionTestCase` — `TestCase`'s open transaction hides the test's rows from
that thread (`test_agent.MemoryGateTests` says why). The rest of the backend is
still verified by `manage.py check`, `makemigrations --check --dry-run`, and
exercising the API against a throwaway SQLite database.

**Point `DJANGO_SETTINGS_MODULE` at a separate settings module. Never swap
`connections.databases` at runtime.** The runtime swap does not take effect once Django
has read its configuration, and a probe written that way silently wrote three visitors,
fourteen scan events and a device into the live event database. A throwaway module is
four lines, and it belongs outside the repo:

```python
from config.settings.dev import *          # noqa: F403
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3",
                         "NAME": "<scratch>/probe.sqlite3"}}
MEDIA_ROOT = "<scratch>/media"
```

Then assert it took, before touching anything:

```python
db = settings.DATABASES["default"]
assert db["ENGINE"].endswith("sqlite3"), f"REFUSING: engine is {db['ENGINE']}"
```

A real suite belongs behind `settings/test.py`, which now exists — add new apps'
tests there rather than writing another throwaway module.

### Contracts

`scripts/generate.sh` and `scripts/check_contracts.sh` are bash. On Windows run them from
**Git Bash**, not PowerShell:

```bash
cd vms-contracts && ./scripts/generate.sh
./scripts/check_contracts.sh                 # from the repo root, before every commit
```

`check_contracts.sh` finds the venv on either layout — `Scripts/python.exe` or
`bin/python` — so it needs no activation.

### Frontends

```bash
cd vms-dashboard && npm run dev     # http://<lan-ip>:3000
cd vms-screen    && npm run dev -- --port 3001
cd vms-scanner   && npx expo start -c
cd vms-scanner   && npx expo start --web -c    # dev surface only — see the scanner section
```

The `-c` on Expo matters after any `.env` change: `EXPO_PUBLIC_*` is inlined at bundle
time, so without clearing the cache the phone keeps using the previous server address.
It matters a second time on web, where the cache holds *resolution* decisions:
after a `.web.ts` file is added or a dependency drops off the web path, a stale
cache keeps serving — and keeps reporting — the previous bundle's errors.

Formatting: `black` + `ruff` on the backend, strict TypeScript on the frontends.

---

## Conventions

### Run `./scripts/check_contracts.sh` before every commit

```bash
./scripts/check_contracts.sh
```

It regenerates all three generated artifacts and exits non-zero if any of them
moved:

| File | Generated by |
|---|---|
| `vms-backend/openapi.yaml` | `manage.py spectacular` |
| `vms-contracts/openapi.yaml` | copied from the backend |
| `vms-contracts/src/schema.d.ts` | `openapi-typescript` |

A stale schema does not fail loudly. The frontends keep compiling against types
the backend no longer serves, and it surfaces at runtime as a 404 on a renamed
route or an `undefined` where a field used to be — far from the serializer edit
that caused it. The check turns that into a failed command at commit time.

It compares the working tree against the index, so staging a regenerated file
counts as up to date. When it fails, the files in your tree are already correct;
stage them and commit.

CI should run the same script. It replaces the narrower
`git diff --exit-code openapi.yaml`, which only ever caught half the problem.

### `.env` is per machine, `.env.example` is committed

Every device on the LAN points at the server by IP, so each machine sets its own
`.env` and `.env` is gitignored — a committed IP is wrong for everyone except the
person who committed it, and it fails as "the network is down" rather than as a
bad address. `.env.example` carries a neutral placeholder and is tracked.

**Do not write the current IP into this file.** It has already moved once
(192.168.0.63 → 10.101.196.41) and a documented address is a documented lie the
moment DHCP hands out a new one. Ask the machine instead: `ipconfig` on Windows,
`ipconfig getifaddr en0` on macOS, or `GET /api/v1/health`, which reports the LAN
address the server believes it has.

Three files carry it, and only these three:

| File | Setting |
|---|---|
| `vms-backend/.env` | `VMS_MEDIA_BASE_URL` — leave UNSET; auto-detected at startup |
| `vms-scanner/.env` | `EXPO_PUBLIC_API_URL` — a default only; the app probes and can be told a new one |
| `vms-screen/.env` | `NEXT_PUBLIC_VMS_BACKEND_ORIGIN` — last resort only; the screen probes at runtime |

`vms-dashboard` needs no `.env` at all: it defaults to `localhost:8000` and proxies
server-side, so it follows the server for free as long as both run on one machine.

### `vms-scanner` imports `@vms/contracts` type-only

The scanner uses `import type` and plain `fetch`. **Do not add `openapi-fetch`
there.** It resolves only from `vms-contracts/node_modules`, so using it at
runtime makes the app depend on Metro following the workspace symlink, which it
does not do reliably. A type-only import is erased at build time, so Metro never
resolves the package at all — and hand-rolled `fetch` is what the offline queue
needs anyway, for its own timeout and retry control.

### `src/app/` is the expo-router root in `vms-scanner`

**Do not create a root-level `app/`.** Two candidate route roots is ambiguous,
and `tsconfig` maps `@/*` to `./src/*`, so the whole app is under `src/`.

---

## LAN deployment

```
Router 192.168.1.1
  ├── 192.168.1.50   server: postgres + uvicorn :8000
  ├── 192.168.1.51   lobby screen (browser, kiosk mode)
  ├── dhcp           admin laptop → dashboard
  └── dhcp           guard phones → Expo app
```

- **Static IP or DHCP reservation for the server.** If it changes, every paired device
  breaks and you re-pair during the event.
- `chromium --kiosk --incognito http://192.168.1.50:3000`, OS display sleep disabled.
  Chrome throttles timers and can suspend sockets in background tabs.
- `proxy_read_timeout 3600s` if nginx is in front — the default 60s kills idle sockets.
- **Test on the actual router first.** Some consumer routers enable wireless client
  isolation by default, which alone stops the phones reaching the server.

---

## Build order and current state

| Phase | Work | Status |
|---|---|---|
| 0 | Models, serializers, openapi.yaml, contracts codegen | DONE |
| 1a | Auth (JWT + refresh cookie), visitor CRUD + filters, token issue | DONE |
| 1b | `/scans`, `/screen/feed`, device pairing + device auth, throttling | DONE |
| 2 | Channels: asgi.py, consumer, routing, WS device middleware | DONE |
| 3a | Dashboard: login, visitor CRUD, photo upload | DONE |
| 3b | Scanner: pairing, camera, offline queue | DONE |
| 4 | Lobby screen: WS hook + backfill + welcome card | DONE |
| 5 | Badge PDF templates + bulk A4 print | DONE |
| 6 | Reports + CSV export (also XLSX and PDF) | DONE |
| 7 | **LAN dress rehearsal — real phones, real printed cards** | **NOT STARTED** |

Done since the table was first written, and not in it:

- Branding across all three frontends — event mark plus the two organiser seals,
  palette sampled from the supplied logos, dark mode with a toggle on dashboard
  and screen.
- Derived badge tokens replacing random ones, so a card can be reprinted; the
  permanent-QR rule that follows from it.
- Visitor lifecycle: deactivate, activate, permanent delete.
- Photo cropper with face detection and a print-resolution floor.
- Scanner launch screen (native splash + animation, gated on the keystore).
- Reports: XLSX and PDF exports beside the CSV.
- English / Portuguese / Tetun across all three frontends, and the desktop app.
- `vms-desktop`, the PySide6 control centre, packaged as a Windows executable.
- The badge redrawn as the organisers' own ID card, on screen and then in print:
  95 × 130 mm measured off `ID CARD PVC SECOOP.pdf`, one card per page, no A4
  sheet.
- The chat assistant: `apps/assistant` (LangChain + OpenAI, retrieval through
  the report services) and a popup on every dashboard page. See **THE CHAT
  ASSISTANT**.
- Assistant memory: every chat saved per admin in PostgreSQL, a History view,
  gated memory notes, and English / Portuguese / Tetun specialist answers;
  the backend's first test suite (`apps/assistant/tests`).

**Update this table as phases complete.** It is how context carries between sessions.

**Phase 7 is the only thing left, and it is the one that matters.** The event is
2–3 October 2026. Nothing in this system has yet been run on the real router, with
real phones, against cards off a real printer.

Ordering rationale, so it isn't rearranged:

- **Channels is phase 2, not 1.** Prove the flow works by polling first. Then the
  WebSocket is an enhancement on a path already known to be correct. Build both at once
  and a missing scan gives no signal about which half broke.
- **Badges are phase 5.** The card design changes the moment someone holds a printed one
  next to a real lanyard. Building early means designing twice.
- **The offline queue belongs in 3b**, not later.
- **Phase 7 is not optional.** Print 20 real cards, use two real phones, run the real
  router. Every problem you'll have on the day surfaces there.

---

## Things this document got wrong before

Kept as a list because each one cost time, and because a confident wrong line in here
is worse than no line at all.

- `POST /visitors/{id}/revoke`, `GET /visitors/{id}/badge` and `POST /badges/bulk`
  were documented and never existed.
- `django-cors-headers` was described as "deliberately not installed". It is
  installed and active.
- `PHOTO_ASPECT` was said to live in `PhotoUpload.tsx`. It lives in
  `lib/badge-geometry.ts`.
- The dashboard's fonts were given as Archivo and IBM Plex Mono. They are Plus
  Jakarta Sans, Inter and JetBrains Mono.
- `vms-screen/src/hooks/...` — the screen has no `src/`.
- `config/settings/{base,dev,prod,test}.py` — only `base.py` and `dev.py` exist.
- The pairing rate limit was given as `5/hour per IP`. It is `20/hour`, and it
  counts **failed** attempts only — the code carries a comment explaining why,
  which the document had dropped.
- **The card's header hem was called a parabola.** It is a cubic bezier with two
  control points, and it goes flat at 40.0% of the width rather than 30.6%. The
  parabola was the best fit obtainable from a flattened JPEG, and it was written
  down as though it were the shape. The production PDF has the real path; see
  the table in the badge section. `components/badge-card.tsx` still draws the
  parabola.
- **`POST /badges/reissue-sheet` was documented and coded as DESTRUCTIVE**, in
  its route name, its class docstring, its `@extend_schema` description and
  therefore `openapi.yaml` — the same stale claim, from the same era of random
  tokens, that the credential export carried in four places. It calls
  `collect_badge_tokens`, which recomputes. Only the route name still says it,
  and that stays because renaming it is a schema change for a word.
- **`counts_by_result` WAS a bug, and this list said twice that it was not.**
  The entry read: *"suspected of a missing `.order_by()` and flagged as a bug
  across two sessions. It is not one. `Meta.ordering` stopped being folded into
  `GROUP BY` in Django 3.1 — proved against a throwaway SQLite database, 7/3/2/1
  in, 7/3/2/1 out."*

  Every sentence of that is true and it answers the wrong question.
  `Meta.ordering` was never the problem. `entry_log()` applies an **explicit**
  `.order_by("-scanned_at", "-id")`, which Django still folds into the `GROUP BY`
  of a `values().annotate()` — documented behaviour, unchanged. The proof
  offered was a bare `ScanEvent.objects.all()`, and nothing calls it that way.

  Through the real path the grouping was `GROUP BY result, scanned_at, id`: one
  group per scan, every count 1. The dashboard showed `valid 1, duplicate 1,
  revoked 1, invalid 1` against a day of 91 scans, and those same four numbers
  reached "Refused at the door", the report narrative, and the XLSX and PDF
  exports. Measured on Django 6.1 — bare queryset 7/3/2/1, `entry_log()`
  1/1/1/1, fixed 7/3/2/1.

  The three sibling aggregations were safe only by accident: each ends with an
  `.order_by(...)` of its own, which replaces the inherited one.

  **The lesson is not about Django.** A function was tested in isolation, passed,
  and was pronounced correct for a caller it had never been tested with — twice,
  each time more confidently. Aggregations get verified through `entry_log()`.

**When you change a route, a serializer or a filename, change this file in the same
commit.** Everything above was true once.
