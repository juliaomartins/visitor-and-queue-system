<div align="center">

<sub>CASE STUDY · DRCCMD 2026</sub>

# Visitor and Queue System

**Ministers, delegations and guests all arrived at Palm Spring at the same moment.**<br>
Each of them carried a QR ID card, so a single scan at the door was all it took —<br>
and the lobby screen welcomed them by name.

[![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)](vms-backend/)
[![Channels](https://img.shields.io/badge/Django_Channels-WebSocket-44B78B)](vms-backend/apps/scans/)
[![Next.js](https://img.shields.io/badge/Next.js-16-000000?logo=nextdotjs&logoColor=white)](vms-dashboard/)
[![React Native](https://img.shields.io/badge/React_Native-Expo_SDK_57-000020?logo=expo&logoColor=white)](vms-scanner/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-native-4169E1?logo=postgresql&logoColor=white)](vms-backend/)
[![PySide6](https://img.shields.io/badge/PySide6-Qt_6-41CD52?logo=qt&logoColor=white)](vms-desktop/)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)](vms-contracts/)
[![LangChain](https://img.shields.io/badge/LangChain-OpenAI_gpt--4o--mini-1C3C3C?logo=langchain&logoColor=white)](vms-backend/apps/assistant/)
![Status](https://img.shields.io/badge/status-used_live_at_the_event-success)

</div>

---

| | |
|---|---|
| **Event** | Díli Regional Cooperative Conference and Ministerial Dialogue 2026 |
| **Place** | Palm Spring, Díli, Timor-Leste |
| **Date** | 2–3 October 2026 |
| **Medium** | Django, Next.js, React Native, Expo |
| **Studio** | [Inovtec](https://inovtec.digital) |
| **Status** | Used live at the event |

<p align="center">
  <img src="evidence/juliao-martins-waiting-for-arrivals.jpg" alt="The lobby screen reading 08:51, waiting for arrivals, beside the registration desk and its team" width="100%">
  <br>
  <sub><b>Nº 01</b> — 08:51, the lobby screen, waiting for the first arrivals.</sub>
</p>

---

## The problem

A ministerial dialogue brings many important guests through one entrance in a
very short window. A paper list at the door turns that moment into a queue —
and nobody inside the hall knows who has already arrived.

## How it worked

Two paths at the door, one welcome. Visitors already in the system go
**straight to the scan**; anyone who isn't is registered on the spot.

```
Not yet registered ─▶ I. Register on the spot ─▶ II. QR ID card ─┐
                                                                 ▼
Already registered ────────── straight to the scan ─────▶ III. One scan ─▶ IV. Welcome on screen
```

<table>
  <tr>
    <td width="50%" valign="top">
      <img src="evidence/juliao-martins-welcome-desk.jpg" alt="The welcome desk at the entrance">
      <h3>I. Register on the spot</h3>
      Anyone not yet in the system is registered at the desk by the welcome
      team — name, country, organisation and a photo — and leaves with a
      working badge.
      <br><sub>The welcome desk at the entrance.</sub>
    </td>
    <td width="50%" valign="top">
      <img src="evidence/juliao-martins-badges-on.jpg" alt="QR code ID cards worn by delegates">
      <h3>II. The QR ID card</h3>
      Every registered visitor carries an ID card with a QR code of their own,
      printed to the organisers' production artwork.
      <br><sub>QR code ID cards.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="evidence/juliao-martins-badge-scan.jpg" alt="A phone scanning a delegate's ID card">
      <h3>III. One scan</h3>
      Registered last week or a minute ago, it makes no difference: a phone
      scans the ID card and the visitor is checked in.
      <br><sub>A phone scans the ID card.</sub>
    </td>
    <td width="50%" valign="top">
      <a href="evidence/juliao-martins-welcome.mp4" title="Open the original MP4"><img src="evidence/juliao-martins-welcome.webp" alt="Video: a scan, then the welcome on the lobby screen"></a>
      <h3>IV. Welcome on screen</h3>
      The lobby screen greets the visitor by name and photograph in about
      200 ms, then waits for the next arrival.
      <br><sub>▶ Filmed at the event: scan, then welcome. <a href="evidence/juliao-martins-welcome.mp4">Original MP4</a></sub>
    </td>
  </tr>
</table>

---

## From the floor

Photographs from DRCCMD 2026 at Palm Spring. Click any one to open it full size.

<table>
  <tr>
    <td width="50%"><a href="evidence/juliao-martins-lobby-screen.jpg"><img src="evidence/juliao-martins-lobby-screen.jpg" alt="Check-in desk in front of the lobby screen"></a><br><sub><b>Nº 02</b> — Check-in desk in front of the lobby screen.</sub></td>
    <td width="50%"><a href="evidence/juliao-martins-scan-closeup.jpg"><img src="evidence/juliao-martins-scan-closeup.jpg" alt="A delegate's badge scanned at the registration desk"></a><br><sub><b>Nº 03</b> — A delegate's badge scanned at the registration desk.</sub></td>
  </tr>
  <tr>
    <td><a href="evidence/juliao-martins-scan-batik.jpg"><img src="evidence/juliao-martins-scan-batik.jpg" alt="Badge and phone: checked in"></a><br><sub><b>Nº 04</b> — Badge and phone: checked in.</sub></td>
    <td><a href="evidence/juliao-martins-scan-arrival.jpg"><img src="evidence/juliao-martins-scan-arrival.jpg" alt="Checking in a delegate on arrival"></a><br><sub><b>Nº 05</b> — Checking in a delegate on arrival.</sub></td>
  </tr>
  <tr>
    <td><a href="evidence/juliao-martins-scan-desk.jpg"><img src="evidence/juliao-martins-scan-desk.jpg" alt="Scanning badges at the door"></a><br><sub><b>Nº 06</b> — Scanning badges at the door.</sub></td>
    <td><a href="evidence/juliao-martins-drccmd-stage.jpg"><img src="evidence/juliao-martins-drccmd-stage.jpg" alt="On stage at the Díli Regional Cooperative Conference"></a><br><sub><b>Nº 07</b> — On stage at the Díli Regional Cooperative Conference.</sub></td>
  </tr>
  <tr>
    <td><a href="evidence/juliao-martins-desk-ready.jpg"><img src="evidence/juliao-martins-desk-ready.jpg" alt="The desk, ready for the next arrival"></a><br><sub><b>Nº 08</b> — The desk, ready for the next arrival.</sub></td>
    <td><a href="evidence/juliao-martins-scan-queue.jpg"><img src="evidence/juliao-martins-scan-queue.jpg" alt="Keeping the line moving"></a><br><sub><b>Nº 09</b> — Keeping the line moving.</sub></td>
  </tr>
  <tr>
    <td><a href="evidence/juliao-martins-scan-lounge.jpg"><img src="evidence/juliao-martins-scan-lounge.jpg" alt="Check-in in the lounge"></a><br><sub><b>Nº 10</b> — Check-in in the lounge.</sub></td>
    <td><a href="evidence/juliao-martins-asean-expo.jpg"><img src="evidence/juliao-martins-asean-expo.jpg" alt="Alongside the ASEAN Cooperative Expo 2026"></a><br><sub><b>Nº 11</b> — Alongside the ASEAN Cooperative Expo 2026.</sub></td>
  </tr>
</table>

---

<sub>BEHIND THE SCENES</sub>

## Made by Inovtec

Inovtec, my team, built the Visitor and Queue System and the official DRCCMD
and ASEAN Cooperative Expo website — and ran the system on site for the whole
event.

| | |
|---|---|
| **Studio** | Inovtec |
| **Built** | Visitor and Queue System |
| **Also built** | Official DRCCMD & ACE website |

[**Visit Inovtec →**](https://inovtec.digital) &nbsp;·&nbsp; [**Visit cooptl.com →**](https://cooptl.com/)

<table>
  <tr>
    <td width="50%" valign="top"><img src="evidence/juliao-martins-inovtec-mission.jpg" alt="The Inovtec team with H.E. Arsénio Pereira da Silva"><br><sub><b>Mission complete</b> — the team with H.E. Arsénio Pereira da Silva, Secretary of State for Cooperatives (SECoop), Timor-Leste.</sub></td>
    <td width="50%" valign="top"><img src="evidence/juliao-martins-inovtec-team.jpg" alt="The Inovtec team running the system during the event"><br><sub><b>Behind the scenes</b> — the team running the system during the event.</sub></td>
  </tr>
</table>

---

<sub>AFTER THE EVENT</sub>

## Ask the data

The doors closed on 3 October, and the questions started: *how many delegates
came on the second day? Which VIP guests never arrived? Can I have that as
Excel?* Each answer was in the system, but behind filters, date pickers and
export buttons.

So the dashboard gained an assistant. An admin opens it from the top bar and
asks in plain words — in **English, Portuguese or Tetun** — and gets the answer
in a sentence, with a **Download** button when they asked for a PDF, Excel or
CSV.

```
Admin:      Which VIP guests from Indonesia never arrived? Send me the PDF.
Assistant:  6 VIP guests never arrived. Two were from Indonesia:
            · Siti Rahmawati, Kementerian Koperasi
            · Agus Wibowo, KopIndo
            [ PDF report — Entrance report, 02/10/2026, Indonesia, VIP   Download ]
```
<sub>Illustrative names.</sub>

**How it answers.** It is retrieval-augmented generation built with LangChain
and OpenAI's `gpt-4o-mini`. The model never sees the database and never writes
SQL: it picks one of seven typed, read-only tools, and each tool reads
PostgreSQL through the same services the reports page uses. So a figure in the
chat and the same figure in the exported file come from one calculation. The
file itself is never generated by the model either: the button fetches the
existing report export with the admin's own login.

**It remembers.** Every conversation is saved in PostgreSQL, privately for each
admin, and reopens from a History view. Within a conversation the server hands
the model the stored history, so *"and on the 3rd?"* just works. Across
conversations it keeps short notes — *"answer in Tetun"*, *"Gate B is the side
gate"* — but only when the admin says *remember*, and each note can be
forgotten with one click.

**It is careful with people.** Visitor names are typed by the public, so the
assistant treats everything a tool returns as data, never as instructions. A
memory note must be built from the admin's own words and may not name a
visitor. Photos, badge codes and database ids never leave the server.
Permanently deleting a visitor also removes their name from saved chats.

<table>
  <tr>
    <td width="33%" valign="top"><b>Plain-language reports</b><br>Arrivals by day, hour, door, country or category; refusals; no-shows — with the PDF, Excel or CSV one click away.</td>
    <td width="33%" valign="top"><b>Three languages, properly</b><br>A shared glossary keeps the chat's words the same as the dashboard's: European Portuguese, Tetun in the INL spelling, and any other language answered in kind.</td>
    <td width="33%" valign="top"><b>Built to be trusted</b><br>Its own automated test suite, read-only data tools, private history per admin, and an invented link or button stripped before it reaches the screen.</td>
  </tr>
</table>

---

## Under the hood

Five applications and one generated contract, in a single monorepo, running on a
closed LAN behind one router — no internet, no cloud, no containers. The one
exception came after the event: the optional chat assistant, which reaches
OpenAI and switches itself off when no API key is set.

### Architecture

```
  Admin laptop                Guard phones                 Lobby screen
  ┌──────────────┐            ┌──────────────┐             ┌──────────────┐
  │ vms-dashboard│            │ vms-scanner  │             │  vms-screen  │
  │ Next.js 16   │            │ Expo / RN    │             │ Next.js, GSAP│
  └──────┬───────┘            └──────┬───────┘             └──────┬───────┘
         │ JWT (HTTP)                │ device token                │ device token
         │                           │ POST /scans                 │ WS  /ws/screen/
         ▼                           ▼                             │ GET /screen/feed
  ┌──────────────────────────────────────────────────────────┐     │
  │  vms-backend — Django · DRF · Channels (ASGI, 1 worker)  │◀────┘
  │  write ScanEvent → transaction.on_commit → group_send    │
  └──────────────────────────┬───────────────────────────────┘
                             ▼
                     PostgreSQL (native)

  vms-desktop (PySide6) starts, watches and stops all of the above.
  vms-contracts: OpenAPI → TypeScript types shared by every frontend.

  Chat assistant (added after the event, optional):
  dashboard panel ─▶ /assistant/chat ─▶ LangChain agent ─▶ read-only tools ─▶ PostgreSQL
                                              └────────▶ OpenAI gpt-4o-mini (internet)
```

### The stack

| Part | Technology |
|---|---|
| **Backend** | Django 6.1, Django REST Framework, SimpleJWT, Django Channels, PostgreSQL |
| **Real-time** | WebSocket push for speed + polling backfill for recovery (`InMemoryChannelLayer`, no Redis) |
| **Admin dashboard** | Next.js 16 (App Router), TypeScript, Tailwind CSS v4, TanStack Query |
| **Guard scanner** | React Native, Expo SDK 57, expo-router, expo-camera, expo-sqlite offline queue |
| **Lobby screen** | Next.js 16, Tailwind CSS v4, GSAP |
| **Control centre** | Python, PySide6 (Qt 6), packaged with PyInstaller |
| **Badges & reports** | ReportLab + qrcode (PDF), openpyxl (Excel) — pure Python |
| **API contract** | drf-spectacular → OpenAPI → openapi-typescript |
| **Languages** | English, Portuguese and Tetun across every interface |
| **Chat assistant** | LangChain (`create_agent`), langchain-openai, OpenAI `gpt-4o-mini`; retrieval from PostgreSQL through typed tools |

### Engineering highlights

- **Sub-second welcome, with no lost arrivals.** Scans are broadcast over
  WebSocket inside `transaction.on_commit`, so a rolled-back scan never reaches
  the wall. When the socket drops or the server restarts, the screen backfills
  from `/screen/feed?since=<id>` and de-duplicates by event id.
- **Works through a bad network.** Every scan is written to an on-device SQLite
  queue first and synced with backoff, carrying its own timestamp and a
  client-generated idempotency key — a retried scan never becomes two arrivals.
- **Badges that can't be forged, but can be reprinted.** The QR holds an HMAC
  derived token, never a visitor id. It is unguessable, reproducible for
  reprints, and revocable at scan time by deactivating the visitor.
- **No logins at the door.** Scanners, screens and the walk-in desk pair once
  with a 6-character code and hold a scoped, revocable device token.
- **Self-registration from a phone**, with server-side photo sanitising,
  throttling, duplicate flagging and an offline in-browser face check.
- **Print-accurate ID cards.** The card PDF is measured off the organisers'
  production file to within half a millimetre, one card per page for the card
  printer.
- **Reports the organisers can use.** Entrance logs by hour, outcome and device,
  exported as CSV, branded Excel and PDF.
- **One-click event day.** A desktop control centre checks prerequisites,
  starts the four services in order, and only reports a service *ready* once a
  network probe says so.
- **Reports by conversation.** A LangChain agent answers admins' questions from
  PostgreSQL through read-only tools that share the reports' own calculations,
  and offers the matching PDF, Excel or CSV export instead of writing one.
- **Memory that can't be poisoned.** Chats are stored per admin and reloaded as
  context; cross-conversation notes need the admin's own words, so a crafted
  visitor name cannot plant instructions. A retry carries an idempotency key, so
  a slow answer is never saved twice.

### Repository layout

```
vms/
├── vms-backend/     Django + DRF + Channels + PostgreSQL
├── vms-dashboard/   Next.js — registration, badges, devices, reports
├── vms-scanner/     React Native + Expo — the guard's camera
├── vms-screen/      Next.js — the lobby welcome wall
├── vms-desktop/     PySide6 — the control centre that starts the rest
├── vms-contracts/   generated TypeScript types (OpenAPI → TS)
└── evidence/        photographs and video from the event
```

### Running it locally

```powershell
# Backend — from vms-backend/ (PostgreSQL running as a native service)
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py seed_demo
..\.venv\Scripts\python.exe -m uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers 1
```

```bash
cd vms-dashboard && npm run dev                  # http://<lan-ip>:3000
cd vms-screen    && npm run dev -- --port 3001
cd vms-scanner   && npx expo start -c
```

The chat assistant is optional. To switch it on, add an OpenAI key to
`vms-backend/.env` and restart the backend; without one, the panel says it is
off and everything else works as before.

```bash
OPENAI_API_KEY=sk-...
VMS_ASSISTANT_MODEL=gpt-4o-mini   # the default
```

Or run `vms-desktop/main.py` and press **Run All**. The backend always runs as
a single worker: the in-memory channel layer lives inside one process.
[`CLAUDE.md`](CLAUDE.md) holds the full design notes and the reasoning behind
every constraint.

---

<div align="center">

**Julião Martins** — turning ideas into reliable digital products.

[Portfolio](https://juliaomartins.dev) · [This case study](https://juliaomartins.dev/projects/visitor-queue-system) · [Inovtec](https://inovtec.digital)

<sub>© 2026 Julião Martins</sub>

</div>
